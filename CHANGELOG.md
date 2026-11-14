## [Unreleased] - xxxx-xx-xx

### Added

- Added `SECURITY.md`.
- Added `CONTRIBUTING.md`.
- Added `.github/` with issue and pull request templates.
- Added `.env.example` containing example environment variables.
- Added a README template for translators and localisers.

### Changed

- Renamed localised README files from `XX_README.md` to `README_XX.md` and updated the `!help` command accordingly.

## [0.15.0] - 2026-11-11

### Added

- Added display name caching with automatic expiration cleanup.
- Added a success flagging system for JSON file writes.
- Added new error messages for failed setting updates, synchronisation, and data deletion.
- Added a maximum attempt limit when generating the Word of the Day.
- Added a global user data deletion command: `!delete all`.
- Made sentiment analysis filtering permanent, using the NLTK VADER lexicon to identify posts with negative sentiment.
- Added NLTK to `requirements.txt`.
- Updated the `README.md` and its localised versions with information about sentiment analysis, the data deletion command, and command handling.

### Changed

- Implemented exponential backoff for Jetstream reconnections.
- Changed filter checking so that posts fail validation if an error occurs during filtering, rather than incorrectly passing.
- Moved synchronous functions into threads to prevent blocking the main event loop.
- Implemented atomic JSON file writing using temporary files.
- Changed data paths to resolve relative to the working directory.
- Reordered post validation checks.
- Changed Word of the Day duplicate checking to check the bot's last five posts instead of relying on the time of day.
- Updated command handling to process up to ten recent commands within a five-minute window.

### Fixed

- Fixed an issue where URIs were incorrectly resolved in the post flags filter.
- Defaulted missing bot data to an empty dictionary when an account DID was not found in the data file
- Removed unused imports and parameters.


## [0.14.1] - 2026-11-10

### Changed

- Replaced links to localised README files with buttons.


## [0.14.0] - 2026-11-08

### Added

- Added the `!language` command, allowing users to switch between supported languages.
- Added a Swedish translation of `locales.json`.
- Added a Swedish translation of `messages.json` and expanded the English responses.
- Added a Swedish translation of `README.md`, saved as `SV_README.md`.
- Added a table of contents to `README.md`.
- Added information about language support and the `!language` command to `README.md`.

### Changed

- Updated the `!settings` command to display language names instead of language codes.
- Updated the `make_post` function to use the user's selected language, defaulting to English if the selected language is unavailable.


## [0.13.1] - 2026-11-06

### Changed

- Updated setting update and error responses to use language specific messages from `locales.json` instead of hardcoded text.
- Updated the `!help` command to link to the corresponding localised README file based on the user's selected language.


## [0.13.0] - 2026-11-05

### Changed

- Updated bot account configuration to dynamically load accounts from numbered environment variables instead of requiring them to be hardcoded.


## [0.12.1] - 2026-11-01

### Added

- Added information about the temporary sentiment analysis filtering to `README.md`.


## [0.12.0] - 2026-06-08

### Added

- Added a Word of the Day feature to Evil Teto.
- Added `wonderwords` to `requirements.txt`.
- Added information about the Word of the Day feature to `README.md`.

### Changed

- Updated the `Filters` class to receive the keyword list as an argument instead of loading it internally.
- Updated the `bots` dictionary to store each bot's handle.

### Fixed

- Fixed the `Filters` class and `refresh_followers` worker using incorrect client instances.


## [0.11.1] - 2026-05-31

### Changed

- Updated `README.md` to use a new format for command examples.
- Removed an unused `requests.Session` instance.


## [0.11.0] - 2026-05-29

### Added

- Added the `!sync` command to synchronise settings between bots.
- Added information about the `!sync` command to `README.md`.

### Changed

- Organised user data by bot DID instead of sharing it between bots.
- Updated post validation checks to use the bot's DID.
- Updated the `!help` command to point to the new GitHub URL.

### Fixed

- Fixed post deletion checks by passing the bot's DID into `delete_post` to verify that the reply belongs to the correct bot.


## [0.10.1] - 2026-05-28

### Added

- Added information about the Evil Teto bot to `README.md`.

### Changed

- Refactored `main.py` to support multiple bot instances and workers.
- Updated the Jetstream connection to enqueue events across each bot's worker queue.
- Refactored `DmWorker` to process direct messages for all configured bots.
- Updated `PostManager` to accept the `bots` dictionary instead of an individual client.


## [0.10.0] - 2026-05-25

### Changed

- Updated account label and post label fetching to use the client object instead of HTTP requests.

### Fixed

- Fixed an issue where accounts with any flags were filtered, rather than only accounts with Bluesky moderation flags.
- Fixed an issue where the message was not being passed to `post_flags`.
- Fixed an issue where `interval_time` was called instead of `interval`.


## [0.9.0] - 2026-05-24

### Added

- Added a filtering system to check for blocked keywords, posts containing links, accounts with moderation flags, and posts with moderation flags.
- Added `blocklist.txt` to store keywords used by the keyword filter.
- Implemented filter checks in `PostManager`.
- Added information about the filtering system and 60 second cooldown to `README.md`.

### Changed

- Enforced a 60 second cooldown between posts for all users.


## [0.8.0] - 2026-02-03

### Added
- Added a default first reply that is sent when a user follows the bot.

### Changed
- Added maximum sizes to `queue` and `json_queue`.
- Refactored classes to receive user data and bot information during initialisation instead of passing them into each method.


## [0.7.2] - 2026-01-16

### Changed

- Refactored setting removal to use a dedicated `remove` operation in the JSON queue instead of the `!pop_entry` instruction.


## [0.7.1] - 2026-01-03

### Added

- Added support for ranged values in the `!interval` command.
- Added the `!skip` command, allowing users to configure a fixed or randomised number of posts to skip before replying.
- Added information about the `!skip` command and interval ranges to `README.md`.

### Changed

- Refactored post handling into a `PostManager` class, handling post creation, deletion, and reply checks.
- Updated the worker and `main.py` to use and initialise the `PostManager`.
- Improved settings formatting and corrected typos in command responses.


## [0.7.0] - 2026-01-01

### Changed

- Refactored the repository to focus solely on the Whimsy Miku bot.
- Refactored command handling into a `CommandManager` class, separating it from `DmWorker`.
- Refactored `check_dms` into a `DmWorker` class.
- Updated `.gitignore` to ignore the `/data` directory.
- Updated `LICENSE` to extend the copyright year to 2026.
- Updated the README with support for variable intervals and the maximum nickname length.
- Updated the bot's account information in the README.

### Fixed

- Fixed an issue where messages were not correctly being retrieved from the message list.


## [0.6.1] - 2025-12-07

### Added

- Added a `disconnect` method to the Jetstream.


## [0.6.0] - 2025-11-22

### Added

- Added a `!settings` command, allowing users to view all their settings.
- Added a `!help` command, linking users to the repository.
- Added information about the `!settings` command to `README.md`.


## [0.5.0] - 2025-11-20

### Added

- Added a `!chance` command, allowing users to set the probability of receiving a reply under their posts.
- Added a `!interval` command, allowing users to set a delay between replies under their posts.
- Added error messages for incorrectly formatted commands or invalid values.
- Added information about the post chance and interval settings to `README.md`.

### Changed

- Updated the post handling logic to check the user's chance and interval settings before replying.


## [0.4.2] - 2025-11-16

### Added

- Added an MIT License.
- Added information on the license to `README.md`.
- Added .txt files explaining what each directory was for.

### Changed

- Updated message loading to support all available languages instead of only English.
- Updated message selection to randomly choose a message using its language key.


## [0.4.1] - 2025-11-15

### Changed

- Moved `client.py` to the `utils` directory and renamed the `bsky` directory to `pos`.
- Limited custom nicknames to 20 characters.


### Fixed

- Fixed a naming conflict between the Jetstream connection variable and its `connect` function.


## [0.4.0] - 2025-11-14

### Added
- Added a queued JSON worker for managing user data.
- Added support for custom nicknames in bot replies.
- Added the ability to delete users' stored data.
- Added support for removing individual user settings.
- Added a `README.md` with bot information, usage instructions and a privacy policy.
- Added `requirements.txt`.
- Added `.gitignore`.


## [0.3.1] - 2025-11-06

### Fixed
- Fixed an issue where not all followers were being properly loaded.


## [0.3.0] - 2025-11-03

### Added
- Expanded the selection of available reply messages.
- Added messages that can include the user's display name.


## [0.2.0] - 2025-11-02

### Added
- Added the ability to delete replies by replying to a bot post with "delete".


## [0.1.3] - 2025-10-28

### Changed
- Replaced the followers text file with a set that refreshes every 2 minutes.


## [0.1.2] - 2025-10-26

### Changed
- Refactored the code to allow the bot to run as a subprocess alongside another bot.


## [0.1.1] - 2025-10-25

### Fixed
- Fixed an issue where followers were sometimes not being added to the followers text file.


## [0.1.0] - 2025-10-24

### Added
- Initial reply functionality.
- Initial follower tracking functionality.
- Initial bot messages.