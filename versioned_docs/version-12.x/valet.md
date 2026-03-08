# Laravel Valet

- [소개](#introduction)
- [설치](#installation)
    - [Valet 업그레이드](#upgrading-valet)
- [사이트 제공](#serving-sites)
    - [`park` 명령어](#the-park-command)
    - [`link` 명령어](#the-link-command)
    - [TLS로 사이트 보안](#securing-sites)
    - [기본 사이트 제공](#serving-a-default-site)
    - [사이트별 PHP 버전](#per-site-php-versions)
- [사이트 공유](#sharing-sites)
    - [로컬 네트워크에서 사이트 공유](#sharing-sites-on-your-local-network)
- [사이트별 환경 변수](#site-specific-environment-variables)
- [서비스 프록시](#proxying-services)
- [커스텀 Valet 드라이버](#custom-valet-drivers)
    - [로컬 드라이버](#local-drivers)
- [기타 Valet 명령어](#other-valet-commands)
- [Valet 디렉토리와 파일](#valet-directories-and-files)
    - [디스크 접근](#disk-access)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> macOS 또는 Windows에서 Laravel 애플리케이션을 더 쉽게 개발하고 싶으신가요? [Laravel Herd](https://herd.laravel.com)를 확인해보세요. Herd는 Valet, PHP, Composer 등을 포함하여 Laravel 개발에 필요한 모든 것을 제공합니다.

[Laravel Valet](https://github.com/laravel/valet)는 macOS 사용자 중 최소한의 개발 환경을 선호하는 개발자들을 위한 개발 환경입니다. Laravel Valet는 mac을 설정하여 컴퓨터가 시작될 때 항상 [Nginx](https://www.nginx.com/)가 백그라운드에서 실행되도록 구성합니다. 그리고 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq)를 사용해 `*.test` 도메인에 대한 모든 요청을 로컬 컴퓨터에 설치된 사이트로 프록시합니다.

즉, Valet는 약 7MB의 RAM만을 사용하며 매우 빠른 Laravel 개발 환경을 제공합니다. Valet는 [Sail](/docs/12.x/sail) 또는 [Homestead](/docs/12.x/homestead)를 완전히 대체하지는 않지만, 기본 기능이 유연하고 극도의 속도를 원하거나 RAM이 제한된 머신에서 작업할 때 좋은 대안이 됩니다.

기본적으로 Valet가 지원하는 것들은 다음과 같지만 이에 국한되지 않습니다:



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

필요에 따라 Valet를 [커스텀 드라이버](#custom-valet-drivers)로 확장할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

> [!WARNING]
> Valet는 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전 Apache나 Nginx 같은 다른 프로그램이 로컬 머신의 80번 포트를 사용 중이지 않은지 반드시 확인하세요.

먼저 Homebrew를 최신 상태로 업데이트해야 합니다:

```shell
brew update
```

그 다음, Homebrew로 PHP를 설치합니다:

```shell
brew install php
```

PHP 설치가 완료되면 [Composer 패키지 관리자](https://getcomposer.org)를 설치할 준비가 된 것입니다. 그리고 `$HOME/.composer/vendor/bin` 디렉토리가 시스템의 "PATH"에 포함되어 있는지 확인하세요. Composer를 설치한 후에는 Laravel Valet를 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```

마지막으로 Valet의 `install` 명령어를 실행합니다. 이 명령어는 Valet와 DnsMasq를 구성 및 설치하며, Valet가 의존하는 데몬들을 시스템 부팅 시 자동으로 실행되도록 설정합니다:

```shell
valet install
```

설치가 완료되면 터미널에서 `ping foobar.test` 같은 명령어로 `*.test` 도메인을 ping 테스트해보세요. Valet가 제대로 설치되었다면 `127.0.0.1`에서 응답이 돌아올 것입니다.

Valet는 머신이 부팅할 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전 관리

> [!NOTE]
> 글로벌 PHP 버전을 변경하는 대신, `isolate` [명령어](#per-site-php-versions)를 사용해 사이트별 PHP 버전을 지정할 수 있습니다.

Valet는 `valet use php@version` 명령어로 PHP 버전을 전환할 수 있습니다. 지정한 PHP 버전이 설치되어 있지 않으면 Homebrew를 통해 자동으로 설치합니다:

```shell
valet use php@8.2

valet use php
```

또한 프로젝트 루트에 `.valetrc` 파일을 생성해 사이트가 사용할 PHP 버전을 지정할 수도 있습니다:

```shell
php=php@8.2
```

이 파일이 생성되면, 단순히 `valet use` 명령어를 실행하면 Valet가 `.valetrc` 파일을 읽어 사이트에 맞는 PHP 버전을 적용합니다.

> [!WARNING]
> 설치된 PHP 버전이 여러 개 있어도 Valet는 한 번에 하나의 PHP 버전만 사용합니다.

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요하면 [DBngin](https://dbngin.com)을 사용해보세요. MySQL, PostgreSQL, Redis 같은 데이터베이스를 한 번에 관리할 수 있는 무료 도구입니다. 설치 후에는 `127.0.0.1`에 `root` 사용자명과 빈 비밀번호로 연결할 수 있습니다.

<a name="resetting-your-installation"></a>
#### 설치 초기화

Valet가 제대로 실행되지 않는 문제가 있으면, `composer global require laravel/valet` 명령을 실행하고 이어서 `valet install`을 실행하면 설치를 초기화하고 다양한 문제를 해결할 수 있습니다. 드물게는 `valet uninstall --force`를 실행한 뒤 다시 `valet install`로 "강제 초기화"가 필요할 수도 있습니다.

<a name="upgrading-valet"></a>
### Valet 업그레이드

터미널에서 `composer global require laravel/valet` 명령어를 실행하여 Valet를 최신 버전으로 업데이트할 수 있습니다. 업그레이드 후에는 설정 파일에 추가적인 변경 사항이 있을 수 있으니 `valet install` 명령어를 실행하는 것이 좋습니다.

<a name="upgrading-to-valet-4"></a>
#### Valet 4 버전으로 업그레이드하기

Valet 3에서 Valet 4로 업그레이드할 때는 다음 절차를 따르세요:

<div class="content-list" markdown="1">

- 사이트별 PHP 버전을 커스텀하는 `.valetphprc` 파일을 사용 중이라면, 각 파일명을 `.valetrc`로 변경하고, 기존 내용 앞에 `php=`를 추가하세요.
- 기존 커스텀 드라이버가 있다면 네임스페이스, 확장, 타입 힌트, 반환 타입 힌트를 새로운 드라이버 시스템에 맞게 업데이트하세요. 예시는 Valet의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php)를 참고하세요.
- PHP 7.1~7.4 버전을 사용해 사이트를 제공하는 경우라도, Homebrew를 사용해 PHP 8.0 이상 버전을 반드시 설치하세요. Valet가 스크립트 실행용으로 이 버전을 사용하기 때문입니다(기본 링크된 PHP 버전과는 별개).

</div>

<a name="serving-sites"></a>
## 사이트 제공 (Serving Sites)

Valet 설치가 완료되면 Laravel 애플리케이션을 서빙할 준비가 된 것입니다. Valet는 애플리케이션을 서빙할 때 유용한 두 가지 명령어를 제공합니다: `park` 와 `link`.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 담긴 디렉토리를 Valet에 등록합니다. 일단 디렉토리를 `park`하면, 해당 디렉토리 안의 모든 하위 디렉토리가 웹 브라우저에서 `http://<디렉토리명>.test` 형식으로 접근 가능해집니다:

```shell
cd ~/Sites

valet park
```

이렇게 하면, "park"한 디렉토리 내에 생성된 모든 애플리케이션이 자동으로 `http://<디렉토리명>.test` 방식으로 서빙됩니다. 예를 들어, "laravel"이라는 디렉토리가 있다고 하면, `http://laravel.test`로 접근할 수 있고, Valet가 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동으로 지원합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 한 개의 특정 사이트만 서빙할 때 유용합니다. 전체 디렉토리를 서빙하지 않고 특정 폴더 하나만 연결하려는 경우에 사용하세요:

```shell
cd ~/Sites/laravel

valet link
```

이렇게 링크한 사이트는 해당 디렉토리명으로 접속할 수 있습니다. 위 예시 사이트는 `http://laravel.test`로 접근 가능합니다. 또한, 와일드카드 서브도메인(`http://foo.laravel.test`)도 자동 지원합니다.

다른 호스트명을 사용하고 싶다면 `link` 명령어 뒤에 원하는 이름을 지정할 수 있습니다. 예를 들어, `http://application.test`로 제공하려면:

```shell
cd ~/Sites/laravel

valet link application
```

서브도메인도 마찬가지로 지원됩니다:

```shell
valet link api.application
```

현재 연결된 모든 링크 목록을 보고 싶으면 다음 명령어를 실행하세요:

```shell
valet links
```

링크를 해제하려면 다음 명령어를 사용합니다:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS로 사이트 보안하기

기본적으로 Valet는 HTTP로 사이트를 제공합니다. 하지만 TLS와 HTTP/2를 사용하여 암호화된 연결을 원한다면 `secure` 명령어를 사용하세요. 만약 `laravel.test` 도메인에서 서비스 중인 사이트를 보안하고 싶다면 다음과 같이 실행합니다:

```shell
valet secure laravel
```

보안을 해제하고 HTTP만 사용하려면 `unsecure` 명령어를 사용하세요. 이 명령어 역시 대상 호스트명을 인수로 받습니다:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### 기본 사이트 제공

알 수 없는 `test` 도메인으로 접속했을 때 `404` 페이지 대신 기본 사이트를 제공하고 싶다면, `~/.config/valet/config.json` 파일에 다음과 같은 `default` 옵션을 추가하세요:

```
"default": "/Users/Sally/Sites/example-site",
```

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

기본적으로 Valet는 글로벌 PHP 설치본을 사용해 사이트를 서빙합니다. 하지만 여러 사이트에서 각기 다른 PHP 버전을 사용해야 한다면 `isolate` 명령어로 특정 사이트별 PHP 버전을 지정할 수 있습니다. 현재 작업 중인 디렉토리의 사이트를 지정한 PHP 버전으로 분리합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

사이트 이름이 디렉토리명과 다르다면 `--site` 옵션으로 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```

또한 `valet php`, `valet composer`, `valet which-php` 명령어를 사용해 사이트별 PHP CLI나 도구를 실행할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```

사이트별 PHP 버전이 설정된 목록을 보고 싶으면 `isolated` 명령어를 실행하세요:

```shell
valet isolated
```

사이트를 다시 글로벌 PHP 버전으로 되돌리려면 루트 디렉토리에서 `unisolate` 명령어를 실행하세요:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 사이트 공유 (Sharing Sites)

Valet는 로컬 사이트를 외부에 손쉽게 공유할 수 있는 명령어를 제공합니다. 모바일 기기 테스트나 팀원, 클라이언트와 빠르게 공유할 때 유용합니다.

Valet는 기본적으로 ngrok 또는 Expose를 통해 사이트를 공유할 수 있습니다. 사이트 공유 전에 `share-tool` 명령어로 `ngrok`, `expose`, `cloudflared` 중 공유 도구를 설정해야 합니다:

```shell
valet share-tool ngrok
```

선택한 도구가 Homebrew(ngrok, cloudflared)나 Composer(Expose)를 통해 설치되어 있지 않으면 Valet가 자동 설치를 권장합니다. 단, 두 도구 모두 공유를 시작하기 전에 계정 인증이 필요합니다.

사이트 폴더로 이동해 `share` 명령어를 실행하면 공개 가능한 URL이 클립보드에 복사되어 브라우저에 붙여넣거나 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```

공유를 중지하려면 `Control + C`를 누르세요.

> [!WARNING]
> 네트워크에서 사용자 지정 DNS 서버(e.g. `1.1.1.1`)를 사용하는 경우 ngrok 공유 기능이 제대로 작동하지 않을 수 있습니다. 이럴 때는 Mac의 시스템 설정 > 네트워크 > 고급 > DNS 탭에서 `127.0.0.1`을 첫 번째 DNS 서버로 추가하세요.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok로 사이트 공유하기

ngrok를 사용해 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup) 후 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 인증 토큰을 얻은 뒤 Valet에 설정하세요:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> 추가 ngrok 파라미터(예: `valet share --region=eu`)를 설정할 수 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs)를 참고하세요.

<a name="sharing-sites-via-expose"></a>
#### Expose로 사이트 공유하기

Expose를 이용하려면 [Expose 계정 생성](https://expose.dev/register) 후 [인증 토큰으로 인증](https://expose.dev/docs/getting-started/getting-your-token)이 필요합니다.

Expose가 지원하는 기타 명령행 파라미터 정보는 [Expose 문서](https://expose.dev/docs)를 참고하세요.

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유하기

Valet는 기본적으로 외부의 인터넷 접속으로부터 개발 머신을 보호하기 위해 들어오는 트래픽을 내부 인터페이스 `127.0.0.1`로 제한합니다.

만약 같은 로컬 네트워크 내 다른 기기에서 머신의 IP 주소(예: `192.168.1.10/application.test`)로 Valet 사이트에 접속하려면, 해당 사이트의 Nginx 설정 파일을 수동으로 수정해 `listen` 지시문의 `127.0.0.1:` 접두어를 제거해야 합니다(포트 80, 443 모두 해당).

`valet secure` 명령어를 실행하지 않은 경우에는 `/usr/local/etc/nginx/valet/valet.conf` 파일을 수정해 HTTPS 미사용 사이트에 대해 네트워크 접근을 열 수 있습니다. 만약 사이트가 HTTPS로 제공되고 있다면(`valet secure`가 실행된 상태), `~/.config/valet/Nginx/app-name.test` 파일을 수정하세요.

Nginx 설정을 수정한 뒤에는 `valet restart` 명령을 실행해 변경 사항을 적용해야 합니다.

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수 (Site Specific Environment Variables)

다른 프레임워크 기반 애플리케이션은 서버 환경 변수에 의존하면서도 프로젝트 내에서 설정할 방법이 없을 수 있습니다. Valet는 프로젝트 루트에 `.valet-env.php` 파일을 만들어 사이트별 환경 변수를 설정할 수 있게 합니다. 이 파일은 사이트별로 글로벌 `$_SERVER` 배열에 추가될 변수 쌍 배열을 반환해야 합니다:

```php
<?php

return [
    // laravel.test 사이트에 대해 $_SERVER['key']를 "value"로 설정...
    'laravel' => [
        'key' => 'value',
    ],

    // 모든 사이트에 대해 $_SERVER['key']를 "value"로 설정...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## 서비스 프록시 (Proxying Services)

가끔 Valet 도메인을 로컬 머신 내 다른 서비스로 프록시해야 할 때가 있습니다. 예를 들어, Valet를 실행하면서 Docker에서 별도의 사이트를 띄우려 할 때, 두 시스템 모두 80번 포트를 사용할 수 없으므로 프록시가 필요합니다.

`proxy` 명령어를 사용해 프록시를 생성할 수 있습니다. 예를 들어, `http://elasticsearch.test`의 모든 트래픽을 `http://127.0.0.1:9200`으로 프록시하려면:

```shell
# HTTP 프록시...
valet proxy elasticsearch http://127.0.0.1:9200

# TLS + HTTP/2 프록시...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

`unproxy` 명령어로 프록시를 제거할 수 있습니다:

```shell
valet unproxy elasticsearch
```

`proxies` 명령어를 사용해 프록시된 사이트 목록을 볼 수 있습니다:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## 커스텀 Valet 드라이버 (Custom Valet Drivers)

Valet가 기본 지원하지 않는 프레임워크나 CMS의 PHP 애플리케이션을 제공하고 싶을 때 직접 "드라이버"를 작성할 수 있습니다. Valet를 설치하면 `~/.config/valet/Drivers` 디렉토리가 생성되고, 여기에는 `SampleValetDriver.php` 파일이 포함되어 있어 커스텀 드라이버 작성 방법을 보여줍니다. 드라이버 작성은 세 가지 메서드만 구현하면 됩니다: `serves`, `isStaticFile`, 그리고 `frontControllerPath`.

세 메서드 모두 `$sitePath`, `$siteName`, `$uri` 인자를 받습니다. `$sitePath`는 `/Users/Lisa/Sites/my-project`와 같이 사이트가 설치된 절대 경로이고, `$siteName`은 도메인의 호스트명 또는 사이트명(`my-project`), `$uri`는 요청된 URI(`/foo/bar`)입니다.

커스텀 드라이버 작성이 끝나면 `~/.config/valet/Drivers` 폴더에 `FrameworkValetDriver.php` 형식의 이름으로 저장하세요. 예를 들어 WordPress용 드라이버라면 파일명은 `WordPressValetDriver.php`가 됩니다.

커스텀 드라이버 메서드 구현 예를 살펴보겠습니다.

<a name="the-serves-method"></a>
#### `serves` 메서드

`serves` 메서드는 해당 요청을 드라이버가 처리할지 결정하며, 처리한다면 `true`, 아니면 `false`를 반환해야 합니다. 이 메서드에서는 `$sitePath`에 해당 프로젝트가 존재하는지 판단하는 로직을 작성합니다.

예를 들어 `WordPressValetDriver`라면 `serves` 메서드는 아래와 같을 수 있습니다:

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

`isStaticFile` 메서드는 요청이 이미지, 스타일시트 등 "정적 파일"에 대한 것인지 판단합니다. 정적 파일이라면 파일의 절대 경로를 반환하고, 아니라면 `false`를 반환해야 합니다:

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
> `isStaticFile`은 `serves`가 해당 요청에 대해 `true`를 반환하고, 요청 URI가 `/`가 아닐 때만 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 애플리케이션의 "프론트 컨트롤러"(일반적으로 `index.php` 파일)의 절대 경로를 반환해야 합니다:

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
### 로컬 드라이버

단일 애플리케이션용 커스텀 Valet 드라이버를 정의하려면, 프로젝트 루트에 `LocalValetDriver.php` 파일을 생성하세요. 해당 커스텀 드라이버는 기본 `ValetDriver` 클래스를 상속하거나, `LaravelValetDriver` 같은 기존 애플리케이션 특화 드라이버를 확장할 수 있습니다:

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
## 기타 Valet 명령어

<div class="overflow-auto">

| 명령어 | 설명 |
| --- | --- |
| `valet list` | 모든 Valet 명령어 목록을 출력합니다. |
| `valet diagnose` | Valet 디버깅에 도움이 되는 진단 정보를 출력합니다. |
| `valet directory-listing` | 디렉토리 리스트 동작을 결정합니다. 기본값은 "off"로, 디렉토리에 대해 404 페이지를 반환합니다. |
| `valet forget` | "park" 상태인 디렉토리를 목록에서 제거합니다. |
| `valet log` | Valet의 서비스가 기록하는 로그 목록을 봅니다. |
| `valet paths` | "park"된 모든 경로를 확인합니다. |
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | Brew와 Valet 명령어를 암호 입력 없이 실행할 수 있도록 sudoers 파일을 추가합니다. |
| `valet uninstall` | Valet를 제거합니다: 수동 제거 지침을 안내하며, `--force` 옵션을 추가하면 Valet의 모든 리소스를 강제로 삭제합니다. |

</div>

<a name="valet-directories-and-files"></a>
## Valet 디렉토리와 파일 (Valet Directories and Files)

Valet 환경 문제 해결 시 다음 디렉토리와 파일 정보를 참고하면 도움이 됩니다:

#### `~/.config/valet`

Valet의 모든 설정을 저장하는 디렉토리입니다. 백업을 권장합니다.

#### `~/.config/valet/dnsmasq.d/`

DNSMasq 설정 파일이 저장됩니다.

#### `~/.config/valet/Drivers/`

Valet 드라이버가 저장되는 곳으로, 특정 프레임워크/CMS를 어떻게 서빙할지 결정합니다.

#### `~/.config/valet/Nginx/`

Valet에서 관리하는 Nginx 사이트 구성 파일들이 위치합니다. `install` 및 `secure` 명령 실행 시 이 파일들이 다시 생성됩니다.

#### `~/.config/valet/Sites/`

[링크한 프로젝트](#the-link-command)의 심볼릭 링크가 저장되는 디렉토리입니다.

#### `~/.config/valet/config.json`

Valet의 마스터 설정 파일입니다.

#### `~/.config/valet/valet.sock`

Valet의 Nginx가 사용하는 PHP-FPM 소켓 파일입니다. PHP가 정상 실행 중일 때만 존재합니다.

#### `~/.config/valet/Log/fpm-php.www.log`

PHP 에러 사용자 로그 파일입니다.

#### `~/.config/valet/Log/nginx-error.log`

Nginx 에러 사용자 로그 파일입니다.

#### `/usr/local/var/log/php-fpm.log`

시스템 PHP-FPM 에러 로그 파일입니다.

#### `/usr/local/var/log/nginx`

Nginx 접근 및 에러 로그 디렉토리입니다.

#### `/usr/local/etc/php/X.X/conf.d`

PHP 설정 관련 `*.ini` 파일들이 저장됩니다.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

PHP-FPM 풀 구성 파일입니다.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

사이트 SSL 인증서 생성을 위한 기본 Nginx 구성 파일입니다.

<a name="disk-access"></a>
### 디스크 접근 (Disk Access)

macOS 10.14부터 일부 파일 및 디렉토리에 대한 접근 권한이 기본적으로 제한됩니다. 여기에는 바탕화면, 문서, 다운로드 디렉토리뿐 아니라 네트워크 볼륨 및 외장 볼륨이 포함됩니다. 따라서 Valet를 사용할 때는 이러한 위치 외부에 사이트 폴더를 두는 것이 권장됩니다.

만약 보호된 위치에 사이트를 두고 서빙해야 한다면, Nginx에 "전체 디스크 접근 권한(Full Disk Access)"을 부여해야 합니다. 그렇지 않으면 서버 오류나 정적 자원 제공 시 예측 불가능한 문제가 발생할 수 있습니다. 일반적으로 macOS는 Nginx가 권한을 필요로 할 때 자동으로 접근 권한 요청 창을 띄웁니다. 수동으로 설정하려면 `시스템 환경설정` > `보안 및 개인정보 보호` > `개인정보 보호` 탭에서 `전체 디스크 접근`을 선택하고, 메인 창에 나타나는 `nginx` 항목을 활성화하세요.