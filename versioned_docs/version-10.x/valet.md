<!-- # Laravel Valet -->
# Laravel Valet

- [Introduction](#introduction)
- [Installation](#installation)
    - [Upgrading Valet](#upgrading-valet)
- [Serving Sites](#serving-sites)
    - [The "Park" Command](#the-park-command)
    - [The "Link" Command](#the-link-command)
    - [Securing Sites With TLS](#securing-sites)
    - [Serving a Default Site](#serving-a-default-site)
    - [Per-Site PHP Versions](#per-site-php-versions)
- [Sharing Sites](#sharing-sites)
    - [Sharing Sites on Your Local Network](#sharing-sites-on-your-local-network)
- [Site Specific Environment Variables](#site-specific-environment-variables)
- [Proxying Services](#proxying-services)
- [Custom Valet Drivers](#custom-valet-drivers)
    - [Local Drivers](#local-drivers)
- [Other Valet Commands](#other-valet-commands)
- [Valet Directories and Files](#valet-directories-and-files)
    - [Disk Access](#disk-access)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!NOTE]
> macOS에서 Laravel 애플리케이션을 더욱 쉽게 개발할 수 있는 방법을 찾고 계신가요? [Laravel Herd](https://herd.laravel.com)를 확인해 보세요. Herd에는 Valet, PHP, Composer 등 Laravel 개발을 시작하는 데 필요한 모든 요소가 포함되어 있습니다.

<!-- [Laravel Valet](https://github.com/laravel/valet) is a development environment for macOS minimalists. Laravel Valet configures your Mac to always run [Nginx](https://www.nginx.com/) in the background when your machine starts. Then, using [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet proxies all requests on the `*.test` domain to point to sites installed on your local machine. -->
[Laravel Valet](https://github.com/laravel/valet)은 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet은 사용자의 Mac이 부팅될 때마다 백그라운드에서 항상 [Nginx](https://www.nginx.com/)가 실행되도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해, `*.test` 도메인으로 들어오는 모든 요청을 로컬 머신에 설치된 사이트로 프록시합니다.

<!-- In other words, Valet is a blazing fast Laravel development environment that uses roughly 7 MB of RAM. Valet isn't a complete replacement for [Sail](/docs/10.x/sail) or [Homestead](/docs/10.x/homestead), but provides a great alternative if you want flexible basics, prefer extreme speed, or are working on a machine with a limited amount of RAM. -->
즉, Valet은 약 7MB의 RAM만으로 동작하는 매우 빠른 Laravel 개발 환경입니다. Valet이 [Sail](/docs/10.x/sail)이나 [Homestead](/docs/10.x/homestead)를 완전히 대체하는 것은 아니지만, 최소한의 기능만 필요하거나 빠른 속도를 원하거나, 메모리가 부족한 환경에서 작업하는 경우에 뛰어난 대안이 됩니다.

<!-- Out of the box, Valet support includes, but is not limited to: -->
Valet은 기본적으로 다음과 같은 다양한 프로젝트를 지원합니다:



<!-- <div id="valet-support" markdown="1"> -->
<div id="valet-support" markdown="1">

<!--
- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)
-->
- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

<!-- </div> -->
</div>

<!-- However, you may extend Valet with your own [custom drivers](#custom-valet-drivers). -->
또한, [custom drivers](#custom-valet-drivers)를 직접 추가하여 Valet을 확장할 수도 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Valet은 macOS와 [Homebrew](https://brew.sh/)를 필요로 합니다. 설치 전에 Apache나 Nginx와 같은 다른 프로그램이 로컬 머신의 80번 포트를 사용하고 있지 않은지 반드시 확인하세요.

<!-- To get started, you first need to ensure that Homebrew is up to date using the `update` command: -->
먼저, Homebrew가 최신 버전인지 `update` 명령어로 확인해야 합니다:

```shell
brew update
```

<!-- Next, you should use Homebrew to install PHP: -->
다음으로 Homebrew를 통해 PHP를 설치합니다:

```shell
brew install php
```

<!-- After installing PHP, you are ready to install the [Composer package manager](https://getcomposer.org). In addition, you should make sure the `$HOME/.composer/vendor/bin` directory is in your system's "PATH". After Composer has been installed, you may install Laravel Valet as a global Composer package: -->
PHP가 설치되면, [Composer package manager](https://getcomposer.org)를 설치할 차례입니다. 그리고 시스템의 "PATH"에 `$HOME/.composer/vendor/bin` 디렉터리가 등록되어 있는지 확인하세요. Composer 설치가 완료되면, Laravel Valet을 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

<!-- Finally, you may execute Valet's `install` command. This will configure and install Valet and DnsMasq. In addition, the daemons Valet depends on will be configured to launch when your system starts: -->
마지막으로, Valet의 `install` 명령어를 실행합니다. 이 명령어는 Valet과 DnsMasq를 설치 및 설정하며, Valet이 필요로 하는 데몬들이 시스템 시작 시 자동으로 실행되도록 구성합니다:

```shell
valet install
```

<!-- Once Valet is installed, try pinging any `*.test` domain on your terminal using a command such as `ping foobar.test`. If Valet is installed correctly you should see this domain responding on `127.0.0.1`. -->
Valet 설치가 완료되면, 터미널에서 `ping foobar.test`와 같이 임의의 `*.test` 도메인에 핑을 시도해 보세요. 정상적으로 설치되었다면 해당 도메인이 `127.0.0.1`로 응답하는 것을 확인할 수 있습니다.

<!-- Valet will automatically start its required services each time your machine boots. -->
Valet은 컴퓨터가 부팅될 때마다 필요한 서비스가 자동으로 시작됩니다.

<a name="php-versions"></a>
<!-- #### PHP Versions -->
#### PHP Versions

> [!NOTE]
> 글로벌 PHP 버전을 변경하는 대신, 각 사이트별로 PHP 버전을 지정하고 싶다면 `isolate` [command](#per-site-php-versions)를 사용할 수 있습니다.

<!-- Valet allows you to switch PHP versions using the `valet use php@version` command. Valet will install the specified PHP version via Homebrew if it is not already installed: -->
Valet에서는 `valet use php@version` 명령어를 통해 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 Homebrew에 설치되어 있지 않다면, 자동으로 설치가 진행됩니다:

```shell
valet use php@8.1

valet use php
```

<!-- You may also create a `.valetrc` file in the root of your project. The `.valetrc` file should contain the PHP version the site should use: -->
또한, 프로젝트 루트에 `.valetrc` 파일을 생성하여 사이트에서 사용할 PHP 버전을 지정할 수도 있습니다. `.valetrc` 파일에는 해당 사이트에서 사용할 PHP 버전을 적어주면 됩니다:

```shell
php=php@8.1
```

<!-- Once this file has been created, you may simply execute the `valet use` command and the command will determine the site's preferred PHP version by reading the file. -->
이 파일이 생성된 후에는 `valet use` 명령어만 실행해도 Valet이 해당 파일을 읽어 사이트에 알맞은 PHP 버전을 사용하도록 설정합니다.

> [!WARNING]
> Valet은 여러 PHP 버전이 설치되어 있더라도, 한 번에 한 버전의 PHP만 운영할 수 있습니다.

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- If your application needs a database, check out [DBngin](https://dbngin.com), which provides a free, all-in-one database management tool that includes MySQL, PostgreSQL, and Redis. After DBngin has been installed, you can connect to your database at `127.0.0.1` using the `root` username and an empty string for the password. -->
애플리케이션에서 데이터베이스가 필요하다면, [DBngin](https://dbngin.com)을 확인해 보세요. DBngin은 MySQL, PostgreSQL, Redis를 지원하는 무료 통합 데이터베이스 관리 도구입니다. DBngin 설치 후에는 `127.0.0.1` 주소, `root` 사용자명, 비밀번호는 빈 문자열로 데이터베이스에 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
<!-- #### Resetting Your Installation -->
#### Resetting Your Installation

<!-- If you are having trouble getting your Valet installation to run properly, executing the `composer global require laravel/valet` command followed by `valet install` will reset your installation and can solve a variety of problems. In rare cases, it may be necessary to "hard reset" Valet by executing `valet uninstall --force` followed by `valet install`. -->
Valet이 제대로 실행되지 않거나 문제를 겪고 있다면, `composer global require laravel/valet` 명령어와 이어지는 `valet install` 명령어를 실행하면 설치가 초기화되어 다양한 문제가 해결될 수 있습니다. 극히 드문 경우, `valet uninstall --force`와 `valet install`을 차례로 실행하여 “하드 리셋”이 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
<!-- ### Upgrading Valet -->
### Upgrading Valet

<!-- You may update your Valet installation by executing the `composer global require laravel/valet` command in your terminal. After upgrading, it is good practice to run the `valet install` command so Valet can make additional upgrades to your configuration files if necessary. -->
터미널에서 `composer global require laravel/valet` 명령어를 실행하면 Valet 설치를 최신 버전으로 업그레이드할 수 있습니다. 업그레이드 후, 추가적인 설정 파일 업데이트가 필요한 경우를 위해 `valet install` 명령어를 실행하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
<!-- #### Upgrading to Valet 4 -->
#### Upgrading to Valet 4

<!-- If you're upgrading from Valet 3 to Valet 4, take the following steps to properly upgrade your Valet installation: -->
Valet 3에서 Valet 4로 업그레이드하는 경우, 아래 단계를 따라 올바르게 업그레이드하세요:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- If you've added `.valetphprc` files to customize your site's PHP version, rename each `.valetphprc` file to `.valetrc`. Then, prepend `php=` to the existing content of the `.valetrc` file.
- Update any custom drivers to match the namespace, extension, type-hints, and return type-hints of the new driver system. You may consult Valet's [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) as an example.
- If you use PHP 7.1 - 7.4 to serve your sites, make sure you still use Homebrew to install a version of PHP that's 8.0 or higher, as Valet will use this version, even if it's not your primary linked version, to run some of its scripts.
-->
- 사이트별 PHP 버전을 커스터마이즈하기 위해 `.valetphprc` 파일을 추가했다면, 각 `.valetphprc` 파일명을 `.valetrc`로 변경하고 기존 `.valetrc` 파일 내용 앞에 `php=`를 추가하세요.
- 커스텀 드라이버를 사용하는 경우, 네임스페이스, 확장자, 타입 힌트, 반환값 등 새로운 드라이버 시스템에 맞게 드라이버를 업데이트하세요. Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고할 수 있습니다.
- PHP 7.1~7.4로 사이트를 운영 중이라면, 여전히 Homebrew를 통해 PHP 8.0 이상 버전을 설치해야 합니다. Valet은 주 연결 버전이 아니더라도, 일부 스크립트 실행에 이 버전을 사용합니다.

<!-- </div> -->
</div>

<a name="serving-sites"></a>
<!-- ## Serving Sites -->
## Serving Sites

<!-- Once Valet is installed, you're ready to start serving your Laravel applications. Valet provides two commands to help you serve your applications: `park` and `link`. -->
Valet 설치가 끝나면, Laravel 애플리케이션을 서비스할 준비가 완료됩니다. Valet에서는 애플리케이션을 서비스하기 위해 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
<!-- ### The `park` Command -->
### The `park` Command

<!-- The `park` command registers a directory on your machine that contains your applications. Once the directory has been "parked" with Valet, all of the directories within that directory will be accessible in your web browser at `http://<directory-name>.test`: -->
`park` 명령어는 사용자의 컴퓨터에 위치한 애플리케이션이 포함된 디렉터리를 등록합니다. Valet에 디렉터리를 “파킹”하면, 해당 디렉터리 내의 모든 하위 디렉터리가 웹 브라우저에서 `http://<directory-name>.test`로 접근 가능해집니다:

```shell
cd ~/Sites

valet park
```

<!-- That's all there is to it. Now, any application you create within your "parked" directory will automatically be served using the `http://<directory-name>.test` convention. So, if your parked directory contains a directory named "laravel", the application within that directory will be accessible at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard subdomains (`http://foo.laravel.test`). -->
이렇게 하면 "파킹"된 디렉터리 내에서 생성하는 모든 애플리케이션이 자동으로 `http://<directory-name>.test` 규칙에 따라 서비스됩니다. 예를 들어, 해당 디렉터리 내에 "laravel"이라는 하위 폴더가 있으면, 이 애플리케이션은 `http://laravel.test` 주소로 접근할 수 있습니다. 또한, Valet은 와일드카드 서브도메인(`http://foo.laravel.test`)을 자동으로 지원합니다.

<a name="the-link-command"></a>
<!-- ### The `link` Command -->
### The `link` Command

<!-- The `link` command can also be used to serve your Laravel applications. This command is useful if you want to serve a single site in a directory and not the entire directory: -->
`link` 명령어도 Laravel 애플리케이션을 서비스하는 데 사용할 수 있습니다. 이 명령어는 전체 디렉터리가 아닌, 단일 사이트만 서비스하고 싶을 때 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```

<!-- Once an application has been linked to Valet using the `link` command, you may access the application using its directory name. So, the site that was linked in the example above may be accessed at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard sub-domains (`http://foo.laravel.test`). -->
한 번 `link` 명령어로 애플리케이션을 등록하면, 해당 디렉터리명으로 애플리케이션에 접근할 수 있습니다. 위 예시처럼 링크된 사이트는 `http://laravel.test`로 접근 가능합니다. 마찬가지로 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 지원됩니다.

<!-- If you would like to serve the application at a different hostname, you may pass the hostname to the `link` command. For example, you may run the following command to make an application available at `http://application.test`: -->
다른 호스트명으로 애플리케이션을 서비스하고 싶다면, `link` 명령어에 호스트명을 추가로 입력하세요. 예를 들어, `http://application.test`로 사용하려면 다음 명령어를 실행하면 됩니다:

```shell
cd ~/Sites/laravel

valet link application
```

<!-- Of course, you may also serve applications on subdomains using the `link` command: -->
물론, `link` 명령어를 사용해 서브도메인 형태로도 서비스를 할 수 있습니다:

```shell
valet link api.application
```

<!-- You may execute the `links` command to display a list of all of your linked directories: -->
등록된 모든 링크 디렉터리는 `links` 명령어로 확인할 수 있습니다:

```shell
valet links
```

<!-- The `unlink` command may be used to destroy the symbolic link for a site: -->
사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용할 수 있습니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
<!-- ### Securing Sites With TLS -->
### Securing Sites With TLS

<!-- By default, Valet serves sites over HTTP. However, if you would like to serve a site over encrypted TLS using HTTP/2, you may use the `secure` command. For example, if your site is being served by Valet on the `laravel.test` domain, you should run the following command to secure it: -->
Valet은 기본적으로 HTTP를 통해 사이트를 서비스합니다. 그러나, 암호화된 TLS를 통한 HTTP/2 서비스를 원한다면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인에서 사이트를 서비스하는 경우, 다음과 같이 명령어를 실행하세요:

```shell
valet secure laravel
```

<!-- To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command. Like the `secure` command, this command accepts the hostname that you wish to unsecure: -->
사이트의 보안 설정을 해제해 일반 HTTP로 다시 전환하려면, `unsecure` 명령어를 사용할 수 있습니다. `secure` 명령어와 마찬가지로 이 명령어에도 원하는 호스트명을 입력합니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
<!-- ### Serving a Default Site -->
### Serving a Default Site

<!-- Sometimes, you may wish to configure Valet to serve a "default" site instead of a `404` when visiting an unknown `test` domain. To accomplish this, you may add a `default` option to your `~/.config/valet/config.json` configuration file containing the path to the site that should serve as your default site: -->
가끔은 알 수 없는 `test` 도메인에 접속했을 때 `404` 페이지 대신 "기본" 사이트를 서비스하고 싶을 때가 있습니다. 이를 위해, `~/.config/valet/config.json` 설정 파일에 기본 사이트로 사용할 경로를 담은 `default` 옵션을 추가하면 됩니다:

<!--     "default": "/Users/Sally/Sites/example-site", -->
    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
<!-- ### Per-Site PHP Versions -->
### Per-Site PHP Versions

<!-- By default, Valet uses your global PHP installation to serve your sites. However, if you need to support multiple PHP versions across various sites, you may use the `isolate` command to specify which PHP version a particular site should use. The `isolate` command configures Valet to use the specified PHP version for the site located in your current working directory: -->
Valet은 기본적으로 글로벌 PHP 설정을 사용해 사이트를 서비스합니다. 그러나 다양한 사이트에서 각각 다른 PHP 버전을 사용해야 할 경우, `isolate` 명령어로 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. `isolate` 명령어는 현재 작업 디렉터리 내 사이트에 대해 Valet이 지정한 PHP 버전을 사용하도록 설정합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

<!-- If your site name does not match the name of the directory that contains it, you may specify the site name using the `--site` option: -->
사이트 이름이 실제 디렉터리명과 다르다면, `--site` 옵션으로 직접 사이트명을 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

<!-- For convenience, you may use the `valet php`, `composer`, and `which-php` commands to proxy calls to the appropriate PHP CLI or tool based on the site's configured PHP version: -->
편의를 위해, 사이트에서 지정한 PHP 버전에 맞는 PHP CLI 도구나 툴을 프록시하는 `valet php`, `composer`, `which-php` 명령어도 활용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

<!-- You may execute the `isolated` command to display a list of all of your isolated sites and their PHP versions: -->
모든 격리된 사이트와 해당 PHP 버전 목록은 `isolated` 명령어로 확인할 수 있습니다:

```shell
valet isolated
```

<!-- To revert a site back to Valet's globally installed PHP version, you may invoke the `unisolate` command from the site's root directory: -->
사이트를 다시 Valet의 글로벌 PHP 버전으로 되돌리려면, 사이트 루트 디렉터리에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
<!-- ## Sharing Sites -->
## Sharing Sites

<!-- Valet includes a command to share your local sites with the world, providing an easy way to test your site on mobile devices or share it with team members and clients. -->
Valet에는 로컬 사이트를 외부에도 쉽게 공유할 수 있는 기능이 내장되어 있습니다. 이 기능을 활용하면 모바일 기기에서 사이트를 테스트하거나 팀원, 클라이언트와 사이트를 손쉽게 공유할 수 있습니다.

<!-- Out of the box, Valet supports sharing your sites via ngrok or Expose. Before sharing a site, you should update your Valet configuration using the `share-tool` command, specifying either `ngrok` or `expose`: -->
Valet 기본 설정만으로도 ngrok 또는 Expose를 이용해 사이트 공유가 가능합니다. 사이트를 공유하기 전에, `share-tool` 명령어로 `ngrok` 또는 `expose` 중 원하는 도구를 지정해 Valet 설정을 갱신하세요:

```shell
valet share-tool ngrok
```

<!-- If you choose a tool and don't have it installed via Homebrew (for ngrok) or Composer (for Expose), Valet will automatically prompt you to install it. Of course, both tools require you to authenticate your ngrok or Expose account before you can start sharing sites. -->
선택한 툴이 Homebrew(ngrok)나 Composer(Expose)로 설치되어 있지 않으면, Valet이 자동으로 설치하라고 안내합니다. 또한, 두 도구 모두 사이트 공유를 시작하기 전에 ngrok 또는 Expose 계정 인증이 필요합니다.

<!-- To share a site, navigate to the site's directory in your terminal and run Valet's `share` command. A publicly accessible URL will be placed into your clipboard and is ready to paste directly into your browser or to be shared with your team: -->
공유할 사이트의 디렉터리로 이동한 뒤, Valet의 `share` 명령어를 실행합니다. 이렇게 하면 공유용 공용 URL이 클립보드에 복사되며, 바로 브라우저나 팀원에게 전달할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

<!-- To stop sharing your site, you may press `Control + C`. -->
사이트 공유를 중단하려면 `Control + C`를 누르세요.

> [!WARNING]
> 커스텀 DNS 서버(예: `1.1.1.1`)를 사용 중이라면 ngrok 공유가 제대로 동작하지 않을 수 있습니다. 이런 경우, Mac 시스템 설정 > 네트워크 설정 > 고급 > DNS 탭에서 `127.0.0.1`을 첫 번째 DNS 서버로 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
<!-- #### Sharing Sites via Ngrok -->
#### Sharing Sites via Ngrok

<!-- Sharing your site using ngrok requires you to [create an ngrok account](https://dashboard.ngrok.com/signup) and [set up an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken). Once you have an authentication token, you can update your Valet configuration with that token: -->
ngrok으로 사이트를 공유하려면, 먼저 [create an ngrok account](https://dashboard.ngrok.com/signup) 후 [set up an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken)을 해야 합니다. 인증 토큰을 얻었다면 아래와 같이 Valet 설정에 토큰을 입력하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> `valet share --region=eu` 등과 같은 추가 ngrok 파라미터를 share 명령어에 전달할 수 있습니다. 더 자세한 정보는 [ngrok documentation](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
<!-- #### Sharing Sites via Expose -->
#### Sharing Sites via Expose

<!-- Sharing your site using Expose requires you to [create an Expose account](https://expose.dev/register) and [authenticate with Expose via your authentication token](https://expose.dev/docs/getting-started/getting-your-token). -->
Expose로 사이트를 공유하려면, [create an Expose account](https://expose.dev/register) 후 [authenticate with Expose via your authentication token](https://expose.dev/docs/getting-started/getting-your-token)을 해야 합니다.

<!-- You may consult the [Expose documentation](https://expose.dev/docs) for information regarding the additional command-line parameters it supports. -->
또한, Expose에서 지원하는 기타 커맨드라인 파라미터 등 자세한 내용은 [Expose documentation](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
<!-- ### Sharing Sites on Your Local Network -->
### Sharing Sites on Your Local Network

<!-- Valet restricts incoming traffic to the internal `127.0.0.1` interface by default so that your development machine isn't exposed to security risks from the Internet. -->
Valet은 기본적으로 외부 인터넷으로부터 개발 머신이 노출되는 보안 위험을 피하기 위해 `127.0.0.1` 인터페이스에서만 트래픽을 허용합니다.

<!-- If you wish to allow other devices on your local network to access the Valet sites on your machine via your machine's IP address (eg: `192.168.1.10/application.test`), you will need to manually edit the appropriate Nginx configuration file for that site to remove the restriction on the `listen` directive. You should remove the `127.0.0.1:` prefix on the `listen` directive for ports 80 and 443. -->
로컬 네트워크 내 다른 기기가 해당 머신의 Valet 사이트에 직접(IP 주소를 통해서, 예: `192.168.1.10/application.test`) 접속할 수 있게 하려면, 각 사이트의 Nginx 설정 파일을 수동으로 수정해야 합니다. 80번, 443번 포트의 `listen` 설정에서 `127.0.0.1:` 프리픽스를 제거하세요. 두 포트의 `listen` 설정 모두에 적용됩니다.

<!-- If you have not run `valet secure` on the project, you can open up network access for all non-HTTPS sites by editing the `/usr/local/etc/nginx/valet/valet.conf` file. However, if you're serving the project site over HTTPS (you have run `valet secure` for the site) then you should edit the `~/.config/valet/Nginx/app-name.test` file. -->
프로젝트에서 `valet secure`를 실행하지 않았다면 `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정해서 네트워크 접근을 열 수 있습니다. 만약 `valet secure`로 사이트를 HTTPS로 서비스 중이라면 `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

<!-- Once you have updated your Nginx configuration, run the `valet restart` command to apply the configuration changes. -->
Nginx 설정을 저장한 후에는 `valet restart` 명령어를 실행해 변경사항을 적용합니다.

<a name="site-specific-environment-variables"></a>
<!-- ## Site Specific Environment Variables -->
## Site Specific Environment Variables

<!-- Some applications using other frameworks may depend on server environment variables but do not provide a way for those variables to be configured within your project. Valet allows you to configure site specific environment variables by adding a `.valet-env.php` file within the root of your project. This file should return an array of site / environment variable pairs which will be added to the global `$_SERVER` array for each site specified in the array: -->
다른 프레임워크를 사용하는 일부 애플리케이션에서는 서버 환경 변수에 의존하지만, 이러한 변수를 프로젝트 내에서 직접 지정할 방법을 제공하지 않을 수 있습니다. Valet에서는 프로젝트 루트에 `.valet-env.php` 파일을 만들어 사이트별 환경 변수를 지정할 수 있습니다. 이 파일은 사이트/환경 변수 쌍을 가진 배열을 리턴해야 하며, 각 사이트에 대해 글로벌 `$_SERVER` 배열에 항목이 추가됩니다:

```
<?php

return [
    // Set $_SERVER['key'] to "value" for the laravel.test site...
    'laravel' => [
        'key' => 'value',
    ],

    // Set $_SERVER['key'] to "value" for all sites...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
<!-- ## Proxying Services -->
## Proxying Services

<!-- Sometimes you may wish to proxy a Valet domain to another service on your local machine. For example, you may occasionally need to run Valet while also running a separate site in Docker; however, Valet and Docker can't both bind to port 80 at the same time. -->
때때로 Valet 도메인을 로컬 머신의 다른 서비스로 프록시하고 싶을 때가 있습니다. 예를 들어, Docker를 실행하면서 Valet도 함께 사용하려는 경우, Valet과 Docker 모두 80번 포트를 사용할 수 없어 충돌이 발생할 수 있습니다.

<!-- To solve this, you may use the `proxy` command to generate a proxy. For example, you may proxy all traffic from `http://elasticsearch.test` to `http://127.0.0.1:9200`: -->
이럴 때 `proxy` 명령어를 활용해 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test`로 들어오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시할 수 있습니다:

```shell
# Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

<!-- You may remove a proxy using the `unproxy` command: -->
프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

<!-- You may use the `proxies` command to list all site configurations that are proxied: -->
모든 프록시 사이트 구성을 확인하려면 `proxies` 명령어를 사용합니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
<!-- ## Custom Valet Drivers -->
## Custom Valet Drivers

<!-- You can write your own Valet "driver" to serve PHP applications running on a framework or CMS that is not natively supported by Valet. When you install Valet, a `~/.config/valet/Drivers` directory is created which contains a `SampleValetDriver.php` file. This file contains a sample driver implementation to demonstrate how to write a custom driver. Writing a driver only requires you to implement three methods: `serves`, `isStaticFile`, and `frontControllerPath`. -->
Valet이 기본적으로 지원하지 않는 프레임워크나 CMS의 PHP 애플리케이션을 서비스하고자 한다면, 직접 Valet “드라이버”를 작성할 수 있습니다. Valet이 설치되면 `~/.config/valet/Drivers` 디렉터리가 생성되고, 그 안에 `SampleValetDriver.php` 파일이 포함되어 있습니다. 이 파일에는 커스텀 드라이버를 작성하는 기본 예제가 들어 있습니다. 드라이버를 작성하려면 다음 세 가지 메서드만 구현하면 됩니다: `serves`, `isStaticFile`, `frontControllerPath`.

<!-- All three methods receive the `$sitePath`, `$siteName`, and `$uri` values as their arguments. The `$sitePath` is the fully qualified path to the site being served on your machine, such as `/Users/Lisa/Sites/my-project`. The `$siteName` is the "host" / "site name" portion of the domain (`my-project`). The `$uri` is the incoming request URI (`/foo/bar`). -->
이 세 메서드는 모두 `$sitePath`, `$siteName`, `$uri` 인수를 전달받습니다. `$sitePath`는 현재 서비스 중인 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`)이고, `$siteName`은 도메인의 "호스트"/"사이트명" 부분(`my-project`), `$uri`는 요청 URI(`/foo/bar`)입니다.

<!-- Once you have completed your custom Valet driver, place it in the `~/.config/valet/Drivers` directory using the `FrameworkValetDriver.php` naming convention. For example, if you are writing a custom valet driver for WordPress, your filename should be `WordPressValetDriver.php`. -->
커스텀 Valet 드라이버 작성이 끝나면, 파일명을 `FrameworkValetDriver.php` 형태로 하여 `~/.config/valet/Drivers` 디렉터리에 추가하면 됩니다. 예를 들어 WordPress용 커스텀 드라이버를 만들 경우, 파일명은 `WordPressValetDriver.php`여야 합니다.

<!-- Let's take a look at a sample implementation of each method your custom Valet driver should implement. -->
이제 각 메서드의 샘플 구현을 살펴보겠습니다.

<a name="the-serves-method"></a>
<!-- #### The `serves` Method -->
#### The `serves` Method

<!-- The `serves` method should return `true` if your driver should handle the incoming request. Otherwise, the method should return `false`. So, within this method, you should attempt to determine if the given `$sitePath` contains a project of the type you are trying to serve. -->
`serves` 메서드에서는 해당 드라이버가 요청을 처리해야 하는지 여부를 `true` 또는 `false`로 반환해야 합니다. 따라서 이 메서드에서는 주어진 `$sitePath`에 목표 프로젝트 유형이 포함되어 있는지 확인해야 합니다.

<!-- For example, let's imagine we are writing a `WordPressValetDriver`. Our `serves` method might look something like this: -->
예를 들어, 만약 `WordPressValetDriver`를 작성중이라면 `serves` 메서드는 다음과 같이 작성할 수 있습니다:

```
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
<!-- #### The `isStaticFile` Method -->
#### The `isStaticFile` Method

<!-- The `isStaticFile` should determine if the incoming request is for a file that is "static", such as an image or a stylesheet. If the file is static, the method should return the fully qualified path to the static file on disk. If the incoming request is not for a static file, the method should return `false`: -->
`isStaticFile`은 요청이 이미지, 스타일시트 등 "정적" 파일을 대상으로 하는지 판별해야 합니다. 정적 파일일 경우, 디스크 상의 정적 파일 전체 경로를 반환하고, 그렇지 않으면 `false`를 반환합니다:

```
/**
 * Determine if the incoming request is for a static file.
 *
 * @return string|false
 */
public function isStaticFile(string $sitePath, string $siteName, string $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> [!WARNING]
> `serves` 메서드가 요청에 대해 `true`를 반환하고 URI가 `/`가 아닐 때만 `isStaticFile` 메서드가 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
<!-- #### The `frontControllerPath` Method -->
#### The `frontControllerPath` Method

<!-- The `frontControllerPath` method should return the fully qualified path to your application's "front controller", which is typically an "index.php" file or equivalent: -->
`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"(보통 "index.php" 등)의 전체 경로를 반환해야 합니다:

```
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
<!-- ### Local Drivers -->
### Local Drivers

<!-- If you would like to define a custom Valet driver for a single application, create a `LocalValetDriver.php` file in the application's root directory. Your custom driver may extend the base `ValetDriver` class or extend an existing application specific driver such as the `LaravelValetDriver`: -->
단일 애플리케이션에 대해 커스텀 Valet 드라이버를 정의하고 싶다면, 애플리케이션 루트 디렉터리에 `LocalValetDriver.php` 파일을 생성하세요. 이 드라이버는 기본 `ValetDriver` 클래스를 상속받거나, `LaravelValetDriver` 등 기존 애플리케이션별 드라이버를 상속받을 수 있습니다:

```
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
<!-- ## Other Valet Commands -->
## Other Valet Commands

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Command  | Description
------------- | -------------
`valet list` | Display a list of all Valet commands.
`valet diagnose` | Output diagnostics to aid in debugging Valet.
`valet directory-listing` | Determine directory-listing behavior. Default is "off", which renders a 404 page for directories.
`valet forget` | Run this command from a "parked" directory to remove it from the parked directory list.
`valet log` | View a list of logs which are written by Valet's services.
`valet paths` | View all of your "parked" paths.
`valet restart` | Restart the Valet daemons.
`valet start` | Start the Valet daemons.
`valet stop` | Stop the Valet daemons.
`valet trust` | Add sudoers files for Brew and Valet to allow Valet commands to be run without prompting for your password.
`valet uninstall` | Uninstall Valet: shows instructions for manual uninstall. Pass the `--force` option to aggressively delete all of Valet's resources.
-->
명령어  | 설명
------------- | -------------
`valet list` | 모든 Valet 명령어 목록을 표시합니다.
`valet diagnose` | Valet 디버깅을 위한 진단 정보를 출력합니다.
`valet directory-listing` | 디렉터리 리스트 동작 방식 확인 혹은 변경. 기본값은 "off"로, 디렉터리 접근 시 404 페이지를 반환합니다.
`valet forget` | "파킹"된 디렉터리 내에서 실행 시, 해당 디렉터리를 파킹 목록에서 제거합니다.
`valet log` | Valet 서비스가 작성한 로그 목록을 확인할 수 있습니다.
`valet paths` | 모든 "파킹"된 경로를 확인합니다.
`valet restart` | Valet 데몬을 재시작합니다.
`valet start` | Valet 데몬을 시작합니다.
`valet stop` | Valet 데몬을 중지합니다.
`valet trust` | Brew 및 Valet에 대해 sudoers 파일을 추가, 비밀번호 입력 없이 Valet 명령어를 실행할 수 있게 합니다.
`valet uninstall` | Valet을 제거합니다. 강제 삭제를 원하면 `--force` 옵션을 사용해 모든 리소스도 함께 삭제합니다.

<!-- </div> -->
</div>

<a name="valet-directories-and-files"></a>
<!-- ## Valet Directories and Files -->
## Valet Directories and Files

<!-- You may find the following directory and file information helpful while troubleshooting issues with your Valet environment: -->
Valet 환경에서 문제를 해결하려 할 때, 아래의 디렉터리 및 파일 정보를 참고할 수 있습니다:

<!-- #### `~/.config/valet` -->
#### `~/.config/valet`

<!-- Contains all of Valet's configuration. You may wish to maintain a backup of this directory. -->
Valet의 모든 설정 파일이 들어 있습니다. 이 디렉터리는 백업해 두는 것이 좋습니다.

<!-- #### `~/.config/valet/dnsmasq.d/` -->
#### `~/.config/valet/dnsmasq.d/`

<!-- This directory contains DNSMasq's configuration. -->
DNSMasq의 설정 파일이 저장되어 있습니다.

<!-- #### `~/.config/valet/Drivers/` -->
#### `~/.config/valet/Drivers/`

<!-- This directory contains Valet's drivers. Drivers determine how a particular framework / CMS is served. -->
Valet 드라이버가 저장됩니다. 드라이버는 각 프레임워크/CMS를 어떻게 서비스할지 정의합니다.

<!-- #### `~/.config/valet/Nginx/` -->
#### `~/.config/valet/Nginx/`

<!-- This directory contains all of Valet's Nginx site configurations. These files are rebuilt when running the `install` and `secure` commands. -->
Valet의 모든 Nginx 사이트 설정 파일이 저장됩니다. 이 파일들은 `install` 및 `secure` 명령어 실행 시 재생성됩니다.

<!-- #### `~/.config/valet/Sites/` -->
#### `~/.config/valet/Sites/`

<!-- This directory contains all of the symbolic links for your [linked projects](#the-link-command). -->
[linked projects](#the-link-command)의 모든 심볼릭 링크가 저장됩니다.

<!-- #### `~/.config/valet/config.json` -->
#### `~/.config/valet/config.json`

<!-- This file is Valet's master configuration file. -->
Valet의 마스터 설정 파일입니다.

<!-- #### `~/.config/valet/valet.sock` -->
#### `~/.config/valet/valet.sock`

<!-- This file is the PHP-FPM socket used by Valet's Nginx installation. This will only exist if PHP is running properly. -->
Valet의 Nginx 설치에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상적으로 실행 중일 때만 존재합니다.

<!-- #### `~/.config/valet/Log/fpm-php.www.log` -->
#### `~/.config/valet/Log/fpm-php.www.log`

<!-- This file is the user log for PHP errors. -->
PHP 에러 관련 사용자 로그입니다.

<!-- #### `~/.config/valet/Log/nginx-error.log` -->
#### `~/.config/valet/Log/nginx-error.log`

<!-- This file is the user log for Nginx errors. -->
Nginx 에러 관련 사용자 로그입니다.

<!-- #### `/usr/local/var/log/php-fpm.log` -->
#### `/usr/local/var/log/php-fpm.log`

<!-- This file is the system log for PHP-FPM errors. -->
PHP-FPM 시스템 에러 로그입니다.

<!-- #### `/usr/local/var/log/nginx` -->
#### `/usr/local/var/log/nginx`

<!-- This directory contains the Nginx access and error logs. -->
Nginx의 접근 및 에러 로그가 들어 있는 디렉터리입니다.

<!-- #### `/usr/local/etc/php/X.X/conf.d` -->
#### `/usr/local/etc/php/X.X/conf.d`

<!-- This directory contains the `*.ini` files for various PHP configuration settings. -->
여러 PHP 설정 값이 담긴 `*.ini` 파일이 있는 디렉터리입니다.

<!-- #### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf` -->
#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

<!-- This file is the PHP-FPM pool configuration file. -->
PHP-FPM 풀 설정 파일입니다.

<!-- #### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf` -->
#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

<!-- This file is the default Nginx configuration used for building SSL certificates for your sites. -->
사이트의 SSL 인증서 생성에 사용되는 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
<!-- ### Disk Access -->
### Disk Access

<!-- Since macOS 10.14, [access to some files and directories is restricted by default](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). These restrictions include the Desktop, Documents, and Downloads directories. In addition, network volume and removable volume access is restricted. Therefore, Valet recommends your site folders are located outside of these protected locations. -->
macOS 10.14부터는 [access to some files and directories is restricted by default](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)됩니다. 예를 들어, 데스크탑, Documents, Downloads 디렉터리와 네트워크/이동식 볼륨에도 제한이 적용됩니다. 따라서 Valet에서는 사이트 폴더를 이러한 보호된 위치 밖에 두는 것을 권장합니다.

<!-- However, if you wish to serve sites from within one of those locations, you will need to give Nginx "Full Disk Access". Otherwise, you may encounter server errors or other unpredictable behavior from Nginx, especially when serving static assets. Typically, macOS will automatically prompt you to grant Nginx full access to these locations. Or, you may do so manually via `System Preferences` > `Security & Privacy` > `Privacy` and selecting `Full Disk Access`. Next, enable any `nginx` entries in the main window pane. -->
하지만, 반드시 위 폴더 내에서 사이트를 서비스해야 한다면, Nginx에 “전체 디스크 접근 권한(Full Disk Access)”을 부여해야 하며, 그렇지 않으면 정적 자산 서비스 등에서 서버 오류를 겪을 수 있습니다. 일반적으로 macOS에서는 이러한 권한 필요 시 자동으로 Nginx에 접근 권한 부여를 요청하지만, 수동으로 부여하려면 `System Preferences` > `Security & Privacy` > `Privacy` 탭에서 `Full Disk Access`를 선택하고, 메인 창에서 `nginx` 항목에 체크하세요.
