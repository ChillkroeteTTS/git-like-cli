# git-like

> Give your coworkers the appreciation they deserve without enduring the complex dynamics of social interaction.

When browsing the code base of coworkers or open-source projects I often find myself appreciating the work of my fellow coders.
Be it because they found a smart solution for a problem or just because they kept to a certain style guide we committed on.
However, communication can be a tedious task which distracts the sender as well as the receiver, so the appreciation usually does not cross the borders of my brain.

Git-like is a small CLI which aims to make everyday life of us programmers a bit more collaborative, fun and finally - rewarding. 

The concept is quite simple. Whenever you find a nice piece of code, you like it by typing something like

``` bash
$ git-like like FILE FROM_LINE TO_LINE
```

and the author contributing most to the block of code you select receives a like in shape of a notification.
In between all the frustrations which come with coding, this will give him a small positive incentive to continue his good work.
A digitial clap on the shoulder.

By using information from your git configuration, git-likes setup is minimal.

## Setup
You are 4 steps apart from liking and receiving likes:

### 1) Installation
```
$ pip install git-like
```

### 2) Claiming your email address
To prevent other people from using your email, you need to claim it.
Therefore, we will email you an access code.

```bash
$ git-like claim YOUR-EMAIL
$ git-like claim YOUR-EMAIL --code ACCESS_CODE
```

### 3) Starting the daemon
git-like comes with a lightweight background process checking for new likes. You can start and stop it by using the cli.

```bash
$ git-like start
$ git-like stop
```

Git-like uses the email in your commits and in your ~/.gitconfig file to identify you. Be sure to configure your config correctly to receive likes.

## Commands
- `git-like claim YOUR-EMAIL` - Request an access token for your email
    - YOUR_EMAIL - The email address you have configured in your .gitconfig.
- `git-like claim YOUR-EMAIL --code CODE` - Enter your access token to claim your email address
    - YOUR_EMAIL - The email address you have configured in your .gitconfig.
    - CODE - The code we sent you in an email
- `git-like like FILE LINE_TO LINE_FROM` - Like a set of lines in a given file
    - FILE - The (local) file containing the code snippet you want to like. The file must be part of a git project
    - LINE_FROM - A number indicating the start of the code snippet you want to like 
    - LINE_TO - A number indicating the end of the code snippet you want to like 
- `git-like start` - Start the git-like daemon to be able to receive likes 
- `git-like stop` - Stop the git-like daemon to stop receiving likes 

## Privacy
We only collect metadata. So your code is safe.
Git-like collects following information when you like a piece of code:
- your email
- authors email
- line number
- git project url

## Integrations
A Jetbrains Intellij plugin is WIP.
