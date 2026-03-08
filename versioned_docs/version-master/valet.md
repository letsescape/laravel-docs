# Laravel Valet (Laravel Valet)

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 제공](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보안 적용](#securing-sites)
    - [기본 사이트 제공](#serving-a-default-site)
    - [사이트별 PHP 버전](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [사용자 정의 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉터리 및 파일](#valet-directories-and-files)
    - [디스크 접근 권한](#disk-access)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> macOS 또는 Windows에서 Laravel 애플리케이션을 더 쉽게 개발할 방법을 찾고 계신가요? [Laravel Herd](https://herd.laravel.com)를 확인해 보세요. Herd에는 Laravel 개발을 시작하는 데 필요한 모든 요소(Valet, PHP, Composer 등)가 포함되어 있습니다.

[Laravel Valet](https://github.com/laravel/valet)은 최소한의 설정을 선호하는 macOS 사용자를 위한 개발 환경입니다. Laravel Valet은 Mac이 부팅될 때 항상 백그라운드에서 [Nginx](https://www.nginx.com/)를 실행하도록 설정합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해, `*.test` 도메인에 들어오는 모든 요청을 여러분의 로컬 머신에 설치된 사이트로 프록시합니다.

즉, Valet은 약 7MB의 메모리만 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet은 [Sail](/docs/master/sail)이나 [Homestead](/docs/master/homestead)를 완전히 대체하는 것은 아니지만, 기본적인 기능만 유연하게 원하거나 빠른 속도가 필요하거나, 메모리 용량이 제한된 머신에서 작업하는 경우 훌륭한 대안이 될 수 있습니다.

Valet은 기본적으로 아래와 같은 다양한 프레임워크 및 툴을 지원합니다(단, 이에 국한되지 않습니다):

<div id="valet-support" markdown="1">

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

</div>

추가로, 직접 [사용자 정의 드라이버](#custom-valet-drivers)를 만들어 Valet을 확장할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Valet은 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx 같은 다른 프로그램이 로컬 머신의 80번 포트를 사용 중이지 않은지 꼭 확인하세요.

먼저, Homebrew가 최신 상태인지 `update` 명령어로 확인해야 합니다:

```shell
brew update
```

다음으로, Homebrew를 사용해 PHP를 설치합니다:

```shell
brew install php
```

PHP 설치가 완료되면, [Composer 패키지 매니저](https://getcomposer.org)를 설치하세요. 또한 `$HOME/.composer/vendor/bin` 디렉터리가 시스템의 "PATH"에 포함되어 있는지 확인해야 합니다. Composer 설치 후, Laravel Valet을 전역 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로, Valet의 `install` 명령어를 실행합니다. 이 명령어는 Valet과 DnsMasq를 설정 및 설치합니다. 또한, Valet이 동작하는 데 필요한 데몬들이 시스템 시작 시 자동으로 실행되도록 설정합니다:

```shell
valet install
```

Valet이 설치되면, 터미널에서 `ping foobar.test`와 같은 명령어로 `*.test` 도메인을 핑해 보세요. Valet이 제대로 설치되었다면 해당 도메인이 `127.0.0.1`에서 응답하는 것을 볼 수 있습니다.

Valet은 필요한 서비스를 매번 Mac이 부팅될 때 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]
> 전역 PHP 버전을 직접 변경하지 않아도, [`isolate` 명령어](#per-site-php-versions)로 사이트별로 PHP 버전을 지정할 수 있습니다.

Valet에서는 `valet use php@version` 명령어로 PHP 버전을 전환할 수 있습니다. 명시한 PHP 버전이 아직 설치되지 않았다면, Homebrew를 통해 자동으로 설치됩니다:

```shell
valet use php@8.2

valet use php
```

또한, 프로젝트 루트에 `.valetrc` 파일을 생성하여 사이트별 PHP 버전을 지정할 수 있습니다. `.valetrc` 파일에는 해당 사이트가 사용할 PHP 버전을 아래와 같이 적습니다:

```shell
php=php@8.2
```

이 파일이 생성된 이후에는 `valet use` 명령어를 실행하면, 해당 파일을 읽어 사이트별로 알맞은 PHP 버전을 자동으로 적용합니다.

> [!WARNING]
> 여러 버전의 PHP가 설치되어 있어도, Valet은 한 번에 오직 하나의 PHP 버전만 제공합니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요하다면 [DBngin](https://dbngin.com)을 추천합니다. 이 툴은 MySQL, PostgreSQL, Redis를 지원하는 무료 통합 데이터베이스 관리 도구입니다. DBngin을 설치한 후에는 `127.0.0.1` 주소, 사용자명 `root`, 비밀번호는 빈 문자열로 데이터베이스에 접속할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet이 제대로 동작하지 않을 때는, `composer global require laravel/valet`와 `valet install` 명령어를 차례대로 실행해 설치를 초기화하면 대부분의 문제를 해결할 수 있습니다. 아주 드물게는, `valet uninstall --force` 후 `valet install`을 실행해 "하드 리셋"이 필요할 때도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드 (Upgrading Valet)

터미널에서 `composer global require laravel/valet` 명령어를 실행하면 Valet을 최신 버전으로 업그레이드할 수 있습니다. 업그레이드 후에는 `valet install` 명령어를 실행해 필요한 추가 설정을 적용하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4로 업그레이드

Valet 3에서 Valet 4로 업그레이드하려면 아래 단계를 따라하세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 변경하려고 `.valetphprc` 파일을 사용 중이라면, 각각의 `.valetphprc` 파일을 `.valetrc`로 이름을 변경해야 합니다. 그리고 `.valetrc` 파일의 기존 내용 앞에 `php=`를 추가하세요.
- 사용자 정의 드라이버가 있다면 네임스페이스, 확장자, 타입 힌트, 반환 타입 힌트가 새 드라이버 시스템과 일치하는지 업데이트하세요. [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) 예시를 참고할 수 있습니다.
- PHP 7.1~7.4 버전으로 사이트를 제공 중이라면 Homebrew에서 PHP 8.0 이상 버전도 반드시 설치되어 있는지 확인하세요. Valet이 일부 스크립트를 실행할 때 이 버전을 사용합니다(기본 링크 버전이 아니어도 됨).

</div>

<a name="serving-sites"></a>
## 사이트 제공 (Serving Sites)

Valet 설치가 완료되면 Laravel 애플리케이션을 바로 제공할 수 있습니다. Valet은 애플리케이션을 제공할 때 `park`와 `link` 두 가지 명령어를 제공합니다.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 여러분의 애플리케이션이 포함된 디렉터리를 등록합니다. 디렉터리를 Valet로 "주차(park)"하면 그 하위의 모든 디렉터리를 `http://<디렉터리명>.test` 형태로 브라우저에서 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```

이제 "park"된 디렉터리 내에서 앱을 새로 만들어도 자동으로 `http://<디렉터리명>.test` 형태로 제공됩니다. 예를 들어 "park"된 디렉터리에 "laravel"이란 디렉터리가 있다면, 그 안의 애플리케이션은 `http://laravel.test`에서 바로 접근 가능합니다. Valet은 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 지원합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 단일 디렉터리 내에 있는 Laravel 애플리케이션만 제공하고 싶을 때 사용합니다:

```shell
cd ~/Sites/laravel

valet link
```

`link` 명령어로 한 번 등록한 후에는 해당 디렉터리 이름으로 애플리케이션에 접근할 수 있습니다. 위 예시에서는 `http://laravel.test`로 접근 가능합니다. 또한, Valet은 와일드카드 서브 도메인(`http://foo.laravel.test`)도 자동 제공됩니다.

만약 다른 호스트명으로 사이트를 제공하고 싶다면, 이름을 인수로 전달할 수 있습니다. 예를 들어 `http://application.test` 라는 도메인을 사용하려면 다음과 같이 합니다:

```shell
cd ~/Sites/laravel

valet link application
```

또한 서브도메인으로도 등록할 수 있습니다:

```shell
valet link api.application
```

등록된 모든 디렉터리는 `links` 명령어로 확인할 수 있습니다:

```shell
valet links
```

사이트에 대한 심볼릭 링크를 삭제하려면 `unlink` 명령어를 사용하세요:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안 적용 (Securing Sites With TLS)

기본적으로 Valet은 HTTP로 사이트를 제공합니다. 하지만, HTTP/2를 사용하는 암호화된 TLS(HTTPS)로 제공하려면 `secure` 명령어를 사용할 수 있습니다. 예를 들어, `laravel.test` 도메인을 보안 적용하려면 아래와 같이 실행합니다:

```shell
valet secure laravel
```

사이트의 보안을 해제하고 일반 HTTP로 다시 제공하려면 `unsecure` 명령어를 사용합니다. 이때 해제할 호스트명을 인수로 전달합니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공 (Serving a Default Site)

알 수 없는 `test` 도메인에 접속 시 `404` 페이지 대신 "기본(default)" 사이트를 제공하고 싶을 때가 있습니다. 이 경우 `~/.config/valet/config.json` 파일에 기본 사이트의 경로를 나타내는 `default` 옵션을 추가하면 됩니다:

```
"default": "/Users/Sally/Sites/example-site",
```

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전 (Per-Site PHP Versions)

기본적으로 Valet은 전역 PHP 설치를 사용해 사이트를 제공합니다. 여러 사이트에서 다양한 PHP 버전을 사용할 필요가 있다면, `isolate` 명령어로 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. `isolate` 명령어는 현재 디렉터리의 사이트에 선택한 PHP 버전을 적용합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름과 디렉터리 이름이 다를 경우 `--site` 옵션으로 명확히 지정해 줄 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

편리하게도, `valet php`, `valet composer`, `valet which-php` 명령어로 해당 사이트 설정에 맞는 PHP CLI나 도구를 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

`isolated` 명령어로, 사이트별로 어떤 PHP 버전이 적용되어 있는지 목록을 볼 수 있습니다:

```shell
valet isolated
```

사이트를 다시 전역 PHP 버전으로 돌리려면 해당 사이트의 루트 디렉터리에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet에는 로컬 사이트를 외부에 공개할 수 있도록 도와주는 명령어가 포함되어 있습니다. 이 기능으로 모바일 기기에서 테스트하거나 팀원 혹은 클라이언트와 쉽게 공유할 수 있습니다.

기본적으로 Valet은 ngrok 또는 Expose를 이용한 사이트 공유를 지원합니다. 사이트를 공유하기 전에 `share-tool` 명령어로 사용할 도구(`ngrok`, `expose`, `cloudflared`)를 지정해야 합니다:

```shell
valet share-tool ngrok
```

선택한 도구가 Homebrew(ngrok, cloudflared)나 Composer(Expose)로 미설치된 경우, Valet이 자동으로 설치 안내를 표시합니다. 물론, 모든 도구는 공유 전에 ngrok 또는 Expose 계정 인증이 필요합니다.

사이트를 공유하려면, 터미널에서 해당 사이트 디렉터리로 이동해 Valet의 `share` 명령어를 실행합니다. 공개된 URL이 클립보드에 자동 복사되며, 바로 브라우저에 접속하거나 동료와 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중지하려면 `Control + C`를 누르면 됩니다.

> [!WARNING]
> 만약 커스텀 DNS 서버(예: `1.1.1.1`)를 사용 중이라면 ngrok 공유가 정상적으로 동작하지 않을 수 있습니다. 이 때는 Mac 시스템 환경설정에서 네트워크 -> 고급 -> DNS 탭으로 이동해, 첫 번째 DNS 서버로 `127.0.0.1`을 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok으로 사이트 공유

ngrok으로 사이트를 공유하려면 반드시 [ngrok 계정](https://dashboard.ngrok.com/signup)을 만들고, [인증 토큰](https://dashboard.ngrok.com/get-started/your-authtoken)을 발급받아야 합니다. 인증 토큰을 받으면 아래와 같이 Valet 설정에 적용할 수 있습니다:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> `valet share --region=eu` 등 추가 ngrok 매개변수를 share 명령어에 전달할 수 있습니다. 더 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose로 사이트 공유

Expose로 사이트를 공유하려면 [Expose 계정](https://expose.dev/register)을 생성하고, [Expose 인증 토큰](https://expose.dev/docs/getting-started/getting-your-token)으로 인증해야 합니다.

지원하는 추가 커맨드라인 파라미터 등 상세 설명은 [Expose 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet은 기본적으로 개발 머신이 인터넷 보안 위협에 노출되지 않도록, 내부 `127.0.0.1` 인터페이스로만 요청을 허용합니다.

다른 장치(예: `192.168.1.10/application.test`와 같은 IP)에서 Valet 사이트에 접속하려면, 해당 사이트의 Nginx 설정 파일에서 `listen` 지시문의 `127.0.0.1:` 접두어를 삭제해 제한을 해제해야 합니다.(80/443 포트 적용)

HTTPS를 활성화하지 않았다면 `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정해 비HTTPS 사이트 전체 접근을 허용할 수 있습니다. 만약 사이트가 HTTPS(즉, `valet secure` 사용)라면, `~/.config/valet/Nginx/app-name.test` 파일을 수정해야 합니다.

Nginx 설정 파일을 수정한 뒤에는 `valet restart`로 변경사항을 적용하세요.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수 (Site Specific Environment Variables)

다른 프레임워크를 사용하는 애플리케이션 중에는 서버 환경 변수에 의존하지만 프로젝트 내부에서 환경 변수를 설정할 수 없는 경우도 있습니다. 이런 경우 Valet에서는 프로젝트 루트에 `.valet-env.php` 파일을 만들어 사이트별 환경 변수를 지정할 수 있습니다. 이 파일은 사이트/환경 변수 쌍의 배열을 리턴해야 하며, 배열에 지정된 각 사이트에 대해 글로벌 `$_SERVER` 배열에 자동으로 추가됩니다:

```php
<?php

return [
    // laravel.test 사이트에 대해 $_SERVER['key']를 "value"로 지정합니다...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에 대해 $_SERVER['key']를 "value"로 지정합니다...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시 (Proxying Services)

가끔 Valet 도메인을 로컬 머신 내의 다른 서비스로 프록시해야 할 때가 있습니다. 예를 들어, Docker로 별도의 사이트를 실행하면서 Valet도 동시에 사용해야 할 때 둘 다 80번 포트를 사용할 수 없으므로 충돌이 발생할 수 있습니다.

이럴 때는 `proxy` 명령어로 프록시를 설정할 수 있습니다. 예를 들어, `http://elasticsearch.test`로 들어온 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면 아래와 같이 합니다:

```shell
# HTTP로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2로 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

프록시를 제거하려면 `unproxy` 명령어를 사용하세요:

```shell
valet unproxy elasticsearch
```

프록시 설정 목록을 확인하려면 `proxies` 명령어를 사용할 수 있습니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 사용자 정의 Valet 드라이버 (Custom Valet Drivers)

Valet에서 기본적으로 지원하지 않는 프레임워크나 CMS를 지원하려면, 직접 Valet "드라이버"를 작성할 수 있습니다. Valet을 설치하면 `~/.config/valet/Drivers` 디렉터리가 만들어지고, 그 안에 `SampleValetDriver.php` 예시 파일이 들어 있습니다. 드라이버 작성 시 구현할 주요 메서드는 `serves`, `isStaticFile`, `frontControllerPath` 3가지입니다.

이 세 메서드의 인자로는 `$sitePath`, `$siteName`, `$uri`가 전달됩니다. `$sitePath`는 머신에서 제공할 사이트의 전체 경로(`/Users/Lisa/Sites/my-project` 등), `$siteName`은 도메인의 호스트/사이트명(`my-project`), `$uri`는 요청 URI(`/foo/bar`)입니다.

커스텀 드라이버를 완성하면, 파일명을 `FrameworkValetDriver.php` 형식(예: WordPress라면 `WordPressValetDriver.php`)으로 하여 `~/.config/valet/Drivers` 디렉터리에 저장하세요.

각 메서드가 어떤 식으로 구현되는지 샘플을 통해 알아보겠습니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 이 드라이버가 해당 요청을 처리해야 할지 결정합니다. 처리 대상이면 `true`, 아니면 `false`를 반환하세요. 이 메서드에서는 주어진 `$sitePath` 하위에 여러분이 지원하려는 타입의 프로젝트가 있는지 판단하면 됩니다.

예를 들어, `WordPressValetDriver`를 만든다면 아래처럼 구현할 수 있습니다.

```php
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 메서드

`isStaticFile` 메서드는 요청이 이미지나 CSS 등 "정적" 파일을 위한 것인지 확인합니다. 정적 파일일 경우, 디스크 상의 전체 파일 경로를 반환해야 합니다. 정적 파일이 아니라면 `false`를 반환하세요:

```php
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
> `isStaticFile` 메서드는 `serves`가 `true`를 반환하고, 요청 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러" (보통 `index.php` 파일)의 전체 경로를 반환해야 합니다:

```php
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### 로컬 드라이버 (Local Drivers)

단일 애플리케이션에만 적용되는 사용자 정의 Valet 드라이버를 만들고 싶다면, 해당 애플리케이션 루트에 `LocalValetDriver.php` 파일을 생성하세요. 이 파일에서 기본 `ValetDriver` 클래스를 상속하거나, 이미 존재하는 특정 애플리케이션용 드라이버(예: `LaravelValetDriver`)를 상속할 수 있습니다:

```php
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
## 기타 Valet 명령어 (Other Valet Commands)

<div class="overflow-auto">

| 명령어 | 설명 |
| --- | --- |
| `valet list` | 모든 Valet 명령어 목록을 표시합니다. |
| `valet diagnose` | Valet의 문제 해결을 위한 진단 정보를 출력합니다. |
| `valet directory-listing` | 디렉터리 목록 표시 동작을 설정합니다. 기본값은 "off"로, 디렉터리에 접근 시 404 페이지가 나타납니다. |
| `valet forget` | "park"된 디렉터리에서 실행해, park 디렉터리 목록에서 제거합니다. |
| `valet log` | Valet 서비스가 기록한 로그 목록을 확인합니다. |
| `valet paths` | "park"된 경로를 모두 확인합니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | Brew 및 Valet 명령어를 암호 입력 없이 실행할 수 있도록 sudoers 파일을 추가합니다. |
| `valet uninstall` | Valet을 제거합니다. 수동 삭제 방법도 안내합니다. `--force` 옵션을 주면 Valet의 모든 파일을 강제로 삭제합니다. |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉터리 및 파일 (Valet Directories and Files)

Valet 환경에서 문제를 해결할 때 참고할 수 있는 주요 디렉터리 및 파일 정보입니다:

#### `~/.config/valet`

Valet의 모든 설정이 이 디렉터리에 저장됩니다. 백업이 권장됩니다.

#### `~/.config/valet/dnsmasq.d/`

DNSMasq 설정 파일들이 들어 있습니다.

#### `~/.config/valet/Drivers/`

Valet의 드라이버가 저장되는 디렉터리입니다. 각 프레임워크/CMS의 제공 방식을 결정합니다.

#### `~/.config/valet/Nginx/`

Valet이 관리하는 모든 Nginx 사이트 설정 파일이 이곳에 저장됩니다. `install` 및 `secure` 명령어를 실행할 때마다 파일이 다시 생성됩니다.

#### `~/.config/valet/Sites/`

[링크된 프로젝트](#the-link-command)의 심볼릭 링크가 이 디렉터리에 저장됩니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

PHP-FPM용 소켓으로, Valet의 Nginx가 PHP와 연동하기위해 사용합니다. PHP가 정상 실행 중인 경우에만 이 파일이 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 오류에 대한 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 오류에 대한 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

PHP-FPM 오류에 대한 시스템 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx의 접근 로그 및 오류 로그가 저장되는 디렉터리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

다양한 PHP 설정(`*.ini` 파일들)이 들어 있습니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 프로세스 풀 설정 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트용 SSL 인증서 생성을 위한 기본 Nginx 설정파일입니다.

<a name="disk-access"></a>
### 디스크 접근 권한 (Disk Access)

macOS 10.14부터 [일부 파일 및 디렉터리에 대한 접근이 기본적으로 제한됩니다](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). 이 제한에는 데스크탑, 도큐먼트, 다운로드 디렉터리 등이 포함되며, 네트워크 볼륨이나 외장 드라이브 접근도 제한됩니다. 따라서, Valet 사이트 폴더는 이러한 보호된 위치 밖에 두는 것이 좋습니다.

만약 반드시 보호된 위치 내에서 사이트를 제공해야 한다면, Nginx에 "전체 디스크 접근 권한"을 부여해야 합니다. 그렇지 않으면 서버 오류나 정적 파일 제공 문제 등 예기치 않은 현상이 발생할 수 있습니다. 보통 macOS에서 자동으로 권한 요청 안내가 뜨지만, `시스템 환경설정` > `보안 및 개인정보 보호` > `개인정보`에서 `Full Disk Access(전체 디스크 접근)` 항목에 `nginx`를 수동으로 추가/활성화할 수도 있습니다.