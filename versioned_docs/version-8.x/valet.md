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
- [Sharing Sites](#sharing-sites)
    - [Sharing Sites Via Ngrok](#sharing-sites-via-ngrok)
    - [Sharing Sites Via Expose](#sharing-sites-via-expose)
    - [Sharing Sites On Your Local Network](#sharing-sites-on-your-local-network)
- [Site Specific Environment Variables](#site-specific-environment-variables)
- [Proxying Services](#proxying-services)
- [Custom Valet Drivers](#custom-valet-drivers)
    - [Local Drivers](#local-drivers)
- [Other Valet Commands](#other-valet-commands)
- [Valet Directories & Files](#valet-directories-and-files)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Valet](https://github.com/laravel/valet) is a development environment for macOS minimalists. Laravel Valet configures your Mac to always run [Nginx](https://www.nginx.com/) in the background when your machine starts. Then, using [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet proxies all requests on the `*.test` domain to point to sites installed on your local machine. -->
[Laravel Valet](https://github.com/laravel/valet)은 macOS 환경에서 가볍게 사용할 수 있는 개발 환경 도구입니다. Valet은 Mac이 부팅될 때마다 항상 [Nginx](https://www.nginx.com/)를 백그라운드에서 실행하도록 설정합니다. 또한, [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 이용하여 `*.test` 도메인으로 들어오는 모든 요청을 로컬에 설치된 사이트로 프록시합니다.

<!-- In other words, Valet is a blazing fast Laravel development environment that uses roughly 7 MB of RAM. Valet isn't a complete replacement for [Sail](/docs/8.x/sail) or [Homestead](/docs/8.x/homestead), but provides a great alternative if you want flexible basics, prefer extreme speed, or are working on a machine with a limited amount of RAM. -->
즉, Valet은 약 7MB의 RAM만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/8.x/sail)이나 [Homestead](/docs/8.x/homestead)를 완전히 대체하는 도구는 아니지만, 더 가볍고 빠른 개발 환경을 선호하거나 제한된 RAM을 가진 컴퓨터를 사용하는 경우 뛰어난 대안이 될 수 있습니다.

<!-- Out of the box, Valet support includes, but is not limited to: -->
처음부터 Valet이 기본적으로 지원하는 프레임워크 및 CMS는 다음과 같습니다. (아래 목록에 포함된 항목 외에도 다양한 플랫폼을 지원합니다.)

<!-- <div id="valet-support" markdown="1"> -->
<div id="valet-support" markdown="1">

<!--
- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
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
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
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
이 외에도, 자신만의 [custom drivers](#custom-valet-drivers)를 직접 만들어 Valet을 확장할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!NOTE]
> Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx와 같은 다른 프로그램이 로컬 컴퓨터의 80번 포트를 사용 중이지 않은지 확인해야 합니다.

<!-- To get started, you first need to ensure that Homebrew is up to date using the `update` command: -->
먼저, Homebrew를 최신 버전으로 업데이트해야 합니다. 터미널에서 `update` 명령어를 실행하세요.


<!--     brew update -->
    brew update


<!-- Next, you should use Homebrew to install PHP: -->
그 다음, Homebrew를 사용하여 PHP를 설치합니다.


<!--     brew install php -->
    brew install php


<!-- After installing PHP, you are ready to install the [Composer package manager](https://getcomposer.org). In addition, you should make sure the `~/.composer/vendor/bin` directory is in your system's "PATH". After Composer has been installed, you may install Laravel Valet as a global Composer package: -->
PHP를 설치한 후에는 [Composer package manager](https://getcomposer.org)를 추가로 설치해야 하며, `~/.composer/vendor/bin` 디렉터리가 시스템 "PATH"에 포함되어 있는지 확인해야 합니다. Composer를 설치한 다음, Laravel Valet을 전역 Composer 패키지로 설치합니다.

```
composer global require laravel/valet
```

<!-- Finally, you may execute Valet's `install` command. This will configure and install Valet and DnsMasq. In addition, the daemons Valet depends on will be configured to launch when your system starts: -->
마지막으로, Valet의 `install` 명령어를 실행하세요. 이 명령어는 Valet과 DnsMasq를 설치하고 설정합니다. 또한, Valet이 필요로 하는 각종 데몬을 시스템 시작 시 자동 실행되도록 설정합니다.

<!--     valet install -->
    valet install

<!-- Once Valet is installed, try pinging any `*.test` domain on your terminal using a command such as `ping foobar.test`. If Valet is installed correctly you should see this domain responding on `127.0.0.1`. -->
설치가 완료되면, 터미널에서 `ping foobar.test`와 같이 `*.test` 도메인으로 ping 테스트를 해보세요. Valet이 제대로 설치되었다면, 해당 도메인이 `127.0.0.1`로 응답하는 것을 확인할 수 있습니다.

<!-- Valet will automatically start its required services each time your machine boots. -->
Valet은 컴퓨터가 부팅될 때마다 필요로 하는 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
<!-- #### PHP Versions -->
#### PHP Versions

<!-- Valet allows you to switch PHP versions using the `valet use php@version` command. Valet will install the specified PHP version via Homebrew if it is not already installed: -->
Valet은 `valet use php@version` 명령어를 통해 PHP 버전을 쉽게 전환할 수 있습니다. 명시한 PHP 버전이 아직 설치되어 있지 않으면, Homebrew를 통해 자동으로 설치됩니다.

```
valet use php@7.2

valet use php
```

<!-- You may also create a `.valetphprc` file in the root of your project. The `.valetphprc` file should contain the PHP version the site should use: -->
또한, 프로젝트 루트에 `.valetphprc` 파일을 생성할 수도 있습니다. 이 파일에는 사이트에서 사용할 PHP 버전을 기록하면 됩니다.

<!--     php@7.2 -->
    php@7.2

<!-- Once this file has been created, you may simply execute the `valet use` command and the command will determine the site's preferred PHP version by reading the file. -->
`.valetphprc` 파일을 만든 후에는 단순히 `valet use` 명령어를 실행하면, 명령어가 이 파일을 읽어 사이트에 맞는 PHP 버전을 자동으로 적용합니다.

> [!NOTE]
> 여러 개의 PHP 버전을 설치해두었더라도, Valet은 한 번에 하나의 PHP 버전만 서비스할 수 있습니다.

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- If your application needs a database, check out [DBngin](https://dbngin.com). DBngin provides a free, all-in-one database management tool that includes MySQL, PostgreSQL, and Redis. After DBngin has been installed, you can connect to your database at `127.0.0.1` using the `root` username and an empty string for the password. -->
애플리케이션에서 데이터베이스가 필요하다면 [DBngin](https://dbngin.com)을 살펴보세요. DBngin은 MySQL, PostgreSQL, Redis 등을 모두 지원하는 무료 통합 데이터베이스 관리 도구입니다. 설치 후에는 `127.0.0.1`에 `root` 사용자명과 비밀번호 없이(빈 값) 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
<!-- #### Resetting Your Installation -->
#### Resetting Your Installation

<!-- If you are having trouble getting your Valet installation to run properly, executing the `composer global update` command followed by `valet install` will reset your installation and can solve a variety of problems. In rare cases, it may be necessary to "hard reset" Valet by executing `valet uninstall --force` followed by `valet install`. -->
Valet 설치가 정상적으로 작동하지 않는다면, `composer global update` 후 `valet install`을 차례로 실행하여 설치를 재설정해 볼 수 있습니다. 대부분의 문제는 이 방법으로 해결됩니다. 그래도 문제가 해결되지 않는 드문 경우에는, `valet uninstall --force` 와 `valet install`을 이어서 실행해 "강제 초기화"를 수행해야 할 수도 있습니다.

<a name="upgrading-valet"></a>
<!-- ### Upgrading Valet -->
### Upgrading Valet

<!-- You may update your Valet installation by executing the `composer global update` command in your terminal. After upgrading, it is good practice to run the `valet install` command so Valet can make additional upgrades to your configuration files if necessary. -->
Valet을 업그레이드하려면 터미널에서 `composer global update` 명령어를 실행하면 됩니다. 업그레이드 후에는, 필요한 경우 설정 파일의 업데이트를 위해 `valet install` 명령어를 한 번 더 실행하는 것이 좋습니다.

<a name="serving-sites"></a>
<!-- ## Serving Sites -->
## Serving Sites

<!-- Once Valet is installed, you're ready to start serving your Laravel applications. Valet provides two commands to help you serve your applications: `park` and `link`. -->
Valet을 설치했다면 이제 Laravel 애플리케이션을 서비스할 준비가 된 것입니다. Valet에서는 애플리케이션 서비스를 위해 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
<!-- ### The `park` Command -->
### The `park` Command

<!-- The `park` command registers a directory on your machine that contains your applications. Once the directory has been "parked" with Valet, all of the directories within that directory will be accessible in your web browser at `http://<directory-name>.test`: -->
`park` 명령어는 애플리케이션이 포함된 디렉터리를 등록(파킹)합니다. 일단 디렉터리를 Valet에 파킹하면, 그 하위의 모든 디렉터리는 웹 브라우저에서 `http://<directory-name>.test`와 같은 주소로 접근할 수 있게 됩니다.


```
cd ~/Sites

valet park
```


<!-- That's all there is to it. Now, any application you create within your "parked" directory will automatically be served using the `http://<directory-name>.test` convention. So, if your parked directory contains a directory named "laravel", the application within that directory will be accessible at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard subdomains (`http://foo.laravel.test`). -->
이렇게 하면 끝입니다. 이제 "파킹"된 디렉터리 내에 새로운 애플리케이션을 만들면, 즉시 `http://<directory-name>.test` 형식으로 서비스됩니다. 예를 들어 파킹된 디렉터리에 "laravel" 디렉터리가 있다면, 그 안의 애플리케이션은 `http://laravel.test`에서 접근할 수 있습니다. 또한, Valet은 와일드카드 하위 도메인(`http://foo.laravel.test`)도 자동으로 지원합니다.

<a name="the-link-command"></a>
<!-- ### The `link` Command -->
### The `link` Command

<!-- The `link` command can also be used to serve your Laravel applications. This command is useful if you want to serve a single site in a directory and not the entire directory: -->
`link` 명령어는 Laravel 애플리케이션을 한 개의 디렉터리만 서비스하고 싶을 때 유용합니다. 전체 디렉터리가 아닌, 특정 디렉터리에만 서비스를 연결할 수 있습니다.


```
cd ~/Sites/laravel

valet link
```


<!-- Once an application has been linked to Valet using the `link` command, you may access the application using its directory name. So, the site that was linked in the example above may be accessed at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard sub-domains (`http://foo.laravel.test`). -->
`link` 명령어로 애플리케이션을 Valet에 연결하면, 디렉터리 이름으로 해당 사이트에 접근할 수 있습니다. 위 예시의 경우 `http://laravel.test`에서 사이트가 열립니다. 마찬가지로, 와일드카드 하위 도메인(`http://foo.laravel.test`)도 자동 지원됩니다.

<!-- If you would like to serve the application at a different hostname, you may pass the hostname to the `link` command. For example, you may run the following command to make an application available at `http://application.test`: -->
다른 호스트명으로 사이트를 서비스하려면 `link` 명령어에 호스트명을 인자로 넘길 수 있습니다. 예를 들어, 다음 명령어로 애플리케이션을 `http://application.test`에서 이용 가능하게 할 수 있습니다.


```
cd ~/Sites/laravel

valet link application
```


<!-- You may execute the `links` command to display a list of all of your linked directories: -->
모든 링크된 디렉터리 목록을 확인하려면 `links` 명령어를 사용하세요.

<!--     valet links -->
    valet links

<!-- The `unlink` command may be used to destroy the symbolic link for a site: -->
사이트의 심볼릭 링크를 제거하려면 `unlink` 명령어를 사용합니다.


```
cd ~/Sites/laravel

valet unlink
```


<a name="securing-sites"></a>
<!-- ### Securing Sites With TLS -->
### Securing Sites With TLS

<!-- By default, Valet serves sites over HTTP. However, if you would like to serve a site over encrypted TLS using HTTP/2, you may use the `secure` command. For example, if your site is being served by Valet on the `laravel.test` domain, you should run the following command to secure it: -->
Valet은 기본적으로 사이트를 HTTP로 서비스하지만, 필요하다면 암호화된 TLS(HTTP/2)를 통해 사이트를 서비스할 수 있으며, 이때 `secure` 명령어를 사용합니다. 예를 들어 `laravel.test` 도메인을 HTTPS로 보호하려면 다음 명령어를 실행합니다.

<!--     valet secure laravel -->
    valet secure laravel

<!-- To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command. Like the `secure` command, this command accepts the hostname that you wish to unsecure: -->
사이트의 보안을 해제하고 다시 HTTP로 전환하려면 `unsecure` 명령어를 사용하면 됩니다. `secure` 명령어와 마찬가지로 이때도 해제하려는 호스트명을 인자로 전달합니다.

<!--     valet unsecure laravel -->
    valet unsecure laravel

<a name="serving-a-default-site"></a>
<!-- ### Serving A Default Site -->
### Serving A Default Site

<!-- Sometimes, you may wish to configure Valet to serve a "default" site instead of a `404` when visiting an unknown `test` domain. To accomplish this, you may add a `default` option to your `~/.config/valet/config.json` configuration file containing the path to the site that should serve as your default site: -->
가끔은, 존재하지 않는 `test` 도메인으로 접근할 때 `404` 페이지 대신 "기본" 사이트를 서비스하고 싶을 수도 있습니다. 이 경우 `~/.config/valet/config.json` 설정 파일에 `default` 옵션을 추가하여 기본으로 서비스할 사이트의 경로를 지정할 수 있습니다.

<!--     "default": "/Users/Sally/Sites/foo", -->
    "default": "/Users/Sally/Sites/foo",

<a name="sharing-sites"></a>
<!-- ## Sharing Sites -->
## Sharing Sites

<!-- Valet even includes a command to share your local sites with the world, providing an easy way to test your site on mobile devices or share it with team members and clients. -->
Valet에는 로컬 사이트를 외부에 쉽게 공유할 수 있는 명령어도 포함되어 있습니다. 이 기능을 활용하면 모바일 기기에서 테스트하거나 팀원 및 고객과 손쉽게 사이트를 공유할 수 있습니다.

<a name="sharing-sites-via-ngrok"></a>
<!-- ### Sharing Sites Via Ngrok -->
### Sharing Sites Via Ngrok

<!-- To share a site, navigate to the site's directory in your terminal and run Valet's `share` command. A publicly accessible URL will be inserted into your clipboard and is ready to paste directly into your browser or share with your team: -->
사이트를 공유하려면, 터미널에서 사이트 디렉터리로 이동해 Valet의 `share` 명령어를 실행하세요. 공개 접속이 가능한 URL이 클립보드에 복사되어 있어, 바로 웹 브라우저에 붙여넣거나 팀원과 공유할 수 있습니다.


```
cd ~/Sites/laravel

valet share
```


<!-- To stop sharing your site, you may press `Control + C`. Sharing your site using Ngrok requires you to [create an Ngrok account](https://dashboard.ngrok.com/signup) and [setup an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken). -->
사이트 공유를 중단하려면 `Control + C`를 누르세요. Ngrok을 이용해 사이트를 공유하려면 [create an Ngrok account](https://dashboard.ngrok.com/signup)과 [setup an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다.

> [!TIP]
> `valet share --region=eu`처럼 share 명령어에 추가적인 Ngrok 파라미터를 전달할 수 있습니다. 자세한 내용은 [ngrok documentation](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
<!-- ### Sharing Sites Via Expose -->
### Sharing Sites Via Expose

<!-- If you have [Expose](https://expose.dev) installed, you can share your site by navigating to the site's directory in your terminal and running the `expose` command. Consult the [Expose documentation](https://expose.dev/docs) for information regarding the additional command-line parameters it supports. After sharing the site, Expose will display the sharable URL that you may use on your other devices or amongst team members: -->
[Expose](https://expose.dev)를 설치했다면, 사이트 디렉터리로 이동한 뒤 `expose` 명령어만 실행하여 사이트를 공유할 수 있습니다. 지원하는 추가 커맨드라인 파라미터에 대한 정보는 [Expose documentation](https://expose.dev/docs)를 참고하세요. 사이트 공유를 시작하면, Expose가 공유 가능한 URL을 터미널에 표시해 줍니다. 해당 URL을 다른 기기나 팀원들과 자유롭게 이용하세요.


```
cd ~/Sites/laravel

expose
```


<!-- To stop sharing your site, you may press `Control + C`. -->
공유를 중지하려면 `Control + C`를 누르세요.

<a name="sharing-sites-on-your-local-network"></a>
<!-- ### Sharing Sites On Your Local Network -->
### Sharing Sites On Your Local Network

<!-- Valet restricts incoming traffic to the internal `127.0.0.1` interface by default so that your development machine isn't exposed to security risks from the Internet. -->
Valet은 기본적으로 외부 인터넷이 아닌 내부 `127.0.0.1` 인터페이스에서만 접근이 가능하도록 트래픽을 제한합니다. 이는 개발 머신이 외부로부터 보안 위협에 노출되지 않도록 하기 위함입니다.

<!-- If you wish to allow other devices on your local network to access the Valet sites on your machine via your machine's IP address (eg: `192.168.1.10/application.test`), you will need to manually edit the appropriate Nginx configuration file for that site to remove the restriction on the `listen` directive. You should remove the `127.0.0.1:` prefix on the `listen` directive for ports 80 and 443. -->
만약 로컬 네트워크 내의 다른 기기에서 이 머신의 Valet 사이트에 IP 주소를 통해 접근하고 싶다면(예: `192.168.1.10/application.test`), 해당 사이트의 Nginx 설정 파일에서 `listen` 지시어의 제한을 수동으로 해제해야 합니다. 즉, `listen` 지시어에서 `127.0.0.1:` 접두어를 제거하세요(80, 443 포트 모두 적용).

<!-- If you have not run `valet secure` on the project, you can open up network access for all non-HTTPS sites by editing the `/usr/local/etc/nginx/valet/valet.conf` file. However, if you're serving the project site over HTTPS (you have run `valet secure` for the site) then you should edit the `~/.config/valet/Nginx/app-name.test` file. -->
프로젝트에 대해 `valet secure`를 실행하지 않았다면, `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정하여 모든 HTTP 사이트에 대한 네트워크 접근을 열 수 있습니다. 만약 해당 프로젝트를 HTTPS로 서비스하고 있다면(`valet secure`를 실행한 경우), `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

<!-- Once you have updated your Nginx configuration, run the `valet restart` command to apply the configuration changes. -->
설정 파일을 수정했다면, `valet restart` 명령어를 실행해 변경 사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
<!-- ## Site Specific Environment Variables -->
## Site Specific Environment Variables

<!-- Some applications using other frameworks may depend on server environment variables but do not provide a way for those variables to be configured within your project. Valet allows you to configure site specific environment variables by adding a `.valet-env.php` file within the root of your project. This file should return an array of site / environment variable pairs which will be added to the global `$_SERVER` array for each site specified in the array: -->
프레임워크에 따라 일부 애플리케이션은 서버 환경 변수에 의존하지만, 프로젝트 내부에서 변수 설정 방법을 제공하지 않을 수 있습니다. Valet은 프로젝트 루트에 `.valet-env.php` 파일을 추가하여 사이트별 환경 변수를 지정할 수 있게 해줍니다. 이 파일에서 각 사이트와 환경 변수의 짝을 배열 형태로 반환하면, 해당 값들이 글로벌 `$_SERVER` 배열에 추가됩니다.

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
가끔은 Valet 도메인을 로컬 컴퓨터의 다른 서비스와 프록시 연결하고 싶을 수 있습니다. 예를 들어, Valet을 사용하면서 별도로 Docker에서 돌아가는 사이트가 있다고 합시다. 그러나 Valet과 Docker는 동시에 80번 포트를 사용할 수 없습니다.

<!-- To solve this, you may use the `proxy` command to generate a proxy. For example, you may proxy all traffic from `http://elasticsearch.test` to `http://127.0.0.1:9200`: -->
이런 경우에는 `proxy` 명령어를 사용해 프록시를 설정하면 됩니다. 예를 들어, `http://elasticsearch.test`로 들어오는 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시할 수 있습니다.

```bash
// Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

// Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

<!-- You may remove a proxy using the `unproxy` command: -->
설정한 프록시를 제거하려면 `unproxy` 명령어를 사용합니다.

<!--     valet unproxy elasticsearch -->
    valet unproxy elasticsearch

<!-- You may use the `proxies` command to list all site configurations that are proxied: -->
모든 프록시 사이트 설정 목록을 확인하려면 `proxies` 명령어를 사용하세요.

<!--     valet proxies -->
    valet proxies

<a name="custom-valet-drivers"></a>
<!-- ## Custom Valet Drivers -->
## Custom Valet Drivers

<!-- You can write your own Valet "driver" to serve PHP applications running on a framework or CMS that is not natively supported by Valet. When you install Valet, a `~/.config/valet/Drivers` directory is created which contains a `SampleValetDriver.php` file. This file contains a sample driver implementation to demonstrate how to write a custom driver. Writing a driver only requires you to implement three methods: `serves`, `isStaticFile`, and `frontControllerPath`. -->
Valet이 기본적으로 지원하지 않는 프레임워크나 CMS를 서비스하고자 한다면, 직접 Valet "드라이버"를 작성할 수 있습니다. Valet을 설치하면 `~/.config/valet/Drivers` 디렉터리에 `SampleValetDriver.php` 파일이 생성됩니다. 이 샘플 파일을 참고해 자신만의 커스텀 드라이버를 만들 수 있습니다. 드라이버를 작성하려면 총 세 가지 메서드(`serves`, `isStaticFile`, `frontControllerPath`)만 구현하면 됩니다.

<!-- All three methods receive the `$sitePath`, `$siteName`, and `$uri` values as their arguments. The `$sitePath` is the fully qualified path to the site being served on your machine, such as `/Users/Lisa/Sites/my-project`. The `$siteName` is the "host" / "site name" portion of the domain (`my-project`). The `$uri` is the incoming request URI (`/foo/bar`). -->
세 메서드는 모두 `$sitePath`, `$siteName`, `$uri` 값을 인수로 받습니다. `$sitePath`는 현재 서비스되는 사이트의 전체 경로(예: `/Users/Lisa/Sites/my-project`)이고, `$siteName`은 도메인의 "호스트"/"사이트명" 부분(`my-project`)이며, `$uri`는 들어온 요청 URI(`/foo/bar`)입니다.

<!-- Once you have completed your custom Valet driver, place it in the `~/.config/valet/Drivers` directory using the `FrameworkValetDriver.php` naming convention. For example, if you are writing a custom valet driver for WordPress, your filename should be `WordPressValetDriver.php`. -->
커스텀 드라이버를 완성했다면, `FrameworkValetDriver.php` 형식의 파일명으로 `~/.config/valet/Drivers` 디렉터리에 저장하세요. 예를 들어, WordPress용 커스텀 드라이버라면 파일명은 `WordPressValetDriver.php`가 되어야 합니다.

<!-- Let's take a look at a sample implementation of each method your custom Valet driver should implement. -->
각 메서드의 샘플 구현을 살펴보겠습니다.

<a name="the-serves-method"></a>
<!-- #### The `serves` Method -->
#### The `serves` Method

<!-- The `serves` method should return `true` if your driver should handle the incoming request. Otherwise, the method should return `false`. So, within this method, you should attempt to determine if the given `$sitePath` contains a project of the type you are trying to serve. -->
`serves` 메서드는 현재 드라이버가 해당 요청을 처리해야 할지 여부를 판단합니다. 드라이버가 해당 요청을 담당해야 한다면 `true`를, 아니라면 `false`를 반환해야 합니다. 이 메서드 안에서는 주어진 `$sitePath`가 서비스하려는 유형의 프로젝트를 포함하는지 확인해야 합니다.

<!-- For example, let's imagine we are writing a `WordPressValetDriver`. Our `serves` method might look something like this: -->
예를 들어, `WordPressValetDriver`를 작성한다면 `serves` 메서드는 다음과 같이 구현할 수 있습니다.

```
/**
 * Determine if the driver serves the request.
 *
 * @param  string  $sitePath
 * @param  string  $siteName
 * @param  string  $uri
 * @return bool
 */
public function serves($sitePath, $siteName, $uri)
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
<!-- #### The `isStaticFile` Method -->
#### The `isStaticFile` Method

<!-- The `isStaticFile` should determine if the incoming request is for a file that is "static", such as an image or a stylesheet. If the file is static, the method should return the fully qualified path to the static file on disk. If the incoming request is not for a static file, the method should return `false`: -->
`isStaticFile` 메서드는 들어온 요청이 이미지나 CSS 파일 등 "정적" 파일에 해당하는지 판단합니다. 정적 파일이라면 해당 파일의 전체 경로를 반환하고, 아니라면 `false`를 반환해야 합니다.

```
/**
 * Determine if the incoming request is for a static file.
 *
 * @param  string  $sitePath
 * @param  string  $siteName
 * @param  string  $uri
 * @return string|false
 */
public function isStaticFile($sitePath, $siteName, $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> [!NOTE]
> `isStaticFile` 메서드는 `serves` 메서드가 `true`를 반환하고, 요청한 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
<!-- #### The `frontControllerPath` Method -->
#### The `frontControllerPath` Method

<!-- The `frontControllerPath` method should return the fully qualified path to your application's "front controller", which is typically an "index.php" file or equivalent: -->
`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"(보통 "index.php"와 같은 진입점 파일)의 전체 경로를 반환해야 합니다.

```
/**
 * Get the fully resolved path to the application's front controller.
 *
 * @param  string  $sitePath
 * @param  string  $siteName
 * @param  string  $uri
 * @return string
 */
public function frontControllerPath($sitePath, $siteName, $uri)
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
<!-- ### Local Drivers -->
### Local Drivers

<!-- If you would like to define a custom Valet driver for a single application, create a `LocalValetDriver.php` file in the application's root directory. Your custom driver may extend the base `ValetDriver` class or extend an existing application specific driver such as the `LaravelValetDriver`: -->
특정 애플리케이션 한 곳에만 사용할 커스텀 Valet 드라이버를 만들고 싶다면, 해당 애플리케이션의 루트 디렉터리에 `LocalValetDriver.php` 파일을 생성하면 됩니다. 커스텀 드라이버는 기본 `ValetDriver` 클래스를 확장하거나, `LaravelValetDriver`와 같은 기존 드라이버를 확장할 수도 있습니다.

```
class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return bool
     */
    public function serves($sitePath, $siteName, $uri)
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string
     */
    public function frontControllerPath($sitePath, $siteName, $uri)
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
<!-- ## Other Valet Commands -->
## Other Valet Commands

<!--
Command  | Description
------------- | -------------
`valet forget` | Run this command from a "parked" directory to remove it from the parked directory list.
`valet log` | View a list of logs which are written by Valet's services.
`valet paths` | View all of your "parked" paths.
`valet restart` | Restart the Valet daemons.
`valet start` | Start the Valet daemons.
`valet stop` | Stop the Valet daemons.
`valet trust` | Add sudoers files for Brew and Valet to allow Valet commands to be run without prompting for your password.
`valet uninstall` | Uninstall Valet: shows instructions for manual uninstall. Pass the `--force` option to aggressively delete all of Valet's resources.
-->
Command  | 설명
------------- | -------------
`valet forget` | "파킹"된 디렉터리에서 실행하면, 해당 디렉터리를 파킹 목록에서 제거합니다.
`valet log` | Valet의 서비스와 관련된 로그 목록을 확인합니다.
`valet paths` | 현재 파킹된 모든 경로 목록을 보여줍니다.
`valet restart` | Valet 데몬을 재시작합니다.
`valet start` | Valet 데몬을 시작합니다.
`valet stop` | Valet 데몬을 중지합니다.
`valet trust` | Brew와 Valet에 대해 비밀번호 없이 명령을 실행할 수 있도록 sudoers 파일을 추가합니다.
`valet uninstall` | Valet을 완전히 제거합니다. 수동 삭제 안내를 보여줍니다. `--force` 옵션을 사용하면 Valet의 모든 리소스를 강제 삭제합니다.

<a name="valet-directories-and-files"></a>
<!-- ## Valet Directories & Files -->
## Valet Directories & Files

<!-- You may find the following directory and file information helpful while troubleshooting issues with your Valet environment: -->
Valet 환경에서 문제를 해결하거나 관리할 때 다음 디렉터리와 파일 정보를 참고하면 도움이 될 수 있습니다.

<!-- #### `~/.config/valet` -->
#### `~/.config/valet`

<!-- Contains all of Valet's configuration. You may wish to maintain a backup of this directory. -->
Valet의 모든 설정 파일이 이곳에 저장됩니다. 백업을 유지하는 것이 좋습니다.

<!-- #### `~/.config/valet/dnsmasq.d/` -->
#### `~/.config/valet/dnsmasq.d/`

<!-- This directory contains DNSMasq's configuration. -->
DnsMasq의 설정 파일이 저장된 디렉터리입니다.

<!-- #### `~/.config/valet/Drivers/` -->
#### `~/.config/valet/Drivers/`

<!-- This directory contains Valet's drivers. Drivers determine how a particular framework / CMS is served. -->
Valet 드라이버들이 있는 디렉터리입니다. 각 드라이버는 특정 프레임워크나 CMS를 어떻게 서비스할지 결정합니다.

<!-- #### `~/.config/valet/Extensions/` -->
#### `~/.config/valet/Extensions/`

<!-- This directory contains custom Valet extensions / commands. -->
커스텀 Valet 확장 기능이나 명령어가 저장됩니다.

<!-- #### `~/.config/valet/Nginx/` -->
#### `~/.config/valet/Nginx/`

<!-- This directory contains all of Valet's Nginx site configurations. These files are rebuilt when running the `install`, `secure`, and `tld` commands. -->
Valet에서 사용하는 모든 Nginx 사이트 설정 파일이 들어 있습니다. `install`, `secure`, `tld` 명령어 실행 시 이 파일들이 다시 생성됩니다.

<!-- #### `~/.config/valet/Sites/` -->
#### `~/.config/valet/Sites/`

<!-- This directory contains all of the symbolic links for your [linked projects](#the-link-command). -->
[linked projects](#the-link-command)에 대한 모든 심볼릭 링크가 저장되는 디렉터리입니다.

<!-- #### `~/.config/valet/config.json` -->
#### `~/.config/valet/config.json`

<!-- This file is Valet's master configuration file. -->
Valet의 메인 설정 파일입니다.

<!-- #### `~/.config/valet/valet.sock` -->
#### `~/.config/valet/valet.sock`

<!-- This file is the PHP-FPM socket used by Valet's Nginx installation. This will only exist if PHP is running properly. -->
Valet의 Nginx가 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상적으로 실행 중일 때만 존재합니다.

<!-- #### `~/.config/valet/Log/fpm-php.www.log` -->
#### `~/.config/valet/Log/fpm-php.www.log`

<!-- This file is the user log for PHP errors. -->
PHP 오류에 대한 사용자 로그입니다.

<!-- #### `~/.config/valet/Log/nginx-error.log` -->
#### `~/.config/valet/Log/nginx-error.log`

<!-- This file is the user log for Nginx errors. -->
Nginx 오류에 대한 사용자 로그입니다.

<!-- #### `/usr/local/var/log/php-fpm.log` -->
#### `/usr/local/var/log/php-fpm.log`

<!-- This file is the system log for PHP-FPM errors. -->
시스템 PHP-FPM 오류 로그 파일입니다.

<!-- #### `/usr/local/var/log/nginx` -->
#### `/usr/local/var/log/nginx`

<!-- This directory contains the Nginx access and error logs. -->
Nginx의 액세스 및 오류 로그 디렉터리입니다.

<!-- #### `/usr/local/etc/php/X.X/conf.d` -->
#### `/usr/local/etc/php/X.X/conf.d`

<!-- This directory contains the `*.ini` files for various PHP configuration settings. -->
다양한 PHP 설정을 위한 `*.ini` 파일이 저장되어 있습니다.

<!-- #### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf` -->
#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

<!-- This file is the PHP-FPM pool configuration file. -->
PHP-FPM 풀(pool) 설정 파일입니다.

<!-- #### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf` -->
#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

<!-- This file is the default Nginx configuration used for building SSL certificates for your sites. -->
사이트의 SSL 인증서를 생성할 때 사용하는 기본 Nginx 설정 파일입니다.
