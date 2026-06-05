# pipower5 bash completion
_pipower5_completion() {
    local cur prev words cword
    _init_completion || return

    local commands="start stop doctor uninstall"

    case $prev in
        --debug-level|-dl)
            COMPREPLY=( $(compgen -W "debug info warning error critical" -- "$cur") )
            return
            ;;
        --temperature-unit|-u)
            COMPREPLY=( $(compgen -W "C F" -- "$cur") )
            return
            ;;
        --send-email-on|-seo|--buzz-on|-bzo)
            COMPREPLY=( $(compgen -W "battery_activated low_battery power_disconnected power_restored power_insufficient battery_critical_shutdown battery_voltage_critical_shutdown" -- "$cur") )
            return
            ;;
        --smtp-security|-ssc)
            COMPREPLY=( $(compgen -W "none ssl tls" -- "$cur") )
            return
            ;;
    esac

    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $(compgen -W "--version --config --debug-level --database-retention-days --remove-dashboard --config-path --shutdown-percentage --input-voltage --input-current --output-voltage --output-current --battery-voltage --battery-current --battery-percentage --battery-source --is-input-plugged-in --is-charging --default-on --shutdown-request --power-btn --charging-current --all --firmware --power-failure-simulation --send-email-on --send-email-to --smtp-server --smtp-port --smtp-email --smtp-password --smtp-security --buzz-on --buzzer-volume --buzzer-test --temperature-unit --fix" -- "$cur") )
        return
    fi

    COMPREPLY=( $(compgen -W "$commands" -- "$cur") )
}

complete -F _pipower5_completion pipower5
