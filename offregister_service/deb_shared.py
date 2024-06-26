# -*- coding: utf-8 -*-
from offregister_fab_utils.ubuntu.systemd import (
    install_upgrade_service,
    restart_systemd,
)
from offutils import ensure_separated_str, iteritems


def add_to_environment(v):
    """
    Generate the `Environment=` row for the service file

    :param v: Value
    :type v: ```Union[str, dict]```

    :return: `Environment=` row for the service file
    :rtype: ```str```
    """
    return "Environment='{}'".format(
        "\nEnvironment=".join(
            "{}={}".format(k, "".join(map(str, v))) for k, v in iteritems(v)
        )
        if isinstance(v, dict)
        else v
    )


def install_service0(c, conf_name, *args, **kwargs):
    """
    Install the service (creates the .service file)

    :param c: Connection
    :type c: ```fabric.connection.Connection```

    :param conf_name: Configuration file name (.service file)
    :type conf_name: ```str```

    :param kwargs: Keyword arguments
    :type kwargs: ```TypedDict('ServiceKwargs', { 'ExecStart': str, 'Environments': str,
                                                  'WorkingDirectory': str, 'User': str,
                                                  'systemd-conf-file': Optional[str] })```

    :return: `restart_systemd` output, i.e., res.stdout if res.exited == 0 else res.stderr
    :rtype: ```str```
    """
    install_upgrade_service(
        c,
        conf_name,
        conf_local_filepath=kwargs.get("systemd-conf-file"),
        context={
            "ExecStart": ensure_separated_str(kwargs["ExecStart"], " \\\n  "),
            "Environments": ensure_separated_str(
                map(add_to_environment, kwargs["Environments"])
                if isinstance(kwargs["Environments"], (list, tuple))
                else kwargs["Environments"],
                "\n",
            ),
            "WorkingDirectory": kwargs["WorkingDirectory"],
            "User": kwargs["User"],
            "Group": kwargs["Group"],
        },
    )
    return restart_systemd(c, conf_name)


__all__ = ["install_service0"]
