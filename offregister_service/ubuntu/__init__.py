from offregister_fab_utils.ubuntu.systemd import (
    install_upgrade_service,
    restart_systemd,
)


def install_service0(conf_name, *args, **kwargs):
    install_upgrade_service(
        conf_name,
        conf_local_filepath=kwargs.get("systemd-conf-file"),
        context={
            "ExecStart": kwargs["ExecStart"]
            if isinstance(kwargs["ExecStart"], str)
            else " ".join(kwargs["ExecStart"]),
            "Environments": kwargs["Environments"],
            "WorkingDirectory": kwargs["WorkingDirectory"],
            "User": kwargs["User"],
            "Group": kwargs["Group"],
        },
    )
    return restart_systemd(conf_name)
