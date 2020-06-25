#!/usr/bin/env python

import sys
import os
from cmd import Cmd

import libtmux


class Shell(Cmd):
    def __init__(self, *args):
        self.args = args
        self.server = libtmux.Server()
        self.s_name = os.environ['TMUX'].split(',')[2]
        self.infos = {}
        for pbx in args:
            session = self.server.find_where({'session_name': pbx})
            created = False
            if session is None:
                created = True
                session = self.server.new_session(pbx, attach=False)
            w = session.attached_window
            pane = w.attached_pane
            self.infos[pbx] = {
                'session': session,
                'window': w,
                'pane': pane,
            }
            if created is True:
                pane.send_keys('ssh {}'.format(pbx))

        Cmd.__init__(self)

    def stop(self):
        for pbx in self.infos.keys():
            self.infos[pbx]['session'].kill_session()

    def default(self, line):
        try:
            if line == "!q":
                self.stop()
                return True
            elif line[:1] == "!":
                nb = 0
                if line[1:] != "":
                    nb = int(line[1:])
                pane = self.infos[self.args[nb]]['pane']
                print('\n'.join(pane.cmd('capture-pane', '-p').stdout))
            else:
                for pbx in self.infos.keys():
                    self.infos[pbx]['pane'].send_keys(line)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    shell = Shell(*sys.argv[1:])
    shell.cmdloop()
