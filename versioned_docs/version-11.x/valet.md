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
> macOS나 Windows에서 Laravel 애플리케이션을 더 쉽게 개발하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 확인해보세요. Herd는 Valet, PHP, Composer 등 Laravel 개발에 필요한 모든 것을 한 번에 제공합니다.

<!-- [Laravel Valet](https://github.com/laravel/valet) is a development environment for macOS minimalists. Laravel Valet configures your Mac to always run [Nginx](https://www.nginx.com/) in the background when your machine starts. Then, using [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet proxies all requests on the `*.test` domain to point to sites installed on your local machine. -->
[Laravel Valet](https://github.com/laravel/valet)은 macOS 환경에서 최소한의 설정만으로 사용할 수 있는 개발 환경입니다. Laravel Valet는 Mac이 부팅될 때마다 백그라운드에서 [Nginx](https://www.nginx.com/)가 항상 실행되도록 설정합니다. 그리고, [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용해 `*.test` 도메인으로 오는 모든 요청을 로컬에 설치된 사이트로 프록시합니다.

<!-- In other words, Valet is a blazing fast Laravel development environment that uses roughly 7 MB of RAM. Valet isn't a complete replacement for [Sail](/docs/11.x/sail) or [Homestead](/docs/11.x/homestead), but provides a great alternative if you want flexible basics, prefer extreme speed, or are working on a machine with a limited amount of RAM. -->
즉, Valet는 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet는 [Sail](/docs/11.x/sail)이나 [Homestead](/docs/11.x/homestead)의 완전한 대체품은 아니지만, 기본 기능이 유연하고, 매우 빠른 속도가 필요하거나 램이 제한된 컴퓨터에서 개발하고자 할 때 훌륭한 대안이 될 수 있습니다.

<!-- Out of the box, Valet support includes, but is not limited to: -->
Valet는 기본적으로 다음과 같은 다양한 프레임워크와 CMS를 지원합니다. 이 목록에 국한되지 않고 추가로 확장할 수 있습니다.



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
- 정적 HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

<!-- </div> -->
</div>

<!-- However, you may extend Valet with your own [custom drivers](#custom-valet-drivers). -->
또한, [custom drivers](#custom-valet-drivers)를 직접 만들어 Valet를 확장할 수도 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Valet는 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx와 같이 80번 포트를 사용하는 다른 프로그램이 실행되고 있지 않은지 반드시 확인하세요.

<!-- To get started, you first need to ensure that Homebrew is up to date using the `update` command: -->
먼저 Homebrew의 최신 상태를 `update` 명령어로 확인합니다.

```shell
brew update
```

<!-- Next, you should use Homebrew to install PHP: -->
그다음 Homebrew를 사용해 PHP를 설치합니다.

```shell
brew install php
```

<!-- After installing PHP, you are ready to install the [Composer package manager](https://getcomposer.org). In addition, you should make sure the `$HOME/.composer/vendor/bin` directory is in your system's "PATH". After Composer has been installed, you may install Laravel Valet as a global Composer package: -->
PHP 설치가 끝났다면, 이제 [Composer package manager](https://getcomposer.org)를 설치할 준비가 된 것입니다. 추가로, `$HOME/.composer/vendor/bin` 디렉터리가 시스템 "PATH"에 포함되어 있는지 확인해야 합니다. Composer를 설치한 후에는, Laravel Valet를 전역 Composer 패키지로 설치할 수 있습니다.

```shell
composer global require laravel/valet
```

<!-- Finally, you may execute Valet's `install` command. This will configure and install Valet and DnsMasq. In addition, the daemons Valet depends on will be configured to launch when your system starts: -->
마지막으로, Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet와 DnsMasq의 설정과 설치를 자동으로 진행해줍니다. 또한, Valet가 의존하는 데몬들이 시스템 부팅 시 자동으로 실행될 수 있도록 설정해줍니다.

```shell
valet install
```

<!-- Once Valet is installed, try pinging any `*.test` domain on your terminal using a command such as `ping foobar.test`. If Valet is installed correctly you should see this domain responding on `127.0.0.1`. -->
설치가 완료되면, 터미널에서 `ping foobar.test` 같은 명령어로 `*.test` 도메인이 응답하는지 확인해보세요. Valet가 올바르게 설치되었다면, 해당 도메인이 `127.0.0.1`로 응답하는 것을 볼 수 있습니다.

<!-- Valet will automatically start its required services each time your machine boots. -->
Valet는 매번 부팅될 때마다 필요한 서비스들을 자동으로 시작합니다.

<a name="php-versions"></a>
<!-- #### PHP Versions -->
#### PHP Versions

> [!NOTE]
> PHP의 전체 글로벌 버전을 바꾸지 않고, [command](#per-site-php-versions) `isolate`를 통해 사이트별 PHP 버전을 지정할 수 있습니다.

<!-- Valet allows you to switch PHP versions using the `valet use php@version` command. Valet will install the specified PHP version via Homebrew if it is not already installed: -->
Valet는 `valet use php@version` 명령어로 PHP 버전을 전환할 수 있습니다. 아직 설치되지 않은 특정 PHP 버전은 Homebrew를 통해 자동으로 설치됩니다.

```shell
valet use php@8.2

valet use php
```

<!-- You may also create a `.valetrc` file in the root of your project. The `.valetrc` file should contain the PHP version the site should use: -->
프로젝트 루트에 `.valetrc` 파일을 생성해, 해당 사이트에서 사용할 PHP 버전을 명시할 수도 있습니다. `.valetrc` 파일에는 해당 사이트에서 사용할 PHP 버전을 적어주면 됩니다.

```shell
php=php@8.2
```

<!-- Once this file has been created, you may simply execute the `valet use` command and the command will determine the site's preferred PHP version by reading the file. -->
이 파일이 만들어지면, `valet use` 명령어를 실행하면 Valet가 파일을 읽어 최적의 PHP 버전을 자동으로 적용해줍니다.

> [!WARNING]
> 여러 PHP 버전이 설치되어 있더라도 Valet는 한 번에 하나의 PHP 버전만 제공합니다.

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- If your application needs a database, check out [DBngin](https://dbngin.com), which provides a free, all-in-one database management tool that includes MySQL, PostgreSQL, and Redis. After DBngin has been installed, you can connect to your database at `127.0.0.1` using the `root` username and an empty string for the password. -->
애플리케이션에서 데이터베이스가 필요하다면 [DBngin](https://dbngin.com)을 추천합니다. MySQL, PostgreSQL, Redis 등 여러 데이터베이스를 포함한 무료 통합 데이터베이스 관리 도구입니다. DBngin 설치 후에는 `127.0.0.1`에서 접속할 수 있고, 사용자명은 `root`, 비밀번호는 빈 문자열을 사용하면 됩니다.

<a name="resetting-your-installation"></a>
<!-- #### Resetting Your Installation -->
#### Resetting Your Installation

<!-- If you are having trouble getting your Valet installation to run properly, executing the `composer global require laravel/valet` command followed by `valet install` will reset your installation and can solve a variety of problems. In rare cases, it may be necessary to "hard reset" Valet by executing `valet uninstall --force` followed by `valet install`. -->
Valet 설치가 제대로 동작하지 않을 때는, `composer global require laravel/valet` 명령어를 실행한 뒤, `valet install`을 다시 실행해 설치를 초기화하세요. 간혹 문제가 계속된다면, `valet uninstall --force` 명령어로 완전히 제거한 뒤, `valet install`을 다시 실행하는 것이 필요할 수 있습니다.

<a name="upgrading-valet"></a>
<!-- ### Upgrading Valet -->
### Upgrading Valet

<!-- You may update your Valet installation by executing the `composer global require laravel/valet` command in your terminal. After upgrading, it is good practice to run the `valet install` command so Valet can make additional upgrades to your configuration files if necessary. -->
터미널에서 `composer global require laravel/valet` 명령어를 실행하여 Valet를 최신 버전으로 업데이트할 수 있습니다. 업그레이드 후에는, 필요한 경우 설정 파일 추가 업그레이드를 적용하기 위해 `valet install` 명령어를 실행하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
<!-- #### Upgrading to Valet 4 -->
#### Upgrading to Valet 4

<!-- If you're upgrading from Valet 3 to Valet 4, take the following steps to properly upgrade your Valet installation: -->
Valet 3에서 Valet 4로 업그레이드하려면 아래 단계를 순서대로 진행하세요.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- If you've added `.valetphprc` files to customize your site's PHP version, rename each `.valetphprc` file to `.valetrc`. Then, prepend `php=` to the existing content of the `.valetrc` file.
- Update any custom drivers to match the namespace, extension, type-hints, and return type-hints of the new driver system. You may consult Valet's [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) as an example.
- If you use PHP 7.1 - 7.4 to serve your sites, make sure you still use Homebrew to install a version of PHP that's 8.0 or higher, as Valet will use this version, even if it's not your primary linked version, to run some of its scripts.
-->
- 사이트별 PHP 버전을 커스터마이즈하기 위해 `.valetphprc` 파일을 추가했다면, 각 `.valetphprc` 파일명을 `.valetrc`로 변경합니다. 그리고 `.valetrc` 파일의 기존 내용 앞에 `php=`를 붙여줍니다.
- 기존 커스텀 드라이버가 있다면 새로운 드라이버 시스템의 네임스페이스, 확장자, 타입힌트, 반환 타입힌트 방식에 맞게 업데이트해야 합니다. 예시는 Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)에서 참고할 수 있습니다.
- PHP 7.1~7.4 버전으로 사이트를 운영 중이라면, 여전히 Homebrew를 통해 PHP 8.0 이상의 버전을 설치해야 합니다. Valet는 본인의 주요 PHP 버전이 아니더라도 이 버전을 사용해 일부 스크립트를 실행하니 꼭 설치해두어야 합니다.

<!-- </div> -->
</div>

<a name="serving-sites"></a>
<!-- ## Serving Sites -->
## Serving Sites

<!-- Once Valet is installed, you're ready to start serving your Laravel applications. Valet provides two commands to help you serve your applications: `park` and `link`. -->
Valet를 설치했다면 Laravel 애플리케이션 제공을 바로 시작할 수 있습니다. Valet는 애플리케이션 제공을 돕기 위해 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
<!-- ### The `park` Command -->
### The `park` Command

<!-- The `park` command registers a directory on your machine that contains your applications. Once the directory has been "parked" with Valet, all of the directories within that directory will be accessible in your web browser at `http://<directory-name>.test`: -->
`park` 명령어는 여러분의 애플리케이션이 포함된 디렉터리를 등록합니다. 해당 디렉터리를 Valet에 "park"하면, 그 디렉터리 안에 있는 모든 하위 디렉터리가 웹 브라우저에서 `http://<directory-name>.test` 형식으로 접근할 수 있습니다.

```shell
cd ~/Sites

valet park
```

<!-- That's all there is to it. Now, any application you create within your "parked" directory will automatically be served using the `http://<directory-name>.test` convention. So, if your parked directory contains a directory named "laravel", the application within that directory will be accessible at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard subdomains (`http://foo.laravel.test`). -->
이제 "park"된 디렉터리 내부에 애플리케이션을 새로 만들면, 해당 애플리케이션은 자동으로 `http://<directory-name>.test` 규칙을 따라 제공됩니다. 예를 들어, park 디렉터리에 "laravel"이라는 폴더가 있으면, 그 안의 애플리케이션은 `http://laravel.test`에서 접근할 수 있습니다. 추가로, Valet는 와일드카드 서브도메인(`http://foo.laravel.test`)으로도 사이트 접근을 허용합니다.

<a name="the-link-command"></a>
<!-- ### The `link` Command -->
### The `link` Command

<!-- The `link` command can also be used to serve your Laravel applications. This command is useful if you want to serve a single site in a directory and not the entire directory: -->
`link` 명령어는 Laravel 애플리케이션을 제공하는 또 다른 방법으로, 특정 디렉터리 내 단일 사이트만 제공할 때 유용합니다.

```shell
cd ~/Sites/laravel

valet link
```

<!-- Once an application has been linked to Valet using the `link` command, you may access the application using its directory name. So, the site that was linked in the example above may be accessed at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard sub-domains (`http://foo.laravel.test`). -->
`link` 명령어로 애플리케이션을 등록하면, 해당 디렉터리 이름을 사용해 접속할 수 있습니다. 위의 예시에서는 `http://laravel.test` 주소로 접속할 수 있습니다. 역시 Valet는 와일드카드 서브 도메인(`http://foo.laravel.test`)도 지원합니다.

<!-- If you would like to serve the application at a different hostname, you may pass the hostname to the `link` command. For example, you may run the following command to make an application available at `http://application.test`: -->
다른 호스트명으로 사이트를 제공하고 싶다면, `link` 명령어에 원하는 호스트명을 함께 지정하면 됩니다. 예를 들어, `http://application.test`로 제공하려면 다음과 같이 실행합니다.

```shell
cd ~/Sites/laravel

valet link application
```

<!-- Of course, you may also serve applications on subdomains using the `link` command: -->
물론, `link` 명령어를 이용해 서브도메인 형태로 사이트를 제공할 수도 있습니다.

```shell
valet link api.application
```

<!-- You may execute the `links` command to display a list of all of your linked directories: -->
`links` 명령어를 실행하면 현재 링크된 모든 디렉터리 목록을 확인할 수 있습니다.

```shell
valet links
```

<!-- The `unlink` command may be used to destroy the symbolic link for a site: -->
특정 사이트의 심볼릭 링크를 삭제하려면 `unlink` 명령어를 사용하세요.

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
<!-- ### Securing Sites With TLS -->
### Securing Sites With TLS

<!-- By default, Valet serves sites over HTTP. However, if you would like to serve a site over encrypted TLS using HTTP/2, you may use the `secure` command. For example, if your site is being served by Valet on the `laravel.test` domain, you should run the following command to secure it: -->
Valet는 기본적으로 사이트를 HTTP로 제공합니다. 그러나, HTTPS(HTTP/2로 암호화된 TLS)를 적용하고 싶다면 `secure` 명령어를 사용하면 됩니다. 예를 들어, `laravel.test` 도메인을 Valet에서 제공 중이라면 다음과 같이 실행해 보안 설정을 적용할 수 있습니다.

```shell
valet secure laravel
```

<!-- To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command. Like the `secure` command, this command accepts the hostname that you wish to unsecure: -->
사이트에 적용된 보안을 해제하고 일반 HTTP로 다시 제공하려면 `unsecure` 명령어를 사용합니다. `secure` 명령어와 마찬가지로 이 명령어 역시 보안을 해제할 도메인명을 인자로 받습니다.

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
<!-- ### Serving a Default Site -->
### Serving a Default Site

<!-- Sometimes, you may wish to configure Valet to serve a "default" site instead of a `404` when visiting an unknown `test` domain. To accomplish this, you may add a `default` option to your `~/.config/valet/config.json` configuration file containing the path to the site that should serve as your default site: -->
알 수 없는 `test` 도메인에 접속할 때 `404` 대신 특정 "기본 사이트"를 제공하고 싶을 때가 있습니다. 이럴 경우, `~/.config/valet/config.json` 설정 파일의 `default` 옵션에 기본 사이트로 사용할 경로를 추가하면 됩니다.

<!--     "default": "/Users/Sally/Sites/example-site", -->
    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
<!-- ### Per-Site PHP Versions -->
### Per-Site PHP Versions

<!-- By default, Valet uses your global PHP installation to serve your sites. However, if you need to support multiple PHP versions across various sites, you may use the `isolate` command to specify which PHP version a particular site should use. The `isolate` command configures Valet to use the specified PHP version for the site located in your current working directory: -->
Valet는 디폴트로 시스템 전체에 설치된 글로벌 PHP를 사용하지만, 여러 사이트마다 서로 다른 PHP 버전을 사용해야 할 경우 `isolate` 명령어로 사이트별 PHP 버전을 지정할 수 있습니다. `isolate` 명령어는 현재 디렉터리에 위치한 사이트에 대해 원하는 PHP 버전을 설정해줍니다.

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

<!-- If your site name does not match the name of the directory that contains it, you may specify the site name using the `--site` option: -->
사이트 이름이 디렉터리 이름과 다를 경우, `--site` 옵션으로 명시할 수 있습니다.

```shell
valet isolate php@8.0 --site="site-name"
```

<!-- For convenience, you may use the `valet php`, `composer`, and `which-php` commands to proxy calls to the appropriate PHP CLI or tool based on the site's configured PHP version: -->
편의상 `valet php`, `composer`, `which-php` 명령어를 사용하면, 사이트에 설정된 PHP 버전에 맞춰 CLI 명령을 프록시해줍니다.

```shell
valet php
valet composer
valet which-php
```

<!-- You may execute the `isolated` command to display a list of all of your isolated sites and their PHP versions: -->
`isolated` 명령어를 실행하면 PHP 버전이 격리(isolate)된 모든 사이트 목록과 설정된 PHP 버전을 확인할 수 있습니다.

```shell
valet isolated
```

<!-- To revert a site back to Valet's globally installed PHP version, you may invoke the `unisolate` command from the site's root directory: -->
사이트를 다시 Valet의 글로벌 PHP 버전으로 되돌리려면, 사이트 루트에서 `unisolate` 명령어를 실행하면 됩니다.

```shell
valet unisolate
```

<a name="sharing-sites"></a>
<!-- ## Sharing Sites -->
## Sharing Sites

<!-- Valet includes a command to share your local sites with the world, providing an easy way to test your site on mobile devices or share it with team members and clients. -->
Valet는 여러분의 로컬 사이트를 외부에 손쉽게 공유할 수 있도록 도와주는 명령어를 제공합니다. 이를 통해 모바일 기기에서 테스트하거나, 팀원 또는 클라이언트에게 쉽게 사이트를 공유할 수 있습니다.

<!-- Out of the box, Valet supports sharing your sites via ngrok or Expose. Before sharing a site, you should update your Valet configuration using the `share-tool` command, specifying either `ngrok` or `expose`: -->
Valet는 기본적으로 ngrok 또는 Expose를 통해 사이트 공유를 지원합니다. 공유를 시작하기 전, `share-tool` 명령어로 사용할 도구를 `ngrok` 또는 `expose`로 지정해야 합니다.

```shell
valet share-tool ngrok
```

<!-- If you choose a tool and don't have it installed via Homebrew (for ngrok) or Composer (for Expose), Valet will automatically prompt you to install it. Of course, both tools require you to authenticate your ngrok or Expose account before you can start sharing sites. -->
선택한 도구가 (ngrok은 Homebrew로, Expose는 Composer로) 설치되지 않았다면 Valet가 자동으로 설치 안내를 합니다. 두 도구 모두 사이트 공유를 시작하기 전에 자신의 계정 인증이 필요합니다.

<!-- To share a site, navigate to the site's directory in your terminal and run Valet's `share` command. A publicly accessible URL will be placed into your clipboard and is ready to paste directly into your browser or to be shared with your team: -->
사이트를 공유하려면, 터미널에서 사이트 디렉터리로 이동한 다음 Valet의 `share` 명령어를 실행하세요. 그러면 손쉽게 사용할 수 있는 공개 URL이 클립보드에 복사되며, 브라우저에 붙여넣거나 팀원에게 제공할 수 있습니다.

```shell
cd ~/Sites/laravel

valet share
```

<!-- To stop sharing your site, you may press `Control + C`. -->
사이트 공유를 중지하려면 `Control + C`를 누르면 됩니다.

> [!WARNING]
> 커스텀 DNS 서버(`1.1.1.1` 등)를 사용 중이면 ngrok 공유가 제대로 작동하지 않을 수 있습니다. 이 경우, Mac 시스템 설정의 네트워크 > 고급 설정 > DNS 탭에서 DNS 서버 1순위로 `127.0.0.1`을 추가해 주세요.

<a name="sharing-sites-via-ngrok"></a>
<!-- #### Sharing Sites via Ngrok -->
#### Sharing Sites via Ngrok

<!-- Sharing your site using ngrok requires you to [create an ngrok account](https://dashboard.ngrok.com/signup) and [set up an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken). Once you have an authentication token, you can update your Valet configuration with that token: -->
ngrok로 사이트를 공유하려면 [create an ngrok account](https://dashboard.ngrok.com/signup) 및 [set up an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 토큰을 발급받았다면, 아래와 같이 Valet 설정에 토큰을 적용하세요.

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> `valet share --region=eu` 등과 같이 추가적인 ngrok 파라미터를 전달할 수도 있습니다. 자세한 내용은 [ngrok documentation](https://ngrok.com/docs)를 참조하세요.

<a name="sharing-sites-via-expose"></a>
<!-- #### Sharing Sites via Expose -->
#### Sharing Sites via Expose

<!-- Sharing your site using Expose requires you to [create an Expose account](https://expose.dev/register) and [authenticate with Expose via your authentication token](https://expose.dev/docs/getting-started/getting-your-token). -->
Expose로 사이트를 공유하려면 [create an Expose account](https://expose.dev/register) 및 [authenticate with Expose via your authentication token](https://expose.dev/docs/getting-started/getting-your-token)가 필요합니다.

<!-- You may consult the [Expose documentation](https://expose.dev/docs) for information regarding the additional command-line parameters it supports. -->
추가 명령행 옵션 등 자세한 정보는 [Expose documentation](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
<!-- ### Sharing Sites on Your Local Network -->
### Sharing Sites on Your Local Network

<!-- Valet restricts incoming traffic to the internal `127.0.0.1` interface by default so that your development machine isn't exposed to security risks from the Internet. -->
Valet는 개발 머신이 인터넷으로부터 보안 위험에 노출되지 않도록, 기본적으로 `127.0.0.1` 내부 인터페이스로 들어오는 트래픽만 허용합니다.

<!-- If you wish to allow other devices on your local network to access the Valet sites on your machine via your machine's IP address (eg: `192.168.1.10/application.test`), you will need to manually edit the appropriate Nginx configuration file for that site to remove the restriction on the `listen` directive. You should remove the `127.0.0.1:` prefix on the `listen` directive for ports 80 and 443. -->
그러나, 같은 로컬 네트워크에 연결된 다른 기기(예: `192.168.1.10/application.test`)에서 Valet 사이트에 접근하게 하려면, 해당 사이트의 Nginx 설정 파일에서 `listen` 디렉티브에 있는 `127.0.0.1:` 접두어를 제거해야 합니다. 이는 80과 443 포트의 `listen` 디렉티브 모두에 적용됩니다.

<!-- If you have not run `valet secure` on the project, you can open up network access for all non-HTTPS sites by editing the `/usr/local/etc/nginx/valet/valet.conf` file. However, if you're serving the project site over HTTPS (you have run `valet secure` for the site) then you should edit the `~/.config/valet/Nginx/app-name.test` file. -->
`valet secure`를 실행하지 않은 일반 HTTP 기반 사이트의 경우 `/usr/local/etc/nginx/valet/valet.conf` 파일에서 설정을 수정하세요. 만약 특정 사이트에 `valet secure`를 적용하여 HTTPS로 제공 중이라면, `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

<!-- Once you have updated your Nginx configuration, run the `valet restart` command to apply the configuration changes. -->
Nginx 설정을 변경한 뒤에는 `valet restart` 명령어로 변경사항을 적용합니다.

<a name="site-specific-environment-variables"></a>
<!-- ## Site Specific Environment Variables -->
## Site Specific Environment Variables

<!-- Some applications using other frameworks may depend on server environment variables but do not provide a way for those variables to be configured within your project. Valet allows you to configure site specific environment variables by adding a `.valet-env.php` file within the root of your project. This file should return an array of site / environment variable pairs which will be added to the global `$_SERVER` array for each site specified in the array: -->
다른 프레임워크를 사용하는 일부 애플리케이션은 서버 환경 변수에 의존하지만, 프로젝트 내에서 환경 변수를 직접 설정하기 어려운 경우가 있습니다. 이럴 때, 프로젝트 루트에 `.valet-env.php` 파일을 추가하면 사이트별 환경 변수를 직접 지정할 수 있습니다. 이 파일은 각 사이트/환경 변수 쌍을 배열 형태로 반환해야 하며, 지정한 값들은 사이트별로 글로벌 `$_SERVER` 배열에 추가됩니다.

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
가끔 Valet 도메인을 로컬의 다른 서비스로 프록시하고 싶을 때가 있습니다. 예를 들어, Docker에서 별도 사이트를 실행하는 등 Valet와 Docker가 동시에 80번 포트를 사용할 수 없을 때가 해당됩니다.

<!-- To solve this, you may use the `proxy` command to generate a proxy. For example, you may proxy all traffic from `http://elasticsearch.test` to `http://127.0.0.1:9200`: -->
이럴 땐, `proxy` 명령어를 사용해 프록시를 생성할 수 있습니다. 예를 들면, `http://elasticsearch.test`로 오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시할 수 있습니다.

```shell
# Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

<!-- You may remove a proxy using the `unproxy` command: -->
프록시를 삭제하려면 `unproxy` 명령어를 사용합니다.

```shell
valet unproxy elasticsearch
```

<!-- You may use the `proxies` command to list all site configurations that are proxied: -->
`proxies` 명령어를 실행하면 현재 프록시 설정된 모든 사이트 목록을 볼 수 있습니다.

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
<!-- ## Custom Valet Drivers -->
## Custom Valet Drivers

<!-- You can write your own Valet "driver" to serve PHP applications running on a framework or CMS that is not natively supported by Valet. When you install Valet, a `~/.config/valet/Drivers` directory is created which contains a `SampleValetDriver.php` file. This file contains a sample driver implementation to demonstrate how to write a custom driver. Writing a driver only requires you to implement three methods: `serves`, `isStaticFile`, and `frontControllerPath`. -->
Valet에서 기본적으로 지원하지 않는 프레임워크나 CMS(콘텐츠 관리 시스템)용 PHP 애플리케이션을 제공하고자 할 때, 직접 Valet "드라이버"를 만들 수 있습니다. Valet를 설치하면 `~/.config/valet/Drivers` 디렉터리가 생성되며, 여기에 예시 구현이 담긴 `SampleValetDriver.php` 파일이 있습니다. 사용자 정의 드라이버는 크게 세 가지 메서드만 구현하면 됩니다: `serves`, `isStaticFile`, `frontControllerPath`.

<!-- All three methods receive the `$sitePath`, `$siteName`, and `$uri` values as their arguments. The `$sitePath` is the fully qualified path to the site being served on your machine, such as `/Users/Lisa/Sites/my-project`. The `$siteName` is the "host" / "site name" portion of the domain (`my-project`). The `$uri` is the incoming request URI (`/foo/bar`). -->
이 세 메서드 모두 `$sitePath`, `$siteName`, `$uri` 값을 인수로 받습니다. `$sitePath`는 시스템 내 제공될 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`), `$siteName`은 도메인의 "호스트"/"사이트명" 부분(`my-project`), `$uri`는 요청 URI(`/foo/bar`)입니다.

<!-- Once you have completed your custom Valet driver, place it in the `~/.config/valet/Drivers` directory using the `FrameworkValetDriver.php` naming convention. For example, if you are writing a custom valet driver for WordPress, your filename should be `WordPressValetDriver.php`. -->
커스텀 드라이버를 완성했다면 해당 PHP 파일을 `~/.config/valet/Drivers` 디렉터리에 `FrameworkValetDriver.php` 형식의 파일명으로 저장하세요. 예를 들어, 워드프레스를 위한 드라이버라면 `WordPressValetDriver.php`로 저장해야 합니다.

<!-- Let's take a look at a sample implementation of each method your custom Valet driver should implement. -->
이제 각 메서드별로 어떻게 구현할 수 있는지 살펴보겠습니다.

<a name="the-serves-method"></a>
<!-- #### The `serves` Method -->
#### The `serves` Method

<!-- The `serves` method should return `true` if your driver should handle the incoming request. Otherwise, the method should return `false`. So, within this method, you should attempt to determine if the given `$sitePath` contains a project of the type you are trying to serve. -->
`serves` 메서드는 드라이버가 해당 요청을 직접 처리할지 여부를 판단해 `true` 또는 `false`를 반환합니다. 즉, 이 메서드에서 주어진 `$sitePath`가 해당 타입의 프로젝트를 포함하고 있는지를 판별해야 합니다.

<!-- For example, let's imagine we are writing a `WordPressValetDriver`. Our `serves` method might look something like this: -->
예시로, `WordPressValetDriver`를 만든다고 가정할 때, `serves` 메서드는 다음과 같이 작성할 수 있습니다.

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
`isStaticFile`은 요청이 이미지나 스타일시트 같은 "정적" 파일인지 확인해야 합니다. 정적 파일이라면 디스크 상의 전체 파일 경로를 반환하고, 아니라면 `false`를 반환합니다.

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
> `isStaticFile` 메서드는 반드시 `serves` 메서드가 `true`를 반환하고, 요청 URI가 `/`가 아닐 경우에만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
<!-- #### The `frontControllerPath` Method -->
#### The `frontControllerPath` Method

<!-- The `frontControllerPath` method should return the fully qualified path to your application's "front controller", which is typically an "index.php" file or equivalent: -->
`frontControllerPath` 메서드는 애플리케이션의 "front controller"(일반적으로 "index.php" 파일)의 전체 경로를 반환해야 합니다.

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
특정 애플리케이션에만 사용할 커스텀 Valet 드라이버를 정의하고 싶다면, 애플리케이션 루트 디렉터리에 `LocalValetDriver.php` 파일을 만들면 됩니다. 이 커스텀 드라이버는 기본 `ValetDriver` 클래스를 상속하거나, `LaravelValetDriver` 등 기존 애플리케이션용 드라이버를 확장할 수 있습니다.

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

| 명령어 | 설명 |
| --- | --- |
| `valet list` | 모든 Valet 명령어 목록을 표시합니다. |
| `valet diagnose` | Valet 문제 해결을 위한 진단 정보를 출력합니다. |
| `valet directory-listing` | 디렉터리 listing 동작 방식을 결정합니다. 기본값은 "off"이며, 디렉터리에 접근시 404 페이지가 표시됩니다. |
| `valet forget` | "park"된 디렉터리 내에서 실행하면 해당 경로를 park 목록에서 제거합니다. |
| `valet log` | Valet 서비스에서 기록한 로그들을 조회합니다. |
| `valet paths` | 등록된 모든 "park" 경로를 조회합니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | Brew와 Valet를 위한 sudoers 파일을 추가해 Valet 명령 실행 시 비밀번호 입력을 요구하지 않도록 합니다. |
| `valet uninstall` | Valet를 제거합니다. (수동 제거 방법 안내 제공) `--force` 옵션을 전달하면 Valet의 모든 리소스를 강제 삭제합니다. |

<!-- </div> -->
</div>

<a name="valet-directories-and-files"></a>
<!-- ## Valet Directories and Files -->
## Valet Directories and Files

<!-- You may find the following directory and file information helpful while troubleshooting issues with your Valet environment: -->
Valet 환경에서 문제가 발생했을 때 아래 주요 디렉터리와 파일 정보를 참고하면 도움이 됩니다.

<!-- #### `~/.config/valet` -->
#### `~/.config/valet`

<!-- Contains all of Valet's configuration. You may wish to maintain a backup of this directory. -->
Valet의 모든 설정 파일이 이 디렉터리에 있습니다. 중요한 설정이므로 백업을 권장합니다.

<!-- #### `~/.config/valet/dnsmasq.d/` -->
#### `~/.config/valet/dnsmasq.d/`

<!-- This directory contains DNSMasq's configuration. -->
DnsMasq의 설정 파일이 저장되어 있습니다.

<!-- #### `~/.config/valet/Drivers/` -->
#### `~/.config/valet/Drivers/`

<!-- This directory contains Valet's drivers. Drivers determine how a particular framework / CMS is served. -->
Valet에서 사용하는 드라이버가 담겨있는 디렉터리입니다. 각 프레임워크/CMS 제공 방식을 이곳에서 정의합니다.

<!-- #### `~/.config/valet/Nginx/` -->
#### `~/.config/valet/Nginx/`

<!-- This directory contains all of Valet's Nginx site configurations. These files are rebuilt when running the `install` and `secure` commands. -->
모든 Valet Nginx 사이트 설정이 여기에 저장됩니다. `install`이나 `secure` 명령을 실행할 때마다 이 파일들이 새로 생성됩니다.

<!-- #### `~/.config/valet/Sites/` -->
#### `~/.config/valet/Sites/`

<!-- This directory contains all of the symbolic links for your [linked projects](#the-link-command). -->
[linked projects](#the-link-command)에 대한 심볼릭 링크가 여기에 저장됩니다.

<!-- #### `~/.config/valet/config.json` -->
#### `~/.config/valet/config.json`

<!-- This file is Valet's master configuration file. -->
Valet의 주요 설정이 담긴 마스터 설정 파일입니다.

<!-- #### `~/.config/valet/valet.sock` -->
#### `~/.config/valet/valet.sock`

<!-- This file is the PHP-FPM socket used by Valet's Nginx installation. This will only exist if PHP is running properly. -->
Valet의 Nginx 설치에서 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 실행 중일 때만 존재합니다.

<!-- #### `~/.config/valet/Log/fpm-php.www.log` -->
#### `~/.config/valet/Log/fpm-php.www.log`

<!-- This file is the user log for PHP errors. -->
PHP 오류에 대한 사용자 로그 파일입니다.

<!-- #### `~/.config/valet/Log/nginx-error.log` -->
#### `~/.config/valet/Log/nginx-error.log`

<!-- This file is the user log for Nginx errors. -->
Nginx 오류에 대한 사용자 로그 파일입니다.

<!-- #### `/usr/local/var/log/php-fpm.log` -->
#### `/usr/local/var/log/php-fpm.log`

<!-- This file is the system log for PHP-FPM errors. -->
시스템 전체 PHP-FPM 오류 로그 파일입니다.

<!-- #### `/usr/local/var/log/nginx` -->
#### `/usr/local/var/log/nginx`

<!-- This directory contains the Nginx access and error logs. -->
Nginx의 접근 로그 및 오류 로그가 저장됩니다.

<!-- #### `/usr/local/etc/php/X.X/conf.d` -->
#### `/usr/local/etc/php/X.X/conf.d`

<!-- This directory contains the `*.ini` files for various PHP configuration settings. -->
여러 PHP 설정을 위한 `*.ini` 파일이 위치한 디렉터리입니다.

<!-- #### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf` -->
#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

<!-- This file is the PHP-FPM pool configuration file. -->
PHP-FPM 풀 설정 파일입니다.

<!-- #### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf` -->
#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

<!-- This file is the default Nginx configuration used for building SSL certificates for your sites. -->
사이트의 SSL 인증서 생성을 위한 기본 Nginx 설정 파일입니다.

<a name="disk-access"></a>
<!-- ### Disk Access -->
### Disk Access

<!-- Since macOS 10.14, [access to some files and directories is restricted by default](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). These restrictions include the Desktop, Documents, and Downloads directories. In addition, network volume and removable volume access is restricted. Therefore, Valet recommends your site folders are located outside of these protected locations. -->
macOS 10.14부터는 [access to some files and directories is restricted by default](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). 데스크톱, 문서, 다운로드 폴더 등이 이에 해당하며, 네트워크 및 이동식 볼륨 접근도 제한됩니다. 따라서 Valet에서는 사이트 폴더를 이러한 보호된 위치 밖에 두는 것을 권장합니다.

<!-- However, if you wish to serve sites from within one of those locations, you will need to give Nginx "Full Disk Access". Otherwise, you may encounter server errors or other unpredictable behavior from Nginx, especially when serving static assets. Typically, macOS will automatically prompt you to grant Nginx full access to these locations. Or, you may do so manually via `System Preferences` > `Security & Privacy` > `Privacy` and selecting `Full Disk Access`. Next, enable any `nginx` entries in the main window pane. -->
만약 해당 위치에서 사이트를 제공하려면, Nginx에 "전체 디스크 접근 권한(Full Disk Access)"을 부여해야 합니다. 그렇지 않으면 Nginx가 정적 리소스를 제공하지 못하거나 서버 오류 등 예기치 못한 문제가 발생할 수 있습니다. 일반적으로 macOS에서 해당 폴더에 처음 접근할 때 권한 승인을 요청하지만, 수동으로도 설정할 수 있습니다. `System Preferences` > `Security & Privacy` > `Privacy`에서 `Full Disk Access`를 선택한 뒤, 메인 목록에서 `nginx` 항목을 활성화하세요.
