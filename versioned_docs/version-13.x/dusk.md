# Laravel Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용하기](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 처리](#environment-handling)
- [브라우저 기본 사항](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [탐색](#navigation)
    - [브라우저 창 크기 조정](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 디스크에 저장](#storing-console-output-to-disk)
    - [페이지 소스 디스크에 저장](#storing-page-source-to-disk)
- [요소와 상호작용하기](#interacting-with-elements)
    - [Dusk 선택자](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용하기](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [JavaScript 대화 상자](#javascript-dialogs)
    - [인라인 프레임과 상호작용하기](#interacting-with-iframes)
    - [선택자 범위 지정](#scoping-selectors)
    - [요소 기다리기](#waiting-for-elements)
    - [요소를 화면 안으로 스크롤하기](#scrolling-an-element-into-view)
- [사용 가능한 Assertion](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [축약 선택자](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> 이제 [Pest 4](https://pestphp.com/)에는 Laravel Dusk와 비교해 성능과 사용성이 크게 개선된 자동화 브라우저 테스트 기능이 포함되어 있습니다. 새 프로젝트에서는 브라우저 테스트에 Pest를 사용하는 것을 권장합니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 표현력이 뛰어나고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 로컬 컴퓨터에 JDK나 Selenium을 설치하지 않아도 됩니다. 대신 Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 하지만 원하는 다른 Selenium 호환 driver를 자유롭게 사용할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가해야 합니다.

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, **절대로** 프로덕션 환경에 등록해서는 안 됩니다. 그렇게 하면 임의의 사용자가 애플리케이션에 인증할 수 있게 될 수 있습니다.

Dusk 패키지를 설치한 후 `dusk:install` Artisan 명령어를 실행합니다. `dusk:install` 명령어는 `tests/Browser` 디렉터리와 예제 Dusk 테스트를 만들고, 운영 체제에 맞는 Chrome Driver 바이너리를 설치합니다.

```shell
php artisan dusk:install
```

다음으로 애플리케이션의 `.env` 파일에서 `APP_URL` 환경 변수를 설정합니다. 이 값은 브라우저에서 애플리케이션에 접근할 때 사용하는 URL과 일치해야 합니다.

> [!NOTE]
> 로컬 개발 환경을 관리하기 위해 [Laravel Sail](/docs/13.x/sail)을 사용하고 있다면, [Dusk 테스트 설정 및 실행](/docs/13.x/sail#laravel-dusk)에 관한 Sail 문서도 함께 참고하십시오.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리

`dusk:install` 명령어를 통해 Laravel Dusk가 설치한 버전과 다른 ChromeDriver 버전을 설치하고 싶다면, `dusk:chrome-driver` 명령어를 사용할 수 있습니다.

```shell
# Install the latest version of ChromeDriver for your OS...
php artisan dusk:chrome-driver

# Install a given version of ChromeDriver for your OS...
php artisan dusk:chrome-driver 86

# Install a given version of ChromeDriver for all supported OSs...
php artisan dusk:chrome-driver --all

# Install the version of ChromeDriver that matches the detected version of Chrome / Chromium for your OS...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리가 실행 가능해야 합니다. Dusk 실행에 문제가 있다면, 다음 명령어를 사용해 바이너리가 실행 가능한 상태인지 확인해야 합니다: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용하기

기본적으로 Dusk는 브라우저 테스트를 실행하기 위해 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver) 설치를 사용합니다. 하지만 직접 Selenium 서버를 시작하고 원하는 브라우저를 대상으로 테스트를 실행할 수 있습니다.

시작하려면 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일에서 `startChromeDriver` 메서드 호출을 제거할 수 있습니다. 이렇게 하면 Dusk가 ChromeDriver를 자동으로 시작하지 않습니다.

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

다음으로 원하는 URL과 포트에 연결하도록 `driver` 메서드를 수정할 수 있습니다. 또한 WebDriver에 전달할 "desired capabilities"도 수정할 수 있습니다.

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
    );
}
```

<a name="getting-started"></a>
## 시작하기 (Getting Started)

<a name="generating-tests"></a>
### 테스트 생성

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용합니다. 생성된 테스트는 `tests/Browser` 디렉터리에 배치됩니다.

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

작성하는 대부분의 테스트는 애플리케이션의 데이터베이스에서 데이터를 가져오는 페이지와 상호작용합니다. 하지만 Dusk 테스트에서는 절대로 `RefreshDatabase` trait를 사용해서는 안 됩니다. `RefreshDatabase` trait는 데이터베이스 트랜잭션을 활용하는데, 이 트랜잭션은 HTTP 요청 간에는 적용되거나 사용할 수 없습니다. 대신 `DatabaseMigrations` trait와 `DatabaseTruncation` trait라는 두 가지 선택지가 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` trait는 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만 각 테스트마다 데이터베이스 테이블을 삭제하고 다시 만드는 방식은 일반적으로 테이블을 비우는 방식보다 느립니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    //
}
```

> [!WARNING]
> Dusk 테스트를 실행할 때는 SQLite 인메모리 데이터베이스를 사용할 수 없습니다. 브라우저는 자체 프로세스 안에서 실행되므로, 다른 프로세스의 인메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 테이블 비우기 사용

`DatabaseTruncation` trait는 데이터베이스 테이블이 올바르게 생성되었는지 확인하기 위해 첫 번째 테스트에서 데이터베이스를 마이그레이션합니다. 하지만 이후 테스트에서는 데이터베이스의 테이블을 단순히 비우기만 하므로, 모든 데이터베이스 마이그레이션을 다시 실행하는 것보다 속도가 빨라집니다.

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;

pest()->use(DatabaseTruncation::class);

//
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;

    //
}
```

기본적으로 이 trait는 `migrations` 테이블을 제외한 모든 테이블을 비웁니다. 비워야 하는 테이블을 직접 지정하고 싶다면 테스트 클래스에 `$tablesToTruncate` 속성을 정의할 수 있습니다.

> [!NOTE]
> Pest를 사용하는 경우, 기본 `DuskTestCase` 클래스나 테스트 파일이 확장하는 클래스에 속성 또는 메서드를 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는 테스트 클래스에 `$exceptTables` 속성을 정의해 비우기 대상에서 제외할 테이블을 지정할 수 있습니다.

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

테이블을 비울 데이터베이스 연결을 지정하려면 테스트 클래스에 `$connectionsToTruncate` 속성을 정의할 수 있습니다.

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

데이터베이스 테이블을 비우기 전이나 후에 코드를 실행하고 싶다면, 테스트 클래스에 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의할 수 있습니다.

```php
/**
 * Perform any work that should take place before the database has started truncating.
 */
protected function beforeTruncatingDatabase(): void
{
    //
}

/**
 * Perform any work that should take place after the database has finished truncating.
 */
protected function afterTruncatingDatabase(): void
{
    //
}
```

<a name="running-tests"></a>
### 테스트 실행

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 실행합니다.

```shell
php artisan dusk
```

마지막으로 `dusk` 명령어를 실행했을 때 실패한 테스트가 있었다면, `dusk:fails` 명령어를 사용해 실패한 테스트를 먼저 다시 실행하여 시간을 절약할 수 있습니다.

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스트 러너가 일반적으로 받는 모든 인수를 받을 수 있습니다. 예를 들어 특정 [group](https://docs.phpunit.de/en/10.5/annotations.html#group)에 속한 테스트만 실행할 수 있습니다.

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> 로컬 개발 환경을 관리하기 위해 [Laravel Sail](/docs/13.x/sail)을 사용하고 있다면, [Dusk 테스트 설정 및 실행](/docs/13.x/sail#laravel-dusk)에 관한 Sail 문서를 참고하십시오.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 시작

기본적으로 Dusk는 ChromeDriver를 자동으로 시작하려고 시도합니다. 특정 시스템에서 이 방식이 동작하지 않는다면, `dusk` 명령어를 실행하기 전에 ChromeDriver를 수동으로 시작할 수 있습니다. ChromeDriver를 수동으로 시작하기로 했다면, `tests/DuskTestCase.php` 파일의 다음 줄을 주석 처리해야 합니다.

```php
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 */
public static function prepare(): void
{
    // static::startChromeDriver();
}
```

또한 ChromeDriver를 9515가 아닌 다른 포트에서 시작했다면, 같은 클래스의 `driver` 메서드가 올바른 포트를 반영하도록 수정해야 합니다.

```php
use Facebook\WebDriver\Remote\RemoteWebDriver;

/**
 * Create the RemoteWebDriver instance.
 */
protected function driver(): RemoteWebDriver
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
### 환경 처리

테스트 실행 시 Dusk가 자체 환경 파일을 사용하도록 강제하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만듭니다. 예를 들어 `local` 환경에서 `dusk` 명령어를 시작한다면 `.env.dusk.local` 파일을 만들어야 합니다.

테스트를 실행할 때 Dusk는 `.env` 파일을 백업하고 Dusk 환경 파일의 이름을 `.env`로 변경합니다. 테스트가 완료되면 기존 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 사항 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성

시작을 위해 애플리케이션에 로그인할 수 있는지 확인하는 테스트를 작성해 보겠습니다. 테스트를 생성한 후, 로그인 페이지로 이동하고, 몇 가지 인증 정보를 입력하고, "Login" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스를 생성하려면 Dusk 테스트 안에서 `browse` 메서드를 호출하면 됩니다.

```php tab=Pest
<?php

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $user = User::factory()->create([
        'email' => 'taylor@laravel.com',
    ]);

    $this->browse(function (Browser $browser) use ($user) {
        $browser->visit('/login')
            ->type('email', $user->email)
            ->type('password', 'password')
            ->press('Login')
            ->assertPathIs('/home');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * A basic browser test example.
     */
    public function test_basic_example(): void
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function (Browser $browser) use ($user) {
            $browser->visit('/login')
                ->type('email', $user->email)
                ->type('password', 'password')
                ->press('Login')
                ->assertPathIs('/home');
        });
    }
}
```
위 예제에서 볼 수 있듯이, `browse` 메서드는 클로저를 받습니다. Dusk는 이 클로저에 브라우저 인스턴스를 자동으로 전달하며, 이 인스턴스가 애플리케이션과 상호작용하고 애플리케이션에 대한 assertion을 수행하는 데 사용하는 주요 객체입니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 만들기

테스트를 제대로 수행하기 위해 여러 브라우저가 필요할 때가 있습니다. 예를 들어, WebSocket과 상호작용하는 채팅 화면을 테스트하려면 여러 브라우저가 필요할 수 있습니다. 여러 브라우저를 만들려면 `browse` 메서드에 전달하는 클로저의 시그니처에 브라우저 인수를 더 추가하면 됩니다.

```php
$this->browse(function (Browser $first, Browser $second) {
    $first->loginAs(User::find(1))
        ->visit('/home')
        ->waitForText('Message');

    $second->loginAs(User::find(2))
        ->visit('/home')
        ->waitForText('Message')
        ->type('message', 'Hey Taylor')
        ->press('Send');

    $first->waitForText('Hey Taylor')
        ->assertSee('Jeffrey Way');
});
```

<a name="navigation"></a>
### 내비게이션

`visit` 메서드를 사용하여 애플리케이션 내의 지정된 URI로 이동할 수 있습니다.

```php
$browser->visit('/login');
```

`visitRoute` 메서드를 사용하여 [이름이 지정된 라우트](/docs/13.x/routing#named-routes)로 이동할 수 있습니다.

```php
$browser->visitRoute($routeName, $parameters);
```

`back` 및 `forward` 메서드를 사용하여 "뒤로" 및 "앞으로" 이동할 수 있습니다.

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드를 사용하여 페이지를 새로고침할 수 있습니다.

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조정

`resize` 메서드를 사용하여 브라우저 창의 크기를 조정할 수 있습니다.

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드를 사용하여 브라우저 창을 최대화할 수 있습니다.

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창의 크기를 콘텐츠 크기에 맞게 조정합니다.

```php
$browser->fitContent();
```

테스트가 실패하면 Dusk는 스크린샷을 찍기 전에 브라우저 크기를 콘텐츠에 맞게 자동으로 조정합니다. 테스트 내에서 `disableFitOnFailure` 메서드를 호출하여 이 기능을 비활성화할 수 있습니다.

```php
$browser->disableFitOnFailure();
```

`move` 메서드를 사용하여 브라우저 창을 화면의 다른 위치로 이동할 수 있습니다.

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로

여러 테스트에서 재사용할 수 있는 사용자 정의 브라우저 메서드를 정의하려면 `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 [서비스 프로바이더](/docs/13.x/providers)의 `boot` 메서드에서 호출해야 합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Browser::macro('scrollToElement', function (string $element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

`macro` 함수는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받습니다. `Browser` 인스턴스에서 매크로를 메서드처럼 호출하면 해당 매크로의 클로저가 실행됩니다.

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증

인증이 필요한 페이지를 테스트하는 경우가 많습니다. 매번 테스트에서 애플리케이션의 로그인 화면과 상호작용하지 않으려면 Dusk의 `loginAs` 메서드를 사용할 수 있습니다. `loginAs` 메서드는 인증 가능한 모델과 연결된 기본 키 또는 인증 가능한 모델 인스턴스를 받습니다.

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용한 후에는 해당 파일 안의 모든 테스트에서 사용자 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키

`cookie` 메서드를 사용하여 암호화된 쿠키 값을 가져오거나 설정할 수 있습니다. 기본적으로 Laravel이 생성하는 모든 쿠키는 암호화됩니다.

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

`plainCookie` 메서드를 사용하여 암호화되지 않은 쿠키 값을 가져오거나 설정할 수 있습니다.

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` 메서드를 사용하여 지정된 쿠키를 삭제할 수 있습니다.

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행하기

`script` 메서드를 사용하여 브라우저 안에서 임의의 JavaScript 문을 실행할 수 있습니다.

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기

`screenshot` 메서드를 사용하여 스크린샷을 찍고 지정된 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다.

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드를 사용하여 여러 breakpoint에서 일련의 스크린샷을 찍을 수 있습니다.

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드를 사용하여 페이지의 특정 요소를 스크린샷으로 찍을 수 있습니다.

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력을 디스크에 저장하기

`storeConsoleLog` 메서드를 사용하여 현재 브라우저의 콘솔 출력을 지정된 파일명으로 디스크에 기록할 수 있습니다. 콘솔 출력은 `tests/Browser/console` 디렉터리에 저장됩니다.

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스를 디스크에 저장하기

`storeSource` 메서드를 사용하여 현재 페이지의 소스를 지정된 파일명으로 디스크에 기록할 수 있습니다. 페이지 소스는 `tests/Browser/source` 디렉터리에 저장됩니다.

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 선택자

요소와 상호작용하기 위한 좋은 CSS 선택자를 고르는 일은 Dusk 테스트를 작성할 때 가장 어려운 부분 중 하나입니다. 시간이 지나면서 프론트엔드가 변경되면 다음과 같은 CSS 선택자가 테스트를 깨뜨릴 수 있습니다.

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 선택자를 사용하면 CSS 선택자를 기억하는 대신 효과적인 테스트 작성에 집중할 수 있습니다. 선택자를 정의하려면 HTML 요소에 `dusk` 속성을 추가하십시오. 그런 다음 Dusk 브라우저와 상호작용할 때 선택자 앞에 `@`를 붙이면 테스트 안에서 연결된 요소를 조작할 수 있습니다.

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원한다면 `selectorHtmlAttribute` 메서드를 통해 Dusk 선택자가 사용하는 HTML 속성을 사용자 정의할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드에서 호출해야 합니다.

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성

<a name="retrieving-setting-values"></a>
#### 값 가져오기 및 설정하기

Dusk는 페이지 요소의 현재 값, 표시 텍스트, 속성과 상호작용하기 위한 여러 메서드를 제공합니다. 예를 들어, 지정된 CSS 또는 Dusk 선택자와 일치하는 요소의 "value"를 가져오려면 `value` 메서드를 사용하십시오.

```php
// Retrieve the value...
$value = $browser->value('selector');

// Set the value...
$browser->value('selector', 'value');
```

지정된 필드 이름을 가진 입력 요소의 "value"를 가져오려면 `inputValue` 메서드를 사용할 수 있습니다.

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기

`text` 메서드를 사용하여 지정된 선택자와 일치하는 요소의 표시 텍스트를 가져올 수 있습니다.

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기

마지막으로, `attribute` 메서드를 사용하여 지정된 선택자와 일치하는 요소의 속성 값을 가져올 수 있습니다.

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용하기

<a name="typing-values"></a>
#### 값 입력하기

Dusk는 폼 및 입력 요소와 상호작용하기 위한 다양한 메서드를 제공합니다. 먼저 입력 필드에 텍스트를 입력하는 예제를 살펴보겠습니다.

```php
$browser->type('email', 'taylor@laravel.com');
```

필요하다면 이 메서드에 CSS 선택자를 전달할 수 있지만, `type` 메서드에 반드시 CSS 선택자를 전달해야 하는 것은 아닙니다. CSS 선택자가 제공되지 않으면 Dusk는 지정된 `name` 속성을 가진 `input` 또는 `textarea` 필드를 검색합니다.

필드의 기존 내용을 지우지 않고 텍스트를 덧붙이려면 `append` 메서드를 사용할 수 있습니다.

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

`clear` 메서드를 사용하여 입력 값를 비울 수 있습니다.

```php
$browser->clear('email');
```

`typeSlowly` 메서드를 사용하면 Dusk가 천천히 입력하도록 지시할 수 있습니다. 기본적으로 Dusk는 키 입력 사이에 100밀리초 동안 멈춥니다. 키 입력 사이의 시간을 사용자 정의하려면 적절한 밀리초 값을 메서드의 세 번째 인수로 전달하면 됩니다.

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드를 사용하여 텍스트를 천천히 덧붙일 수 있습니다.

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 요소에서 사용할 수 있는 값을 선택하려면 `select` 메서드를 사용할 수 있습니다. `type` 메서드와 마찬가지로 `select` 메서드에도 전체 CSS 선택자가 필요하지 않습니다. `select` 메서드에 값을 전달할 때는 표시 텍스트가 아니라 실제 option 값을 전달해야 합니다.

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 무작위 option을 선택할 수 있습니다.

```php
$browser->select('size');
```

`select` 메서드의 두 번째 인수로 배열을 제공하면 여러 option을 선택하도록 메서드에 지시할 수 있습니다.

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

checkbox 입력을 "체크"하려면 `check` 메서드를 사용할 수 있습니다. 다른 많은 입력 관련 메서드와 마찬가지로 전체 CSS 선택자는 필요하지 않습니다. CSS 선택자와 일치하는 항목을 찾을 수 없으면 Dusk는 일치하는 `name` 속성을 가진 checkbox를 검색합니다.

```php
$browser->check('terms');
```

`uncheck` 메서드를 사용하여 checkbox 입력을 "체크 해제"할 수 있습니다.

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

`radio` 입력 option을 "선택"하려면 `radio` 메서드를 사용할 수 있습니다. 다른 많은 입력 관련 메서드와 마찬가지로 전체 CSS 선택자는 필요하지 않습니다. CSS 선택자와 일치하는 항목을 찾을 수 없으면 Dusk는 일치하는 `name` 및 `value` 속성을 가진 `radio` 입력을 검색합니다.

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부하기

`attach` 메서드를 사용하여 `file` 입력 요소에 파일을 첨부할 수 있습니다. 다른 많은 입력 관련 메서드와 마찬가지로 전체 CSS 선택자는 필요하지 않습니다. CSS 선택자와 일치하는 항목을 찾을 수 없으면 Dusk는 일치하는 `name` 속성을 가진 `file` 입력을 검색합니다.

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```
> [!WARNING]
> `attach` 함수는 서버에 `Zip` PHP 확장이 설치되고 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기

`press` 메서드는 페이지의 버튼 요소를 클릭할 때 사용할 수 있습니다. `press` 메서드에 전달하는 인수는 버튼에 표시되는 텍스트이거나 CSS / Dusk 셀렉터일 수 있습니다.

```php
$browser->press('Login');
```

폼을 제출할 때 많은 애플리케이션은 버튼이 눌린 후 폼의 제출 버튼을 비활성화하고, 폼 제출의 HTTP 요청이 완료되면 버튼을 다시 활성화합니다. 버튼을 누른 뒤 버튼이 다시 활성화될 때까지 기다리려면 `pressAndWaitFor` 메서드를 사용할 수 있습니다.

```php
// Press the button and wait a maximum of 5 seconds for it to be enabled...
$browser->pressAndWaitFor('Save');

// Press the button and wait a maximum of 1 second for it to be enabled...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭하기

링크를 클릭하려면 브라우저 인스턴스에서 `clickLink` 메서드를 사용할 수 있습니다. `clickLink` 메서드는 지정된 표시 텍스트를 가진 링크를 클릭합니다.

```php
$browser->clickLink($linkText);
```

지정된 표시 텍스트를 가진 링크가 페이지에 보이는지 확인하려면 `seeLink` 메서드를 사용할 수 있습니다.

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드들은 jQuery와 상호작용합니다. 페이지에서 jQuery를 사용할 수 없다면, Dusk는 테스트가 실행되는 동안 사용할 수 있도록 페이지에 jQuery를 자동으로 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 사용하기

`keys` 메서드를 사용하면 일반적으로 `type` 메서드가 허용하는 것보다 더 복잡한 입력 시퀀스를 특정 요소에 제공할 수 있습니다. 예를 들어 값을 입력하는 동안 Dusk가 수정 키를 누르고 있도록 지시할 수 있습니다. 다음 예제에서는 주어진 셀렉터와 일치하는 요소에 `taylor`를 입력하는 동안 `shift` 키가 눌린 상태로 유지됩니다. `taylor`가 입력된 후에는 수정 키 없이 `swift`가 입력됩니다.

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

`keys` 메서드의 또 다른 유용한 사용 사례는 애플리케이션의 기본 CSS 셀렉터에 "키보드 단축키" 조합을 보내는 것입니다.

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 모든 수정 키는 `{}` 문자로 감싸며, `Facebook\WebDriver\WebDriverKeys` 클래스에 정의된 상수와 일치합니다. 이 클래스는 [GitHub에서 확인할 수 있습니다](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php).

<a name="fluent-keyboard-interactions"></a>
#### 플루언트 키보드 상호작용

Dusk는 `withKeyboard` 메서드도 제공합니다. 이 메서드를 사용하면 `Laravel\Dusk\Keyboard` 클래스를 통해 복잡한 키보드 상호작용을 유창하게 수행할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 제공합니다.

```php
use Laravel\Dusk\Keyboard;

$browser->withKeyboard(function (Keyboard $keyboard) {
    $keyboard->press('c')
        ->pause(1000)
        ->release('c')
        ->type(['c', 'e', 'o']);
});
```

<a name="keyboard-macros"></a>
#### 키보드 매크로

테스트 스위트 전체에서 쉽게 재사용할 수 있는 사용자 정의 키보드 상호작용을 정의하고 싶다면 `Keyboard` 클래스가 제공하는 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 [ServiceProvider의](/docs/13.x/providers) `boot` 메서드에서 호출해야 합니다.

```php
<?php

namespace App\Providers;

use Facebook\WebDriver\WebDriverKeys;
use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Keyboard;
use Laravel\Dusk\OperatingSystem;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     */
    public function boot(): void
    {
        Keyboard::macro('copy', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'c',
            ]);

            return $this;
        });

        Keyboard::macro('paste', function (string $element = null) {
            $this->type([
                OperatingSystem::onMac() ? WebDriverKeys::META : WebDriverKeys::CONTROL, 'v',
            ]);

            return $this;
        });
    }
}
```

`macro` 함수는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받습니다. 매크로의 클로저는 `Keyboard` 인스턴스에서 매크로를 메서드처럼 호출할 때 실행됩니다.

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용하기

<a name="clicking-on-elements"></a>
#### 요소 클릭하기

`click` 메서드는 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소를 클릭할 때 사용할 수 있습니다.

```php
$browser->click('.selector');
```

`clickAtXPath` 메서드는 주어진 XPath 표현식과 일치하는 요소를 클릭할 때 사용할 수 있습니다.

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` 메서드는 브라우저의 표시 가능한 영역을 기준으로 주어진 좌표 쌍에 있는 최상위 요소를 클릭할 때 사용할 수 있습니다.

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` 메서드는 마우스 더블 클릭을 시뮬레이션할 때 사용할 수 있습니다.

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick` 메서드는 마우스 오른쪽 클릭을 시뮬레이션할 때 사용할 수 있습니다.

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` 메서드는 마우스 버튼을 클릭한 채로 누르고 있는 동작을 시뮬레이션할 때 사용할 수 있습니다. 이후 `releaseMouse` 메서드를 호출하면 이 동작이 해제되고 마우스 버튼이 놓입니다.

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick` 메서드는 브라우저 내에서 `ctrl+click` 이벤트를 시뮬레이션할 때 사용할 수 있습니다.

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

`clickWhenVisible` 또는 `clickWhenEnabled` 메서드는 요소가 준비될 때까지 기다린 뒤 정확히 한 번 클릭하는 데 사용할 수 있습니다:

```php
$browser->clickWhenVisible('@save-button');
$browser->clickWhenEnabled('@submit-button');
```

<a name="mouseover"></a>
#### 마우스오버

`mouseover` 메서드는 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소 위로 마우스를 이동해야 할 때 사용할 수 있습니다.

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드는 주어진 셀렉터와 일치하는 요소를 다른 요소로 드래그할 때 사용할 수 있습니다.

```php
$browser->drag('.from-selector', '.to-selector');
```

또는 요소를 한 방향으로 드래그할 수도 있습니다.

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

마지막으로, 주어진 오프셋만큼 요소를 드래그할 수도 있습니다.

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 대화 상자

Dusk는 JavaScript 대화 상자와 상호작용하기 위한 다양한 메서드를 제공합니다. 예를 들어 `waitForDialog` 메서드를 사용하여 JavaScript 대화 상자가 나타날 때까지 기다릴 수 있습니다. 이 메서드는 대화 상자가 나타날 때까지 몇 초 동안 기다릴지를 나타내는 선택적 인수를 받습니다.

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` 메서드는 대화 상자가 표시되었고 지정된 메시지를 포함하는지 검증할 때 사용할 수 있습니다.

```php
$browser->assertDialogOpened('Dialog message');
```

JavaScript 대화 상자에 프롬프트가 포함되어 있다면 `typeInDialog` 메서드를 사용하여 프롬프트에 값을 입력할 수 있습니다.

```php
$browser->typeInDialog('Hello World');
```

열려 있는 JavaScript 대화 상자를 "OK" 버튼을 클릭해 닫으려면 `acceptDialog` 메서드를 호출할 수 있습니다.

```php
$browser->acceptDialog();
```

열려 있는 JavaScript 대화 상자를 "Cancel" 버튼을 클릭해 닫으려면 `dismissDialog` 메서드를 호출할 수 있습니다.

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용하기

iframe 내부의 요소와 상호작용해야 한다면 `withinFrame` 메서드를 사용할 수 있습니다. `withinFrame` 메서드에 제공된 클로저 안에서 수행되는 모든 요소 상호작용은 지정된 iframe의 컨텍스트로 범위가 제한됩니다.

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정하기

때로는 주어진 셀렉터 안으로 모든 작업의 범위를 제한한 상태에서 여러 작업을 수행하고 싶을 수 있습니다. 예를 들어 특정 텍스트가 테이블 안에만 존재하는지 검증한 다음, 해당 테이블 안의 버튼을 클릭하고 싶을 수 있습니다. 이를 위해 `with` 메서드를 사용할 수 있습니다. `with` 메서드에 전달된 클로저 안에서 수행되는 모든 작업은 원래 셀렉터로 범위가 제한됩니다.

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

때로는 현재 범위 밖에서 검증을 실행해야 할 수도 있습니다. 이를 위해 `elsewhere` 및 `elsewhereWhenAvailable` 메서드를 사용할 수 있습니다.

```php
$browser->with('.table', function (Browser $table) {
    // Current scope is `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 기다리기

JavaScript를 많이 사용하는 애플리케이션을 테스트할 때는 테스트를 계속 진행하기 전에 특정 요소나 데이터를 사용할 수 있을 때까지 "기다려야" 하는 경우가 자주 있습니다. Dusk를 사용하면 이 작업이 매우 간단해집니다. 다양한 메서드를 사용하여 요소가 페이지에 보일 때까지 기다리거나, 주어진 JavaScript 표현식이 `true`로 평가될 때까지 기다릴 수도 있습니다.

<a name="waiting"></a>
#### 기다리기

테스트를 주어진 밀리초 동안 잠시 멈추기만 하면 된다면 `pause` 메서드를 사용합니다.

```php
$browser->pause(1000);
```

주어진 조건이 `true`일 때만 테스트를 잠시 멈춰야 한다면 `pauseIf` 메서드를 사용합니다.

```php
$browser->pauseIf(App::environment('production'), 1000);
```

마찬가지로, 주어진 조건이 `true`가 아닌 경우에만 테스트를 잠시 멈춰야 한다면 `pauseUnless` 메서드를 사용할 수 있습니다.

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 기다리기

`waitFor` 메서드는 주어진 CSS 또는 Dusk 셀렉터와 일치하는 요소가 페이지에 표시될 때까지 테스트 실행을 일시 중지할 때 사용할 수 있습니다. 기본적으로 이 메서드는 예외를 발생시키기 전에 최대 5초 동안 테스트를 일시 중지합니다. 필요한 경우 메서드의 두 번째 인수로 사용자 정의 제한 시간을 전달할 수 있습니다.

```php
// Wait a maximum of five seconds for the selector...
$browser->waitFor('.selector');

// Wait a maximum of one second for the selector...
$browser->waitFor('.selector', 1);
```

주어진 셀렉터와 일치하는 요소가 지정된 텍스트를 포함할 때까지 기다릴 수도 있습니다.

```php
// Wait a maximum of five seconds for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World');

// Wait a maximum of one second for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

주어진 셀렉터와 일치하는 요소가 페이지에서 사라질 때까지 기다릴 수도 있습니다.

```php
// Wait a maximum of five seconds until the selector is missing...
$browser->waitUntilMissing('.selector');

// Wait a maximum of one second until the selector is missing...
$browser->waitUntilMissing('.selector', 1);
```

또는 주어진 셀렉터와 일치하는 요소가 활성화되거나 비활성화될 때까지 기다릴 수 있습니다.

```php
// Wait a maximum of five seconds until the selector is enabled...
$browser->waitUntilEnabled('.selector');

// Wait a maximum of one second until the selector is enabled...
$browser->waitUntilEnabled('.selector', 1);

// Wait a maximum of five seconds until the selector is disabled...
$browser->waitUntilDisabled('.selector');

// Wait a maximum of one second until the selector is disabled...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 사용 가능할 때 셀렉터 범위 지정하기

때로는 주어진 셀렉터와 일치하는 요소가 나타날 때까지 기다린 다음, 그 요소와 상호작용하고 싶을 수 있습니다. 예를 들어 모달 창을 사용할 수 있을 때까지 기다린 뒤 모달 안의 "OK" 버튼을 누르고 싶을 수 있습니다. 이를 위해 `whenAvailable` 메서드를 사용할 수 있습니다. 주어진 클로저 안에서 수행되는 모든 요소 작업은 원래 셀렉터로 범위가 제한됩니다.

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 기다리기

`waitForText` 메서드는 주어진 텍스트가 페이지에 표시될 때까지 기다릴 때 사용할 수 있습니다.

```php
// Wait a maximum of five seconds for the text...
$browser->waitForText('Hello World');

// Wait a maximum of one second for the text...
$browser->waitForText('Hello World', 1);
```

표시된 텍스트가 페이지에서 제거될 때까지 기다리려면 `waitUntilMissingText` 메서드를 사용할 수 있습니다.

```php
// Wait a maximum of five seconds for the text to be removed...
$browser->waitUntilMissingText('Hello World');

// Wait a maximum of one second for the text to be removed...
$browser->waitUntilMissingText('Hello World', 1);
```
<a name="waiting-for-links"></a>
#### 링크 기다리기

`waitForLink` 메서드는 지정한 링크 텍스트가 페이지에 표시될 때까지 기다리는 데 사용할 수 있습니다.

```php
// Wait a maximum of five seconds for the link...
$browser->waitForLink('Create');

// Wait a maximum of one second for the link...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 기다리기

`waitForInput` 메서드는 지정한 입력 필드가 페이지에 보일 때까지 기다리는 데 사용할 수 있습니다.

```php
// Wait a maximum of five seconds for the input...
$browser->waitForInput($field);

// Wait a maximum of one second for the input...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 기다리기

`$browser->assertPathIs('/home')`처럼 경로 어설션을 수행할 때, `window.location.pathname`이 비동기적으로 업데이트되고 있으면 어설션이 실패할 수 있습니다. `waitForLocation` 메서드를 사용하면 위치가 지정한 값이 될 때까지 기다릴 수 있습니다.

```php
$browser->waitForLocation('/secret');
```

`waitForLocation` 메서드는 현재 창의 위치가 정규화된 전체 URL이 될 때까지 기다리는 데에도 사용할 수 있습니다.

```php
$browser->waitForLocation('https://example.com/path');
```

[이름이 지정된 라우트](/docs/13.x/routing#named-routes)의 위치를 기다릴 수도 있습니다.

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 기다리기

어떤 동작을 수행한 뒤 페이지가 새로고침될 때까지 기다려야 한다면 `waitForReload` 메서드를 사용합니다.

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

페이지 새로고침을 기다려야 하는 경우는 보통 버튼을 클릭한 뒤에 발생하므로, 편의를 위해 `clickAndWaitForReload` 메서드를 사용할 수 있습니다.

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 표현식 기다리기

때로는 지정한 JavaScript 표현식이 `true`로 평가될 때까지 테스트 실행을 일시 중지하고 싶을 수 있습니다. `waitUntil` 메서드를 사용하면 이를 쉽게 처리할 수 있습니다. 이 메서드에 표현식을 전달할 때는 `return` 키워드나 끝나는 세미콜론을 포함하지 않아도 됩니다.

```php
// Wait a maximum of five seconds for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0');

// Wait a maximum of one second for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 기다리기

`waitUntilVue` 및 `waitUntilVueIsNot` 메서드는 [Vue 컴포넌트](https://vuejs.org) 속성이 지정한 값을 가질 때까지 기다리는 데 사용할 수 있습니다.

```php
// Wait until the component attribute contains the given value...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// Wait until the component attribute doesn't contain the given value...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 기다리기

`waitForEvent` 메서드는 JavaScript 이벤트가 발생할 때까지 테스트 실행을 일시 중지하는 데 사용할 수 있습니다.

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 현재 스코프에 연결되며, 기본값은 `body` 요소입니다. 스코프가 지정된 셀렉터를 사용할 경우 이벤트 리스너는 일치하는 요소에 연결됩니다.

```php
$browser->with('iframe', function (Browser $iframe) {
    // Wait for the iframe's load event...
    $iframe->waitForEvent('load');
});
```

`waitForEvent` 메서드의 두 번째 인수로 셀렉터를 전달하여 이벤트 리스너를 특정 요소에 연결할 수도 있습니다.

```php
$browser->waitForEvent('load', '.selector');
```

`document` 및 `window` 객체에서 발생하는 이벤트를 기다릴 수도 있습니다.

```php
// Wait until the document is scrolled...
$browser->waitForEvent('scroll', 'document');

// Wait a maximum of five seconds until the window is resized...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백으로 기다리기

Dusk의 여러 "wait" 메서드는 내부적으로 `waitUsing` 메서드에 의존합니다. 이 메서드를 직접 사용하면 지정한 클로저가 `true`를 반환할 때까지 기다릴 수 있습니다. `waitUsing` 메서드는 기다릴 최대 초 수, 클로저를 평가할 간격, 클로저, 그리고 선택 사항인 실패 메시지를 인수로 받습니다.

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 화면 안으로 스크롤하기

요소가 브라우저의 보이는 영역 밖에 있어서 클릭할 수 없는 경우가 있습니다. `scrollIntoView` 메서드는 지정한 셀렉터의 요소가 화면 안에 들어올 때까지 브라우저 창을 스크롤합니다.

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 수행할 수 있는 다양한 어설션을 제공합니다. 사용 가능한 모든 어설션은 아래 목록에 문서화되어 있습니다.

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[assertTitle](#assert-title)
[assertTitleContains](#assert-title-contains)
[assertUrlIs](#assert-url-is)
[assertSchemeIs](#assert-scheme-is)
[assertSchemeIsNot](#assert-scheme-is-not)
[assertHostIs](#assert-host-is)
[assertHostIsNot](#assert-host-is-not)
[assertPortIs](#assert-port-is)
[assertPortIsNot](#assert-port-is-not)
[assertPathBeginsWith](#assert-path-begins-with)
[assertPathEndsWith](#assert-path-ends-with)
[assertPathContains](#assert-path-contains)
[assertPathIs](#assert-path-is)
[assertPathIsNot](#assert-path-is-not)
[assertRouteIs](#assert-route-is)
[assertQueryStringHas](#assert-query-string-has)
[assertQueryStringMissing](#assert-query-string-missing)
[assertFragmentIs](#assert-fragment-is)
[assertFragmentBeginsWith](#assert-fragment-begins-with)
[assertFragmentIsNot](#assert-fragment-is-not)
[assertHasCookie](#assert-has-cookie)
[assertHasPlainCookie](#assert-has-plain-cookie)
[assertCookieMissing](#assert-cookie-missing)
[assertPlainCookieMissing](#assert-plain-cookie-missing)
[assertCookieValue](#assert-cookie-value)
[assertPlainCookieValue](#assert-plain-cookie-value)
[assertSee](#assert-see)
[assertDontSee](#assert-dont-see)
[assertSeeIn](#assert-see-in)
[assertDontSeeIn](#assert-dont-see-in)
[assertSeeAnythingIn](#assert-see-anything-in)
[assertSeeNothingIn](#assert-see-nothing-in)
[assertCount](#assert-count)
[assertScript](#assert-script)
[assertSourceHas](#assert-source-has)
[assertSourceMissing](#assert-source-missing)
[assertSeeLink](#assert-see-link)
[assertDontSeeLink](#assert-dont-see-link)
[assertInputValue](#assert-input-value)
[assertInputValueIsNot](#assert-input-value-is-not)
[assertChecked](#assert-checked)
[assertNotChecked](#assert-not-checked)
[assertIndeterminate](#assert-indeterminate)
[assertRadioSelected](#assert-radio-selected)
[assertRadioNotSelected](#assert-radio-not-selected)
[assertSelected](#assert-selected)
[assertNotSelected](#assert-not-selected)
[assertSelectHasOptions](#assert-select-has-options)
[assertSelectMissingOptions](#assert-select-missing-options)
[assertSelectHasOption](#assert-select-has-option)
[assertSelectMissingOption](#assert-select-missing-option)
[assertValue](#assert-value)
[assertValueIsNot](#assert-value-is-not)
[assertAttribute](#assert-attribute)
[assertAttributeMissing](#assert-attribute-missing)
[assertAttributeContains](#assert-attribute-contains)
[assertAttributeDoesntContain](#assert-attribute-doesnt-contain)
[assertAriaAttribute](#assert-aria-attribute)
[assertDataAttribute](#assert-data-attribute)
[assertVisible](#assert-visible)
[assertPresent](#assert-present)
[assertNotPresent](#assert-not-present)
[assertMissing](#assert-missing)
[assertInputPresent](#assert-input-present)
[assertInputMissing](#assert-input-missing)
[assertDialogOpened](#assert-dialog-opened)
[assertEnabled](#assert-enabled)
[assertDisabled](#assert-disabled)
[assertButtonEnabled](#assert-button-enabled)
[assertButtonDisabled](#assert-button-disabled)
[assertFocused](#assert-focused)
[assertNotFocused](#assert-not-focused)
[assertAuthenticated](#assert-authenticated)
[assertGuest](#assert-guest)
[assertAuthenticatedAs](#assert-authenticated-as)
[assertVue](#assert-vue)
[assertVueIsNot](#assert-vue-is-not)
[assertVueContains](#assert-vue-contains)
[assertVueDoesntContain](#assert-vue-doesnt-contain)

</div>

<a name="assert-title"></a>
#### assertTitle

페이지 제목이 지정한 텍스트와 일치하는지 어설션합니다.

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### assertTitleContains

페이지 제목에 지정한 텍스트가 포함되어 있는지 어설션합니다.

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### assertUrlIs

현재 URL이 쿼리 문자열을 제외하고 지정한 문자열과 일치하는지 어설션합니다.

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### assertSchemeIs

현재 URL 스킴이 지정한 스킴과 일치하는지 어설션합니다.

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### assertSchemeIsNot

현재 URL 스킴이 지정한 스킴과 일치하지 않는지 어설션합니다.

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### assertHostIs

현재 URL 호스트가 지정한 호스트와 일치하는지 어설션합니다.

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### assertHostIsNot

현재 URL 호스트가 지정한 호스트와 일치하지 않는지 어설션합니다.

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### assertPortIs

현재 URL 포트가 지정한 포트와 일치하는지 어설션합니다.

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### assertPortIsNot

현재 URL 포트가 지정한 포트와 일치하지 않는지 어설션합니다.

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### assertPathBeginsWith

현재 URL 경로가 지정한 경로로 시작하는지 어설션합니다.

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

현재 URL 경로가 지정한 경로로 끝나는지 어설션합니다.

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### assertPathContains

현재 URL 경로에 지정한 경로가 포함되어 있는지 어설션합니다.

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### assertPathIs

현재 경로가 지정한 경로와 일치하는지 어설션합니다.

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### assertPathIsNot

현재 경로가 지정한 경로와 일치하지 않는지 어설션합니다.

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### assertRouteIs

현재 URL이 지정한 [이름이 지정된 라우트](/docs/13.x/routing#named-routes)의 URL과 일치하는지 어설션합니다.

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

지정한 쿼리 문자열 파라미터가 존재하는지 어설션합니다.

```php
$browser->assertQueryStringHas($name);
```

지정한 쿼리 문자열 파라미터가 존재하고 지정한 값을 가지는지 어설션합니다.

```php
$browser->assertQueryStringHas($name, $value);
```
<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

주어진 쿼리 문자열 파라미터가 없는지 확인합니다:

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### assertFragmentIs

URL의 현재 해시 프래그먼트가 주어진 프래그먼트와 일치하는지 확인합니다:

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### assertFragmentBeginsWith

URL의 현재 해시 프래그먼트가 주어진 프래그먼트로 시작하는지 확인합니다:

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### assertFragmentIsNot

URL의 현재 해시 프래그먼트가 주어진 프래그먼트와 일치하지 않는지 확인합니다:

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### assertHasCookie

주어진 암호화된 쿠키가 존재하는지 확인합니다:

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### assertHasPlainCookie

주어진 암호화되지 않은 쿠키가 존재하는지 확인합니다:

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### assertCookieMissing

주어진 암호화된 쿠키가 존재하지 않는지 확인합니다:

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

주어진 암호화되지 않은 쿠키가 존재하지 않는지 확인합니다:

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### assertCookieValue

암호화된 쿠키가 주어진 값을 가지는지 확인합니다:

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### assertPlainCookieValue

암호화되지 않은 쿠키가 주어진 값을 가지는지 확인합니다:

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### assertSee

주어진 텍스트가 페이지에 있는지 확인합니다:

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### assertDontSee

주어진 텍스트가 페이지에 없는지 확인합니다:

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### assertSeeIn

주어진 텍스트가 셀렉터 안에 있는지 확인합니다:

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### assertDontSeeIn

주어진 텍스트가 셀렉터 안에 없는지 확인합니다:

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### assertSeeAnythingIn

셀렉터 안에 어떤 텍스트든 존재하는지 확인합니다:

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### assertSeeNothingIn

셀렉터 안에 텍스트가 전혀 없는지 확인합니다:

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-count"></a>
#### assertCount

주어진 셀렉터와 일치하는 요소가 지정한 횟수만큼 나타나는지 확인합니다:

```php
$browser->assertCount($selector, $count);
```

<a name="assert-script"></a>
#### assertScript

주어진 JavaScript 표현식이 주어진 값으로 평가되는지 확인합니다:

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### assertSourceHas

주어진 소스 코드가 페이지에 있는지 확인합니다:

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### assertSourceMissing

주어진 소스 코드가 페이지에 없는지 확인합니다:

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### assertSeeLink

주어진 링크가 페이지에 있는지 확인합니다:

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### assertDontSeeLink

주어진 링크가 페이지에 없는지 확인합니다:

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### assertInputValue

주어진 입력 필드가 주어진 값을 가지는지 확인합니다:

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### assertInputValueIsNot

주어진 입력 필드가 주어진 값을 가지지 않는지 확인합니다:

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### assertChecked

주어진 체크박스가 선택되어 있는지 확인합니다:

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### assertNotChecked

주어진 체크박스가 선택되어 있지 않은지 확인합니다:

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### assertIndeterminate

주어진 체크박스가 미정 상태인지 확인합니다:

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### assertRadioSelected

주어진 라디오 필드가 선택되어 있는지 확인합니다:

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### assertRadioNotSelected

주어진 라디오 필드가 선택되어 있지 않은지 확인합니다:

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### assertSelected

주어진 드롭다운에서 주어진 값이 선택되어 있는지 확인합니다:

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### assertNotSelected

주어진 드롭다운에서 주어진 값이 선택되어 있지 않은지 확인합니다:

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

주어진 값 배열을 선택할 수 있는지 확인합니다:

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### assertSelectMissingOptions

주어진 값 배열을 선택할 수 없는지 확인합니다:

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

주어진 필드에서 주어진 값을 선택할 수 있는지 확인합니다:

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### assertSelectMissingOption

주어진 값을 선택할 수 없는지 확인합니다:

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### assertValue

주어진 셀렉터와 일치하는 요소가 주어진 값을 가지는지 확인합니다:

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### assertValueIsNot

주어진 셀렉터와 일치하는 요소가 주어진 값을 가지지 않는지 확인합니다:

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### assertAttribute

주어진 셀렉터와 일치하는 요소가 지정한 속성에 주어진 값을 가지고 있는지 확인합니다:

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### assertAttributeMissing

주어진 셀렉터와 일치하는 요소에 지정한 속성이 없는지 확인합니다:

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

주어진 셀렉터와 일치하는 요소의 지정한 속성에 주어진 값이 포함되어 있는지 확인합니다:

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

주어진 셀렉터와 일치하는 요소의 지정한 속성에 주어진 값이 포함되어 있지 않은지 확인합니다:

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### assertAriaAttribute

주어진 셀렉터와 일치하는 요소가 지정한 aria 속성에 주어진 값을 가지고 있는지 확인합니다:

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

예를 들어 `<button aria-label="Add"></button>` 마크업이 주어졌다면, 다음과 같이 `aria-label` 속성에 대해 확인할 수 있습니다:

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### assertDataAttribute

주어진 셀렉터와 일치하는 요소가 지정한 data 속성에 주어진 값을 가지고 있는지 확인합니다:

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

예를 들어 `<tr id="row-1" data-content="attendees"></tr>` 마크업이 주어졌다면, 다음과 같이 `data-content` 속성에 대해 확인할 수 있습니다:

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```
<a name="assert-visible"></a>
#### assertVisible

주어진 셀렉터와 일치하는 요소가 표시되는지 검증합니다:

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### assertPresent

주어진 셀렉터와 일치하는 요소가 소스에 존재하는지 검증합니다:

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### assertNotPresent

주어진 셀렉터와 일치하는 요소가 소스에 존재하지 않는지 검증합니다:

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### assertMissing

주어진 셀렉터와 일치하는 요소가 표시되지 않는지 검증합니다:

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### assertInputPresent

주어진 이름을 가진 input이 존재하는지 검증합니다:

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### assertInputMissing

주어진 이름을 가진 input이 소스에 존재하지 않는지 검증합니다:

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### assertDialogOpened

주어진 메시지를 가진 JavaScript 대화 상자가 열렸는지 검증합니다:

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### assertEnabled

주어진 필드가 활성화되어 있는지 검증합니다:

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### assertDisabled

주어진 필드가 비활성화되어 있는지 검증합니다:

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### assertButtonEnabled

주어진 버튼이 활성화되어 있는지 검증합니다:

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### assertButtonDisabled

주어진 버튼이 비활성화되어 있는지 검증합니다:

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### assertFocused

주어진 필드에 포커스가 있는지 검증합니다:

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### assertNotFocused

주어진 필드에 포커스가 없는지 검증합니다:

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 검증합니다:

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았는지 검증합니다:

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

사용자가 주어진 사용자로 인증되었는지 검증합니다:

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### assertVue

Dusk를 사용하면 [Vue 컴포넌트](https://vuejs.org) 데이터의 상태에 대해서도 검증을 수행할 수 있습니다. 예를 들어, 애플리케이션에 다음 Vue 컴포넌트가 포함되어 있다고 가정해 보겠습니다:

    // HTML...

    <profile dusk="profile-component"></profile>

    // Component Definition...

    Vue.component('profile', {
        template: '<div>{{ user.name }}</div>',

        data: function () {
            return {
                user: {
                    name: 'Taylor'
                }
            };
        }
    });

다음과 같이 Vue 컴포넌트의 상태를 검증할 수 있습니다:

```php tab=Pest
test('vue', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
});
```

```php tab=PHPUnit
/**
 * A basic Vue test example.
 */
public function test_vue(): void
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->assertVue('user.name', 'Taylor', '@profile-component');
    });
}
```

<a name="assert-vue-is-not"></a>
#### assertVueIsNot

주어진 Vue 컴포넌트 데이터 속성이 주어진 값과 일치하지 않는지 검증합니다:

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### assertVueContains

주어진 Vue 컴포넌트 데이터 속성이 배열이며 주어진 값을 포함하는지 검증합니다:

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

주어진 Vue 컴포넌트 데이터 속성이 배열이며 주어진 값을 포함하지 않는지 검증합니다:

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## 페이지 (Pages)

때로는 테스트에서 여러 복잡한 작업을 순서대로 수행해야 합니다. 이로 인해 테스트를 읽고 이해하기가 더 어려워질 수 있습니다. Dusk 페이지를 사용하면 표현력 있는 작업을 정의한 뒤, 단일 메서드로 특정 페이지에서 그 작업을 수행할 수 있습니다. 또한 페이지를 사용하면 애플리케이션 전체 또는 단일 페이지에서 자주 사용하는 셀렉터에 대한 단축 이름을 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성

페이지 객체를 생성하려면 `dusk:page` Artisan 명령어를 실행합니다. 모든 페이지 객체는 애플리케이션의 `tests/Browser/Pages` 디렉터리에 배치됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정

기본적으로 페이지에는 `url`, `assert`, `elements` 세 가지 메서드가 있습니다. 먼저 `url` 및 `assert` 메서드를 살펴보겠습니다. `elements` 메서드는 [아래에서 더 자세히 설명합니다](#shorthand-selectors).

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지를 나타내는 URL의 경로를 반환해야 합니다. Dusk는 브라우저에서 해당 페이지로 이동할 때 이 URL을 사용합니다:

```php
/**
 * Get the URL for the page.
 */
public function url(): string
{
    return '/login';
}
```

<a name="the-assert-method"></a>
#### `assert` 메서드

`assert` 메서드는 브라우저가 실제로 주어진 페이지에 있는지 확인하는 데 필요한 모든 검증을 수행할 수 있습니다. 이 메서드 안에 반드시 무언가를 넣어야 하는 것은 아닙니다. 하지만 원한다면 이러한 검증을 자유롭게 추가할 수 있습니다. 이 검증은 페이지로 이동할 때 자동으로 실행됩니다:

```php
/**
 * Assert that the browser is on the page.
 */
public function assert(Browser $browser): void
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
### 페이지로 이동하기

페이지가 정의되면 `visit` 메서드를 사용하여 해당 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

때로는 이미 특정 페이지에 있는 상태에서, 그 페이지의 셀렉터와 메서드를 현재 테스트 컨텍스트에 "로드"해야 할 수 있습니다. 예를 들어 버튼을 누른 뒤 명시적으로 이동하지 않았지만 특정 페이지로 리다이렉트되는 경우에 흔히 발생합니다. 이런 상황에서는 `on` 메서드를 사용하여 페이지를 로드할 수 있습니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 단축 셀렉터

페이지 클래스 안의 `elements` 메서드를 사용하면 페이지의 어떤 CSS 셀렉터든 빠르고 기억하기 쉬운 단축 이름으로 정의할 수 있습니다. 예를 들어, 애플리케이션 로그인 페이지의 "email" input 필드에 대한 단축 이름을 정의해 보겠습니다:

```php
/**
 * Get the element shortcuts for the page.
 *
 * @return array<string, string>
 */
public function elements(): array
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

단축 이름이 정의되면, 일반적으로 전체 CSS 셀렉터를 사용하는 모든 위치에서 이 단축 셀렉터를 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 단축 셀렉터

Dusk를 설치하면 기본 `Page` 클래스가 `tests/Browser/Pages` 디렉터리에 배치됩니다. 이 클래스에는 `siteElements` 메서드가 포함되어 있으며, 애플리케이션 전체의 모든 페이지에서 사용할 수 있는 전역 단축 셀렉터를 정의하는 데 사용할 수 있습니다:

```php
/**
 * Get the global element shortcuts for the site.
 *
 * @return array<string, string>
 */
public static function siteElements(): array
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
### 페이지 메서드

페이지에 기본으로 정의된 메서드 외에도, 테스트 전반에서 사용할 추가 메서드를 정의할 수 있습니다. 예를 들어 음악 관리 애플리케이션을 만들고 있다고 가정해 보겠습니다. 애플리케이션의 한 페이지에서 흔히 수행하는 작업은 플레이리스트를 생성하는 것일 수 있습니다. 각 테스트마다 플레이리스트를 생성하는 로직을 다시 작성하는 대신, 페이지 클래스에 `createPlaylist` 메서드를 정의할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // Other page methods...

    /**
     * Create a new playlist.
     */
    public function createPlaylist(Browser $browser, string $name): void
    {
        $browser->type('name', $name)
            ->check('share')
            ->press('Create Playlist');
    }
}
```

메서드가 정의되면 해당 페이지를 사용하는 어떤 테스트에서도 이 메서드를 사용할 수 있습니다. 브라우저 인스턴스는 사용자 정의 페이지 메서드의 첫 번째 인수로 자동 전달됩니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 "페이지 객체"와 비슷하지만, 내비게이션 바나 알림 창처럼 애플리케이션 전반에서 재사용되는 UI 및 기능 조각을 위한 것입니다. 따라서 컴포넌트는 특정 URL에 묶이지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성

컴포넌트를 생성하려면 `dusk:component` Artisan 명령어를 실행합니다. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 배치됩니다:

```shell
php artisan dusk:component DatePicker
```

위에서 보았듯이 "date picker"는 애플리케이션의 여러 페이지에서 존재할 수 있는 컴포넌트의 예입니다. 테스트 스위트의 수십 개 테스트에서 날짜를 선택하기 위한 브라우저 자동화 로직을 직접 작성하는 일은 번거로워질 수 있습니다. 대신 날짜 선택기를 나타내는 Dusk 컴포넌트를 정의하여, 해당 로직을 컴포넌트 안에 캡슐화할 수 있습니다:

```php
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * Get the root selector for the component.
     */
    public function selector(): string
    {
        return '.date-picker';
    }

    /**
     * Assert that the browser page contains the component.
     */
    public function assert(Browser $browser): void
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * Get the element shortcuts for the component.
     *
     * @return array<string, string>
     */
    public function elements(): array
    {
        return [
            '@date-field' => 'input.datepicker-input',
            '@year-list' => 'div > div.datepicker-years',
            '@month-list' => 'div > div.datepicker-months',
            '@day-list' => 'div > div.datepicker-days',
        ];
    }

    /**
     * Select the given date.
     */
    public function selectDate(Browser $browser, int $year, int $month, int $day): void
    {
        $browser->click('@date-field')
            ->within('@year-list', function (Browser $browser) use ($year) {
                $browser->click($year);
            })
            ->within('@month-list', function (Browser $browser) use ($month) {
                $browser->click($month);
            })
            ->within('@day-list', function (Browser $browser) use ($day) {
                $browser->click($day);
            });
    }
}
```
<a name="using-components"></a>
### 컴포넌트 사용

컴포넌트를 정의한 후에는 어떤 테스트에서든 날짜 선택기 안에서 쉽게 날짜를 선택할 수 있습니다. 그리고 날짜를 선택하는 데 필요한 로직이 변경되더라도 컴포넌트만 업데이트하면 됩니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;

pest()->use(DatabaseMigrations::class);

test('basic example', function () {
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
            ->within(new DatePicker, function (Browser $browser) {
                $browser->selectDate(2019, 1, 30);
            })
            ->assertSee('January');
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Browser;

use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\Browser\Components\DatePicker;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    /**
     * A basic component test example.
     */
    public function test_basic_example(): void
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                ->within(new DatePicker, function (Browser $browser) {
                    $browser->selectDate(2019, 1, 30);
                })
                ->assertSee('January');
        });
    }
}
```

`component` 메서드를 사용하면 지정한 컴포넌트 범위로 제한된 브라우저 인스턴스를 가져올 수 있습니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합 (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk 지속적 통합 구성은 Laravel 애플리케이션이 8000번 포트에서 PHP 내장 개발 서버를 사용해 서비스된다고 가정합니다. 따라서 계속하기 전에 지속적 통합 환경의 `APP_URL` 환경 변수 값이 `http://127.0.0.1:8000`인지 확인해야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 다음 Google Chrome buildpack과 스크립트를 Heroku `app.json` 파일에 추가하십시오:

```json
{
  "environments": {
    "test": {
      "buildpacks": [
        { "url": "heroku/php" },
        { "url": "https://github.com/heroku/heroku-buildpack-chrome-for-testing" }
      ],
      "scripts": {
        "test-setup": "cp .env.testing .env",
        "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux --port=9515 > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk"
      }
    }
  }
}
```

<a name="running-tests-on-travis-ci"></a>
### Travis CI

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 다음 `.travis.yml` 구성을 사용하십시오. Travis CI는 그래픽 환경이 아니므로 Chrome 브라우저를 실행하기 위해 몇 가지 추가 단계가 필요합니다. 또한 PHP의 내장 웹 서버를 실행하기 위해 `php artisan serve`를 사용합니다:

```yaml
language: php

php:
  - 8.2

addons:
  chrome: stable

install:
  - cp .env.testing .env
  - travis_retry composer install --no-interaction --prefer-dist
  - php artisan key:generate
  - php artisan dusk:chrome-driver

before_script:
  - google-chrome-stable --headless --disable-gpu --remote-debugging-port=9222 http://localhost &
  - php artisan serve --no-reload &

script:
  - php artisan dusk
```

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

[GitHub Actions](https://github.com/features/actions)를 사용해 Dusk 테스트를 실행한다면 다음 구성 파일을 시작점으로 사용할 수 있습니다. TravisCI와 마찬가지로 PHP의 내장 웹 서버를 실행하기 위해 `php artisan serve` 명령어를 사용합니다:

```yaml
name: CI
on: [push]
jobs:

  dusk-php:
    runs-on: ubuntu-latest
    env:
      APP_URL: "http://127.0.0.1:8000"
      DB_USERNAME: root
      DB_PASSWORD: root
      MAIL_MAILER: log
    steps:
      - uses: actions/checkout@v5
      - name: Prepare The Environment
        run: cp .env.example .env
      - name: Create Database
        run: |
          sudo systemctl start mysql
          mysql --user="root" --password="root" -e "CREATE DATABASE \`my-database\` character set UTF8mb4 collate utf8mb4_bin;"
      - name: Install Composer Dependencies
        run: composer install --no-progress --prefer-dist --optimize-autoloader
      - name: Generate Application Key
        run: php artisan key:generate
      - name: Upgrade Chrome Driver
        run: php artisan dusk:chrome-driver --detect
      - name: Start Chrome Driver
        run: ./vendor/laravel/dusk/bin/chromedriver-linux --port=9515 &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        run: php artisan dusk
      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: screenshots
          path: tests/Browser/screenshots
      - name: Upload Console Logs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: console
          path: tests/Browser/console
```

<a name="running-tests-on-chipper-ci"></a>
### Chipper CI

[Chipper CI](https://chipperci.com)를 사용해 Dusk 테스트를 실행한다면 다음 구성 파일을 시작점으로 사용할 수 있습니다. 요청을 받을 수 있도록 PHP의 내장 서버를 사용해 Laravel을 실행합니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Include Chrome in the build environment
services:
  - dusk

# Build all commits
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate

      # Create a dusk env file, ensuring APP_URL uses BUILD_HOST
      cp -v .env .env.dusk.ci
      sed -i "s@APP_URL=.*@APP_URL=http://$BUILD_HOST:8000@g" .env.dusk.ci

  - name: Compile Assets
    cmd: |
      npm ci --no-audit
      npm run build

  - name: Browser Tests
    cmd: |
      php -S [::0]:8000 -t public 2>server.log &
      sleep 2
      php artisan dusk:chrome-driver $CHROME_DRIVER
      php artisan dusk --env=ci
```

데이터베이스 사용 방법을 포함하여 Chipper CI에서 Dusk 테스트를 실행하는 방법을 더 알아보려면 [공식 Chipper CI 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하십시오.
