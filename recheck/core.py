#
# core.py
#
# Copyright (C) 2017 Hielke Christian Braun <hcb@unco.de>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

class Core(CorePluginBase):
    def enable(self):
        log.info("[recheck] enable")
        eventmanager = component.get("EventManager")
        eventmanager.register_event_handler("TorrentFinishedEvent", self.on_event_torrent_finished)
        eventmanager.register_event_handler("SessionStartedEvent", self.on_event_session_started)

    def disable(self):
        pass

    def update(self):
        pass

    def on_event_torrent_finished(self, torrent_id):
        torrentmanager = component.get("TorrentManager")
        t = torrentmanager.torrents.get(torrent_id, None)
        t.force_recheck()
        t.resume()
        log.info("[recheck] torrent finished recheck: %s / %s", t.torrent_id, t.state)

    def on_event_session_started(self):
        log.debug("[recheck] on_event_session_started")
        torrentmanager = component.get("TorrentManager")
        torrent_ids = torrentmanager.get_torrent_list()
        for i in torrent_ids:
            t = torrentmanager.torrents.get(i, None)
            t.force_recheck()
            t.resume()
            log.info("[recheck] session started recheck: %s / %s", t.torrent_id, t.state)

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config
