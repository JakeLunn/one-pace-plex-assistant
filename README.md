# Description
This is a command-line tool for assisting with the import of **One Pace** episodes into Plex and setting up its metadata so that it's displayed nicely.

![One Pace library screenshot](docs\images\one-pace-library-01.png)

Using the `setup-media` command, the application will:
- Copy all downloaded .mkv one pace episodes in a directory into a Plex folder structure so it can be easily dropped into the Plex server media files.
- Download cover images for Seasons and Episodes from onepace.net and place them into the Plex folders so that they'll override the auto-generated ones
    - Make sure you've enabled Local Media Assets on your Plex server. [More info here.](https://support.plex.tv/articles/200220677-local-media-assets-movies/)

After this first stage, you should tell Plex to scan your media files and create the show. Remember that the generated file structure should be placed within your Plex folders under the **One Piece** folder.

Then using the `setup-plex` command, the application will:
- Update all titles and descriptions to match onepace.net

# How to Use
The command-line is split into 2 main functions: 

## `setup-media` 
This should be the first command you run. It takes 2 required arguments: 

### `--source-dir` 
The first should be the path to the directory that contains your .mkv files downloaded via onepace.net. These files can be within sub-directories of the directory provided, too. The following folder structures will both work:
```
- /source_dir
    - /sub_dir
        - downloaded-video01.mkv
    - /sub_dir
        - downloaded-video02.mkv
OR

- /source_dir
    - downloaded-video.mkv
    - downloaded-video02.mkv
```

### `--target-dir`
> Note: This can be a path to either a local storage directory or, if applicable, to the Plex folders themselves e.g. `[..]/plex/media/anime/One Piece`

This is the path to the directory where your downloaded files will be **copied** to, renamed, and put into folders so that it matches a format that Plex is expecting. 

## `setup-plex`
This should be done only **after Plex has scanned your media files and created the show/episode in Plex**. You'll notice that the show's metadata (titles, descriptions, show name) will not be correct. This command will update all the metadata to the titles & descriptions from onepace.net.

> Note: You can run this command every time you add new episodes. It won't make any changes to episodes which already have correct titles and descriptions.

### `--plex-token`
Your plex token. This is easy to get, instructions here: [Finding an authentication token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

### `--plex-host`
Your Plex server's host URL. If your server is hosted locally, it will likely be a `localhost` address. If it's hosted on the web, then just the url to your plex instance should be fine e.g. `https://plex.mycoolwebsite.net`

### `--plex-library`
The name of the Plex library that contains the One Pace episodes e.g. `Anime`, `TV`, etc.

### `--one-piece-show-name`
The name of the show in Plex. If you've changed it from One Piece to One Pace already, then you should set this as: `--one-piece-show-name "One Pace"`

### `--change-show-name`
*Optional*: If this flag is included, then the show name will be changed to `One Pace` via metadata (the folder will remain `/One Piece`).
