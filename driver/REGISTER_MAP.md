# PiPower5 MCU I2C Register Map

I2C Address: **0x5C**

## Read Registers (16-bit word reads use `i2c_smbus_read_word_data`)

| Addr | Bits | Name | Unit | Description |
|------|------|------|------|-------------|
| 0 | 16 | `input_voltage` | mV | Input voltage (USB/VBUS) |
| 2 | 16 | `input_current` | mA | Input current |
| 4 | 16 | `output_voltage` | mV | Output voltage to Raspberry Pi |
| 6 | 16 | `output_current` | mA | Output current to Raspberry Pi |
| 8 | 16 | `battery_voltage` | mV | Battery voltage **(signed: +charge, -discharge)** |
| 10 | 16 | `battery_current` | mA | Battery current **(signed: +charge, -discharge)** |
| 12 | 8 | `battery_percentage` | % | Battery charge percentage (0-100) |
| 13 | 8 | `battery_capacity` | % | Battery capacity percentage |
| 15 | 8 | `power_source` | — | 0=External(USB), 1=Battery |
| 16 | 8 | `is_input_plugged_in` | — | 0=Unplugged, 1=Plugged |
| 18 | 8 | `is_charging` | — | 0=Not charging, 1=Charging |
| 20 | 8 | `shutdown_request` | — | 0=None, 1=LowBattery, 2=Button, 3=LowVoltage |
| 128 | 8 | `fw_major` | — | Firmware major version |
| 129 | 8 | `fw_minor` | — | Firmware minor version |
| 130 | 8 | `fw_patch` | — | Firmware patch version |
| 139 | 8 | `default_on` | — | 0=Off, 1=On (auto power-on when input connected) |
| 140-141 | 16 | `board_id` | — | Board hardware ID |
| 143 | 8 | `shutdown_percentage` | % | Auto-shutdown battery threshold |
| 145 | 16 | `battery_internal_resistor` | mΩ | Battery internal resistance |
| 154 | 8 | `power_button_state` | — | See button states below |
| 155 | 8 | `charge_current_max` | ×100mA | Max charging current |
| 162 | 8 | `buzzer_volume` | % | Buzzer volume (0-100) — **may not be supported on all firmware** |

## Write Registers

| Addr | Bits | Name | Range | Description |
|------|------|------|-------|-------------|
| 9 | 8 | `shutdown_percentage` | 0-100 | Set auto-shutdown battery threshold (persisted in MCU) |
| 11 | 8 | `charge_select` | — | Charge current selection |
| 12 | 8 | `power_btn_state` | 0 | Write 0 to clear button state register |
| 13 | 8 | `buzzer_freq_l` | 0-255 | Buzzer frequency low byte |
| 14 | 8 | `buzzer_freq_h` | 0-255 | Buzzer frequency high byte (freq = L + H*256, max 65534) |
| 15 | 8 | `buzzer_vol` | 0-100? | Buzzer volume — **behavior unconfirmed, may not be functional** |

## ADV_CMD Protocol (for VBUS control)

| Byte | Value | Description |
|------|-------|-------------|
| START | 0xAC | Command start marker |
| CMD | 0x01 | VBUS enable command |
| DATA | 0/1 | 1=Enable, 0=Disable |
| END | 0xAE | Command end marker |
| Response | 0xE0=OK, 0xEF=Error | Status byte (read via raw I2C) |

## Power Button States (Register 154)

| Value | Name | Description |
|-------|------|-------------|
| 0 | RELEASED | Button not pressed |
| 1 | CLICK | Short press |
| 2 | DOUBLE_CLICK | Two quick presses |
| 3 | LONG_PRESS_2S | Held for 2 seconds |
| 4 | LONG_PRESS_2S_RELEASED | Released after 2s hold |
| 5 | LONG_PRESS_5S | Held for 5 seconds (forced power-off imminent) |
| 6 | LONG_PRESS_5S_RELEASED | Released after 5s hold |

## Shutdown Request Values (Register 20)

| Value | Name | Description |
|-------|------|-------------|
| 0 | NONE | No shutdown requested |
| 1 | LOW_BATTERY | Battery below shutdown threshold |
| 2 | BUTTON | Button long-press shutdown |
| 3 | LOW_VOLTAGE | Battery voltage critically low |

## Buzzer Event Bitmask (`buzz_on`)

| Bit | Event | Default Sequence |
|-----|-------|-----------------|
| 0 (0x01) | `battery_activated` | 440Hz,50ms; pause,100ms; 494Hz,50ms |
| 1 (0x02) | `low_battery` | 440Hz,50ms; pause,100ms; 440Hz,50ms |
| 2 (0x04) | `power_disconnected` | 587Hz,50ms; pause,100ms; 392Hz,50ms |
| 3 (0x08) | `power_restored` | 392Hz,50ms; pause,100ms; 587Hz,50ms |
| 4 (0x10) | `power_insufficient` | 494Hz,50ms; pause,100ms; 494Hz,50ms; pause,100ms; 494Hz,100ms |
| 5 (0x20) | `battery_critical_shutdown` | 1047Hz,50ms; pause,60ms; 1047Hz,50ms; pause,60ms; 1047Hz,100ms |
| 6 (0x40) | `battery_voltage_critical_shutdown` | 1047Hz×3 with pauses |
| 0x7F | ALL ENABLED (default) | |
| 0x00 | ALL DISABLED | |
