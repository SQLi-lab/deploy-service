import os
import sys

import ansible_runner

from config.config import logger, ANSIBLE_TIMEOUT, ANSIBLE_PLAYBOOKS_DIR


class AnsibleApi:
    def __init__(self):
        self.timeout = ANSIBLE_TIMEOUT
        self.playbooks_dir = ANSIBLE_PLAYBOOKS_DIR

    def start_playbook(self, playbook_name: str = None, uuid: str = None):
        if playbook_name is None or uuid is None:
            err = "Пустые uuid или имя плэйбука"
            logger.error(err)
            raise Exception(err)

        os.chdir(self.playbooks_dir)

        try:
            out, err, _ = ansible_runner.run_command(
                executable_cmd='ansible-playbook',
                cmdline_args=[f'{playbook_name}.yml', '-i', 'inventory.yml', '-e', f'UUID={uuid}'],
                input_fd=sys.stdin.fileno(),
                timeout=self.timeout
            )
        except Exception as e:
            err = f'Ошибка запуска плэйбука Ansible: {e}'
            logger.error(err)
            raise Exception(err)

        ok = self.parse_out(out)
        if not ok or err is not None:
            err = f'Ошибка выполнения плейбука: {err}'
            logger.error(err)
            raise Exception(err)

    def parse_out(self, output) -> bool:
        # TODO: реализовать проверку out
        logger.warn(output)

        return True
