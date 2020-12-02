# git-like

> Give your coworkers the appreciation they deserve without enduring the complex dynamics of social interaction.

When browsing the code base of coworkers or open-source projects I often find myself appreciating the work of my fellow coders.
Be it because they found a smart solution for a problem or just because they kept to a certain style guide we committed on.
However, with communication being can be a tedious task which distracts the sender as well as the receiver, this appreciation stays usually in my head.

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

## Integrations
A Jetbrains Intellij plugin is WIP.
