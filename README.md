# elona_server
Replacement chat server for [Elona](http://ylvania.org/en/elona) and [Elona+](http://wikiwiki.jp/elonaplus/?FrontPage).

If the `serverList` option in the "config.txt" file is set to `1` or the game is started with no Internet connection, the servers listed in the "server.txt" file in the game directory will be used.

Format of the "server.txt" file:

    chat.server.hostname%voting.server.hostname%

Note that the game prepends `www.` to both hostnames before resolving them.
The moongate server hostname is hardcoded, so an official update/patch to decompiled HSP would have to be made.
