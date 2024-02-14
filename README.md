# Description
This is a command-line tool for assisting with the import of **One Pace** episodes into Plex and setting up its metadata so that it's displayed nicely.

![One Pace library screenshot](/docs/images/one-pace-library-01.png)

Using the `setup-media` command, the application will:
- Copy all downloaded .mkv one pace episodes in a directory into a Plex folder structure so it can be easily dropped into the Plex server media files.
- Download cover images for Seasons and Episodes from onepace.net and place them into the Plex folders so that they'll override the auto-generated ones
    - Make sure you've enabled Local Media Assets on your Plex server. [More info here.](https://support.plex.tv/articles/200220677-local-media-assets-movies/)

After this first stage, you should tell Plex to scan your media files and create the show. Remember that the generated file structure should be placed within your Plex folders under the **One Piece** folder.

Then using the `setup-plex` command, the application will:
- Update all titles and descriptions to match onepace.net

# Installing
Installer:
1. Download oppa-setup.exe from the [latest release](https://github.com/JakeLunn/one-pace-plex-assistant/releases).
2. Run installer

Manual:
1. Download the latest release .exe and place it somewhere, preferably into its own folder e.g. `C:\tools\one-pace-plex-assistant`.
2. Add this folder to the system PATH
3. Open command prompt, terminal or powershell and type `oppa -h` as a test.

Via Source Code:
1. `git clone` this repo
1. [Download and install Python](https://www.python.org/downloads/)
1. Open a new terminal / command prompt at the root of the repo
1. run `pip install -r requirements.txt`
1. Run main.py with `python main.py <command> <your args>`

# How to Use
The command-line is split into 2 main functions: 

## `setup-media` 
This should be the first command you run. 

### Arguments
`--source-dir` 
The path to the directory that contains your .mkv files downloaded via onepace.net. These files can be within sub-directories of the directory provided, too. The following folder structures will work:
```
/source_dir
    - /sub_dir
        - downloaded-video01.mkv
    - /sub_dir
        - downloaded-video02.mkv
OR

/source_dir
    - downloaded-video.mkv
    - downloaded-video02.mkv
```

#### `--target-dir`
> Note: This can be a path to either a local storage directory or, if applicable, to the Plex folders themselves e.g. `[..]/plex/media/anime/One Piece`

This is the path to the directory where your downloaded files will be **copied** to, renamed, and put into folders so that it matches a format that Plex is expecting. 

## `setup-plex`
This should be done only **after Plex has scanned your media files and created the show/episode in Plex**. You'll notice that the show's metadata (titles, descriptions, show name) will not be correct. This command will update all the metadata to the titles & descriptions from onepace.net.

> Note: You can run this command every time you add new episodes. It won't make any changes to episodes which already have correct titles and descriptions.

### Arguments

#### `--plex-token`
Your plex token. This is easy to get. Instructions are here: [Finding an authentication token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

#### `--plex-host`
Your Plex server's host URL. If your server is hosted locally, it will likely be a `localhost` address. If it's hosted on the web, then just the url to your plex instance should be fine e.g. `https://plex.mycoolwebsite.net`

#### `--plex-library`
The name of the Plex library that contains the One Pace episodes e.g. `Anime`, `TV`

#### `--one-piece-show-name`
*Optional*: The name of the show in Plex. If you've changed it from One Piece to One Pace already, then you should set this as "One Pace"

#### `--change-show-name`
*Optional*: If this flag is included, then the show name will be changed to `One Pace` via metadata (the folder will remain `/One Piece`).

## Example Usage
- Get help with commands and arguments
    - `oppa -h`
    - `oppa setup-media -h`
    - `oppa setup-plex -h`
- Setup media
    - ```bash
            oppa setup-media \
            --source-dir "C:\downloads" \
            --target-dir "C:\plex-staging"
      ```
- Setup plex
    - ```bash
            oppa setup-plex \
            --plex-token "myplextoken" \
            --plex-host "http://localhost:32400" \
            --plex-library "Anime" \
            --one-piece-show-name "One Pace" \
            --change-show-name
      ```

# FAQ / Caveats
### Caveats
- You can't have One Piece standard episodes + One Pace episodes in the same Plex library.
    - **Why?** Because Plex doesn't have the ability to create shows that can't be matched to an existing TV show. That's why this app chooses to 'use' the One Piece show and then rename all of its metadata. Not ideal, but Plex doesn't have *good* support for custom shows.
- The application will not download the episodes for you. 
- The application will not upload episodes to remote-hosted plex servers or cloud storage like google drive. You will need to do this upload yourself, albeit it's very easy since the entire folder structure + files are created for you.
    - If your Plex is hosted on the same local machine then you can just set the `--target-dir` to the appropriate folder.
- The application reads file names to match them to the correct arcs/episodes from onepace.net. There was 1 mistake that had to be corrected already (whisky peak files were named whiskey peak) in-code and there could be more in future arcs/episodes. Please report any issues like this here on Github and I'll do my best to address.
- This application could be rendered obselete if there are major changes to onepace.net or to the way the files are named. Again, will do my best to keep it up to date.
