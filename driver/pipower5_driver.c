#include <linux/module.h>
#include <linux/fs.h>
#include <linux/device.h>
#include <linux/cdev.h>
#include <linux/power_supply.h>
#include <linux/ioctl.h>
#include <linux/uaccess.h>
#include <linux/slab.h>
#include <linux/version.h>

#define DEVICE_NAME "pipower5"
#define CLASS_NAME "pipower5"
#define POWER_SUPPLY_NAME "pipower5"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("SunFounder");
MODULE_DESCRIPTION("PiPower 5");
MODULE_VERSION("1.0");

#define VIRTUAL_BATTERY_MAGIC 'V'
#define VIRTUAL_BATTERY_REGISTER _IOW(VIRTUAL_BATTERY_MAGIC, 0x10, struct virtual_battery_props)
#define VIRTUAL_BATTERY_UNREGISTER _IOW(VIRTUAL_BATTERY_MAGIC, 0x11, int)
#define VIRTUAL_BATTERY_UPDATE _IOW(VIRTUAL_BATTERY_MAGIC, 0x12, struct virtual_battery_props)

struct virtual_battery_props {
    char name[32];
    int type;
    int technology; // Technology, 0: Unknown, 1: NiMH, 2: Li-ion, 3: LiPo, 4: LiFe, 5: NiCd, 6: LiMn
    // Basic
    int status; // Battery status, 0: unknown, 1: charging, 2: discharging, 3: full
    int capacity; // Capacity in percentage
    int capacity_level; // Capacity level, 0: Unknown, 1: Critical, 2: Low, 3: Normal, 4: High, 5: Full
    int present; // Is Battery is present, 1: present, 0: not present
    int online; // Is AC power connected, 1: connected, 0: not connected
    // Voltage and current
    long voltage_max_design; // Max voltage design in microvolt
    long voltage_min_design; // Min voltage design in microvolt
    long voltage_now; // Current voltage in microvolt
    long current_now; // Current current in microampere
    // Energy
    long energy_full; // Full energy in microjoule
    long energy_now; // Remaining energy in microjoule
    long energy_full_design; // Full energy design in microjoule
    // Energy rate
    long power_now; // Current power in microwatt
};

static struct power_supply *battery;
static struct virtual_battery_props current_props;
static bool registered = false;

static struct class* virtual_class = NULL;
static struct device* virtual_device = NULL;
static dev_t dev_num;
static struct cdev battery_cdev;

static long battery_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    void __user *argp = (void __user *)arg;
    struct virtual_battery_props props;
    
    switch (cmd) {
    case VIRTUAL_BATTERY_REGISTER:
        if (copy_from_user(&props, argp, sizeof(props)))
            return -EFAULT;
            
        memcpy(&current_props, &props, sizeof(props));
        registered = true;
        printk(KERN_INFO "Virtual battery registered\n");
        return 0;
        
    case VIRTUAL_BATTERY_UNREGISTER:
        registered = false;
        printk(KERN_INFO "Virtual battery unregistered\n");
        return 0;
        
    case VIRTUAL_BATTERY_UPDATE:
        if (copy_from_user(&props, argp, sizeof(props)))
            return -EFAULT;
            
        memcpy(&current_props, &props, sizeof(props));
        return 0;
        
    default:
        return -ENOTTY;
    }
}

static const struct file_operations fops = {
    .unlocked_ioctl = battery_ioctl,
    .owner = THIS_MODULE,
};

static enum power_supply_property virtual_battery_properties[] = {
    POWER_SUPPLY_PROP_STATUS,
    POWER_SUPPLY_PROP_PRESENT,
    POWER_SUPPLY_PROP_ONLINE,
    POWER_SUPPLY_PROP_TECHNOLOGY,
    POWER_SUPPLY_PROP_CAPACITY,
    POWER_SUPPLY_PROP_VOLTAGE_MAX_DESIGN,
    POWER_SUPPLY_PROP_VOLTAGE_MIN_DESIGN,
    POWER_SUPPLY_PROP_VOLTAGE_NOW,
    POWER_SUPPLY_PROP_CURRENT_NOW,
    POWER_SUPPLY_PROP_ENERGY_FULL,
    POWER_SUPPLY_PROP_ENERGY_NOW,
    POWER_SUPPLY_PROP_ENERGY_FULL_DESIGN,
    // Energy rate
    POWER_SUPPLY_PROP_POWER_NOW,

};

static int virtual_battery_get_property(struct power_supply *psy,
                    enum power_supply_property psp,
                    union power_supply_propval *val)
{
    if (!registered)
        return -ENODEV;
        
    switch (psp) {
    case POWER_SUPPLY_PROP_STATUS:
        val->intval = current_props.status;
        break;
    case POWER_SUPPLY_PROP_PRESENT:
        val->intval = current_props.present;
        break;
    case POWER_SUPPLY_PROP_ONLINE:
        val->intval = current_props.online;
        break;
    case POWER_SUPPLY_PROP_TECHNOLOGY:
        val->intval = current_props.technology;
        break;
    case POWER_SUPPLY_PROP_CAPACITY:
        val->intval = current_props.capacity;
        break;
    case POWER_SUPPLY_PROP_VOLTAGE_MAX_DESIGN:
        val->intval = current_props.voltage_max_design;
        break;
    case POWER_SUPPLY_PROP_VOLTAGE_MIN_DESIGN:
        val->intval = current_props.voltage_min_design;
        break;
    case POWER_SUPPLY_PROP_VOLTAGE_NOW:
        val->intval = current_props.voltage_now;
        break;
    case POWER_SUPPLY_PROP_CURRENT_NOW:
        val->intval = current_props.current_now;
        break;
    case POWER_SUPPLY_PROP_ENERGY_FULL:
        val->intval = current_props.energy_full;
        break;
    case POWER_SUPPLY_PROP_ENERGY_NOW:
        val->intval = current_props.energy_now;
        break;
    case POWER_SUPPLY_PROP_ENERGY_FULL_DESIGN:
        val->intval = current_props.energy_full_design;
        break;
    // Energy rate
    case POWER_SUPPLY_PROP_POWER_NOW:
        val->intval = current_props.power_now;
        break;
    default:
        return -EINVAL;
    }
    
    return 0;
}

static const struct power_supply_desc virtual_battery_desc = {
    .name = POWER_SUPPLY_NAME,
    .type = POWER_SUPPLY_TYPE_BATTERY,
    .properties = virtual_battery_properties,
    .num_properties = ARRAY_SIZE(virtual_battery_properties),
    .get_property = virtual_battery_get_property,
};

static int __init virtual_battery_init(void)
{
    int ret;
    
    // 分配设备号
    ret = alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        printk(KERN_ERR "Failed to allocate char device region\n");
        return ret;
    }
    
    // 使用新的class_create接口
    #if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
    virtual_class = class_create(CLASS_NAME);
    #else
    virtual_class = class_create(THIS_MODULE, CLASS_NAME);
    #endif
    
    if (IS_ERR(virtual_class)) {
        printk(KERN_ERR "Failed to create device class\n");
        ret = PTR_ERR(virtual_class);
        goto err_class;
    }
    
    // 创建字符设备
    cdev_init(&battery_cdev, &fops);
    ret = cdev_add(&battery_cdev, dev_num, 1);
    if (ret < 0) {
        printk(KERN_ERR "Failed to add character device\n");
        goto err_cdev;
    }
    
    // 创建设备节点
    virtual_device = device_create(virtual_class, NULL, dev_num, NULL, DEVICE_NAME);
    if (IS_ERR(virtual_device)) {
        printk(KERN_ERR "Failed to create device\n");
        ret = PTR_ERR(virtual_device);
        goto err_device;
    }
    
    // 创建电源供应设备
    battery = power_supply_register(virtual_device, &virtual_battery_desc, NULL);
    if (IS_ERR(battery)) {
        printk(KERN_ERR "Failed to register power supply: %ld\n", PTR_ERR(battery));
        ret = PTR_ERR(battery);
        goto err_psy;
    }
    
    printk(KERN_INFO "Virtual battery driver loaded\n");
    return 0;
    
err_psy:
    device_destroy(virtual_class, dev_num);
err_device:
    cdev_del(&battery_cdev);
err_cdev:
    class_destroy(virtual_class);
err_class:
    unregister_chrdev_region(dev_num, 1);
    return ret;
}

static void __exit virtual_battery_exit(void)
{
    power_supply_unregister(battery);
    device_destroy(virtual_class, dev_num);
    cdev_del(&battery_cdev);
    class_destroy(virtual_class);
    unregister_chrdev_region(dev_num, 1);
    printk(KERN_INFO "Virtual battery driver unloaded\n");
}

module_init(virtual_battery_init);
module_exit(virtual_battery_exit);