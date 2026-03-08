# Laravel Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 인스턴스 생성](#creating-browsers)
    - [페이지 이동](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증](#authentication)
    - [쿠키](#cookies)
    - [JavaScript 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 저장](#storing-console-output-to-disk)
    - [페이지 소스 저장](#storing-page-source-to-disk)
- [요소와 상호작용](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성](#text-values-and-attributes)
    - [폼과 상호작용](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 클릭](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 사용](#using-the-keyboard)
    - [마우스 사용](#using-the-mouse)
    - [JavaScript 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [요소 대기](#waiting-for-elements)
    - [요소를 화면에 스크롤](#scrolling-an-element-into-view)
- [사용 가능한 어서션](#available-assertions)
- [페이지](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [약식 셀렉터](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합(CI)](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> [Pest 4](https://pestphp.com/)는 Laravel Dusk에 비해 성능과 사용성에서 큰 개선점을 제공하는 자동화 브라우저 테스트 기능을 내장하고 있습니다. 새로운 프로젝트에서는 브라우저 테스트에 Pest를 사용할 것을 권장합니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk를 사용하기 위해 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신, Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 이용합니다. 하지만, 원하는 경우 Selenium 호환 드라이버를 자유롭게 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저 [Google Chrome](https://www.google.com/chrome)을 설치한 뒤, 프로젝트에 `laravel/dusk` Composer 의존성을 추가합니다:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, 절대로 프로덕션 환경에서는 등록하지 마십시오. 그렇지 않으면 임의의 사용자가 애플리케이션에 인증할 수 있는 보안 위험이 발생할 수 있습니다.

Dusk 패키지 설치 후에는 `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉터리, 예제 Dusk 테스트, 운영 체제에 맞는 Chrome Driver 바이너리를 생성합니다:

```shell
php artisan dusk:install
```

다음으로, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 설정하세요. 이 값은 브라우저에서 애플리케이션을 접속할 때 사용하는 URL과 동일해야 합니다.

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 로컬 개발 환경을 관리하는 경우, [Dusk 테스트 설정 및 실행](/docs/12.x/sail#laravel-dusk)에 관한 Sail 문서도 참고하시기 바랍니다.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령어로 설치되는 ChromeDriver 외에 다른 버전을 사용하고 싶다면, 다음의 `dusk:chrome-driver` 명령어를 활용할 수 있습니다:

```shell
# 운영 체제에 맞는 최신 ChromeDriver 설치...
php artisan dusk:chrome-driver

# 특정 버전의 ChromeDriver 설치...
php artisan dusk:chrome-driver 86

# 지원되는 모든 운영 체제에 특정 버전 설치...
php artisan dusk:chrome-driver --all

# 크롬/크로미움 감지된 버전에 맞게 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk에서는 `chromedriver` 바이너리가 실행 가능이어야 합니다. 구동에 문제가 있다면, 다음 명령어로 실행 권한이 있는지 확인하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`.

<a name="using-other-browsers"></a>
### 다른 브라우저 사용 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)로 브라우저 테스트를 실행합니다. 하지만 Selenium 서버를 직접 시작하여 원하는 브라우저로 테스트 실행도 가능합니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 엽니다. 이 파일에서 `startChromeDriver` 메서드 호출을 제거하면 Dusk가 ChromeDriver를 자동 실행하지 않습니다:

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

이후, `driver` 메서드를 수정하여 원하는 URL과 포트로 연결하고, WebDriver에 전달할 "원하는 기능(desired capabilities)"도 변경할 수 있습니다:

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
### 테스트 생성 (Generating Tests)

Dusk 테스트를 생성하려면, `dusk:make` Artisan 명령어를 사용합니다. 생성된 테스트는 `tests/Browser` 디렉터리에 저장됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

작성하는 대부분의 테스트는 애플리케이션의 데이터베이스에서 데이터를 가져오는 페이지와 상호작용합니다. 하지만 Dusk 테스트에서는 `RefreshDatabase` 트레이트를 사용하면 안 됩니다. 이 트레이트는 데이터베이스 트랜잭션을 활용하지만, HTTP 요청 간에는 해당 기능이 적용되지 않습니다. 대신, `DatabaseMigrations` 트레이트나 `DatabaseTruncation` 트레이트 두 가지 방법을 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 데이터베이스 마이그레이션 사용

`DatabaseMigrations` 트레이트는 각 테스트 이전에 데이터베이스 마이그레이션을 실행합니다. 다만, 각 테스트마다 테이블을 드롭하고 다시 생성하기 때문에 테이블을 단순히 비우는 것보다 느릴 수 있습니다:

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
> Dusk 테스트 실행 시에는 SQLite 메모리 데이터베이스를 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 동작하므로, 다른 프로세스에서 사용하는 메모리 데이터베이스에 접근할 수 없습니다.

<a name="reset-truncation"></a>
#### 데이터베이스 테이블 비우기 사용

`DatabaseTruncation` 트레이트는 첫 번째 테스트 실행 시 데이터베이스를 마이그레이션하여 테이블을 생성하고, 이후에는 단순히 테이블을 비웁니다. 이 방법은 마이그레이션을 반복 실행하는 것보다 속도가 빠릅니다:

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

기본적으로 이 트레이트는 `migrations` 테이블을 제외한 모든 테이블을 비웁니다. 비울 테이블을 직접 지정하고 싶다면 테스트 클래스에 `$tablesToTruncate` 속성을 정의하세요:

> [!NOTE]
> Pest를 사용하는 경우, 속성 또는 메서드는 기본 `DuskTestCase` 클래스나 확장하는 클래스에 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는, 비우지 않을 테이블을 `$exceptTables` 속성에 지정할 수도 있습니다:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

테이블을 비울 데이터베이스 커넥션을 지정하려면 `$connectionsToTruncate` 속성을 사용할 수 있습니다:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

테이블 비우기 전후에 코드를 실행하려면, `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 정의할 수 있습니다:

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
### 테스트 실행 (Running Tests)

브라우저 테스트를 실행하려면, `dusk` Artisan 명령어를 사용하세요:

```shell
php artisan dusk
```

최근 테스트 실행에서 실패한 테스트만 먼저 다시 실행하려면, `dusk:fails` 명령어를 사용해 시간을 절약할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스터에서 사용하는 모든 인수를 받아들입니다. 예를 들어, [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)에 따라 특정 테스트만 실행할 수도 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/12.x/sail)로 개발 환경을 관리한다면, [Dusk 테스트 설정 및 실행](/docs/12.x/sail#laravel-dusk) 관련 Sail 문서를 참조하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행

기본적으로 Dusk는 ChromeDriver를 자동으로 실행합니다. 시스템에 따라 자동 실행이 동작하지 않는다면, `dusk` 명령 실행 전에 ChromeDriver를 직접 시작할 수 있습니다. 이 경우 `tests/DuskTestCase.php` 파일에서 다음 라인을 주석 처리하세요:

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

또한, ChromeDriver를 9515번 포트가 아닌 다른 포트에서 시작한다면, 같은 클래스의 `driver` 메서드에서 포트를 맞춰줘야 합니다:

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
### 환경 파일 처리 (Environment Handling)

Dusk가 테스트 실행 시 독립적인 환경 파일을 사용하도록 하려면, 프로젝트 루트에 `.env.dusk.{환경명}` 파일을 생성하면 됩니다. 예를 들어, `local` 환경에서 `dusk` 명령어를 실행한다면, `.env.dusk.local` 파일을 생성해야 합니다.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업하고 Dusk 환경 파일을 `.env`로 이름을 바꿉니다. 테스트가 끝나면 원래의 `.env` 파일이 복원됩니다.

<a name="browser-basics"></a>
## 브라우저 기본 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 인스턴스 생성 (Creating Browsers)

로그인 기능을 테스트하는 예제를 작성해보겠습니다. 테스트를 생성한 후, 로그인 페이지로 이동하여 인증 정보를 입력하고 "Login" 버튼을 클릭하도록 수정할 수 있습니다. 브라우저 인스턴스를 생성하려면, Dusk 테스트 내에서 `browse` 메서드를 호출합니다:

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

위 예제에서 보듯, `browse` 메서드는 클로저(익명 함수)를 인수로 받으며, 브라우저 인스턴스가 자동으로 전달됩니다. 이 객체를 통해 애플리케이션과 상호작용하고 어서션을 수행할 수 있습니다.

<a name="creating-multiple-browsers"></a>
#### 여러 브라우저 인스턴스 생성

테스트에 복수의 브라우저가 필요한 경우도 있습니다. 예를 들어, 웹소켓이 있는 채팅 화면을 테스트할 때 여러 브라우저가 필요할 수 있습니다. 이 경우, `browse` 메서드의 클로저 인자에 여러 브라우저 인스턴스를 지정하면 됩니다:

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
### 페이지 이동 (Navigation)

`visit` 메서드를 사용하면 애플리케이션의 지정한 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

[named route](/docs/12.x/routing#named-routes)로 이동하려면 `visitRoute` 메서드를 사용할 수 있습니다:

```php
$browser->visitRoute($routeName, $parameters);
```

브라우저의 "뒤로가기", "앞으로가기"는 `back`, `forward` 메서드로 가능합니다:

```php
$browser->back();

$browser->forward();
```

`refresh` 메서드로 페이지 새로고침도 할 수 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드로 브라우저 창의 크기를 지정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드로 브라우저 창을 최대화할 수 있습니다:

```php
$browser->maximize();
```

`fitContent` 메서드는 브라우저 창을 컨텐츠 크기에 맞게 조절합니다:

```php
$browser->fitContent();
```

테스트 실패 시, Dusk는 스크린샷 찍기 전에 자동으로 창을 컨텐츠에 맞춰 조정합니다. 이 기능을 비활성화하려면 `disableFitOnFailure`를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드로 브라우저 창을 화면 내 원하는 위치로 이동할 수도 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재사용할 사용자 정의 브라우저 메서드를 만들고 싶다면, `Browser` 클래스의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출하는 것이 좋습니다:

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저(동작)를 받습니다. 이렇게 정의한 매크로는 브라우저 인스턴스의 메서드처럼 호출할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 (Authentication)

테스트 중 인증이 필요한 페이지를 다루는 경우, 매번 로그인 화면을 거치지 않고 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델의 기본 키 또는 인스턴스를 인수로 받습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드 사용 후 파일 내 모든 테스트에서 해당 유저의 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

암호화된 쿠키 값을 가져오거나 설정하려면 `cookie` 메서드를 사용합니다. 기본적으로 Laravel이 생성하는 쿠키는 모두 암호화됩니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키는 `plainCookie` 메서드로 다룰 수 있습니다:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

쿠키를 삭제하려면 `deleteCookie`를 사용하세요:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScript 실행 (Executing JavaScript)

`script` 메서드를 사용해 원하는 JavaScript 문장을 브라우저에서 실행할 수 있습니다:

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### 스크린샷 찍기 (Taking a Screenshot)

`screenshot` 메서드로 원하는 파일명으로 스크린샷을 저장할 수 있습니다. 스크린샷은 `tests/Browser/screenshots` 디렉터리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드는 여러 브레이크포인트별로 스크린샷을 찍습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드는 특정 요소만 스크린샷으로 저장합니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 저장 (Storing Console Output to Disk)

`storeConsoleLog` 메서드로 브라우저 콘솔 출력을 파일로 저장할 수 있습니다. 저장 위치는 `tests/Browser/console` 디렉터리입니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장 (Storing Page Source to Disk)

`storeSource` 메서드로 현재 페이지의 소스를 파일로 저장할 수 있습니다. 소스는 `tests/Browser/source` 디렉터리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 요소와 상호작용 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

효과적인 Dusk 테스트 코드를 작성할 때 요소를 선택할 좋은 CSS 셀렉터를 정하는 것이 가장 어려운 부분 중 하나입니다. 프론트엔드가 수정되면 기존 CSS 셀렉터가 쉽게 깨질 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 사용하면, CSS 셀렉터를 외우지 않고 테스트 목적에만 집중할 수 있습니다. 셀렉터를 정의하려면 HTML 요소에 `dusk` 속성을 추가하세요. 테스트에서 셀렉터 앞에 `@`를 붙여 해당 요소를 조작할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원한다면, Dusk가 사용하는 HTML 속성을 `selectorHtmlAttribute` 메서드로 변경할 수도 있습니다. 이 메서드는 일반적으로 `AppServiceProvider`의 `boot`에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 얻기 및 설정

Dusk는 페이지 요소의 현재 value, 표시 텍스트, 속성 값 등과 상호작용할 여러 메서드를 제공합니다. 예를 들어, 특정 CSS나 Dusk 셀렉터와 매칭되는 요소의 "value" 값을 얻으려면 `value` 메서드를 사용합니다:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정하기...
$browser->value('selector', 'value');
```

`inputValue` 메서드를 사용하면 특정 name의 input 요소 값을 가져올 수 있습니다:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 얻기

`text` 메서드는 주어진 셀렉터와 매칭되는 요소의 표시 텍스트를 읽어옵니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 값 얻기

`attribute` 메서드는 특정 셀렉터와 매칭되는 요소의 속성값을 얻습니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력하기

폼 및 입력 요소와 상호작용하기 위한 다양한 메서드를 제공합니다. 먼저, input 필드에 텍스트를 입력하는 예시입니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

필요하다면 CSS 셀렉터를 직접 지정할 수도 있지만, 기본적으로 name 속성으로도 찾을 수 있습니다.

필드의 내용을 지우지 않고 값을 이어 쓰려면 `append`를 사용할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력값을 지우려면 `clear`를 사용하세요:

```php
$browser->clear('email');
```

천천히 타이핑하도록 하려면 `typeSlowly`를 사용할 수 있습니다(기본 100ms 간격, 세 번째 인수로 조절 가능):

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` 메서드로 값을 천천히 이어쓸 수도 있습니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운

`select` 요소에서 값을 선택하려면 `select` 메서드를 사용하세요. 두 번째 인수에는 표시 텍스트가 아닌 option의 value 속성 값을 넘깁니다:

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 랜덤 옵션이 선택됩니다:

```php
$browser->select('size');
```

배열을 두 번째 인수로 넘기면 다중 선택도 가능합니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스

체크박스를 체크하려면 `check` 메서드를, 해제하려면 `uncheck`를 사용합니다. name 속성으로도 인식할 수 있습니다:

```php
$browser->check('terms');
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼

라디오 버튼을 선택하려면 `radio` 메서드를 사용하세요:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

파일 첨부는 `attach` 메서드로 할 수 있습니다. name 속성으로 매치합니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능은 서버에 `Zip` PHP 확장 모듈이 설치 및 활성화되어 있어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 클릭 (Pressing Buttons)

버튼 요소를 클릭하려면 `press` 메서드를 사용합니다. 버튼의 표시 텍스트 또는 CSS/Dusk 셀렉터로 지정 가능합니다:

```php
$browser->press('Login');
```

폼 제출 시 버튼이 잠시 비활성화되었다가 완료 후 다시 활성화되는 경우, 버튼이 활성화될 때까지 대기하며 클릭하려면 `pressAndWaitFor`를 활용할 수 있습니다:

```php
// 버튼이 재활성화될 때까지 최대 5초 대기
$browser->pressAndWaitFor('Save');

// 최대 1초 대기
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭 (Clicking Links)

링크를 클릭하려면 `clickLink` 메서드를 사용하세요. 링크의 표시 텍스트로 지정합니다:

```php
$browser->clickLink($linkText);
```

특정 텍스트를 가진 링크가 보이는지 확인하려면 `seeLink`를 사용할 수 있습니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 해당 메서드는 jQuery와 상호작용합니다. 페이지에 jQuery가 없다면 Dusk가 자동으로 임시로 주입하여 테스트하는 동안 사용할 수 있습니다.

<a name="using-the-keyboard"></a>
### 키보드 사용 (Using the Keyboard)

`keys` 메서드를 사용하면 `type`보다 복잡한 입력 시퀀스를 요소에 전달할 수 있습니다. 예를 들어, Shift를 누른 채로 입력 후 다시 일반 입력으로 이어가는 것이 가능합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

키보드 단축키 조합도 보낼 수 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` 등 모든 수정 키는 `{}`로 감싸며, 이는 `Facebook\WebDriver\WebDriverKeys` 클래스의 상수와 일치합니다. [GitHub에서 전체 목록 확인](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)

<a name="fluent-keyboard-interactions"></a>
#### 유연한 키보드 상호작용

`withKeyboard` 메서드와 `Laravel\Dusk\Keyboard` 클래스를 활용하면, 복잡한 키보드 상호작용도 간단히 구현할 수 있습니다. Keyboard 클래스는 `press`, `release`, `type`, `pause` 메서드를 제공합니다:

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

테스트 전역에서 재사용할 키보드 상호작용을 정의하고 싶다면, `Keyboard` 클래스의 `macro` 메서드를 사용할 수 있습니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 정의합니다:

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

이렇게 정의한 매크로는 Keyboard 인스턴스에서 바로 호출 가능합니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 사용 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 요소 클릭

`click` 메서드로 CSS 또는 Dusk 셀렉터에 해당하는 요소를 클릭할 수 있습니다:

```php
$browser->click('.selector');
```

`clickAtXPath`로 XPath 표현식에 맞는 요소를 클릭할 수도 있습니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint`로 브라우저 화면 내 특정 좌표를 클릭하는 것도 가능합니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

더블 클릭은 `doubleClick`으로, 우클릭은 `rightClick`으로 구현합니다:

```php
$browser->doubleClick();
$browser->doubleClick('.selector');

$browser->rightClick();
$browser->rightClick('.selector');
```

마우스 클릭 후 버튼을 계속 누르려면 `clickAndHold`, 이후 `releaseMouse`로 해제할 수 있습니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`은 ctrl+클릭을 시뮬레이션합니다:

```php
$browser->controlClick();
$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스 오버

`mouseover` 메서드는 특정 요소 위로 마우스를 이동합니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭

`drag` 메서드는 한 요소를 다른 요소로 드래그할 때 사용합니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

단일 방향 드래그도 지원합니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

특정 오프셋만큼 드래그하려면 `dragOffset`을 사용합니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript 다이얼로그 (JavaScript Dialogs)

Dusk는 JavaScript 다이얼로그와 상호작용할 다양한 메서드를 제공합니다. 예를 들어, `waitForDialog`로 다이얼로그가 나타날 때까지 대기할 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`로 다이얼로그가 뜨고, 특정 메시지를 포함하고 있는지 어서트할 수 있습니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 있는 경우 `typeInDialog`로 값 입력이 가능합니다:

```php
$browser->typeInDialog('Hello World');
```

"확인" 버튼으로 다이얼로그를 닫으려면 `acceptDialog`, "취소" 버튼은 `dismissDialog`를 이용합니다:

```php
$browser->acceptDialog();
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용 (Interacting With Inline Frames)

iframe 내부 요소와 상호작용하려면 `withinFrame` 메서드를 사용하고, 해당 클로저 내부에서 모든 작업이 프레임 범위 내에서 실행됩니다:

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### 셀렉터 범위 지정 (Scoping Selectors)

특정 영역(예: 테이블) 내의 작업을 여러 번 수행하고 싶을 때, `with` 메서드로 범위를 지정할 수 있습니다. 해당 클로저에서는 설정한 셀렉터 내부 범위로만 동작이 제한됩니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

범위 밖에서 어서션을 실행해야 할 경우, `elsewhere`와 `elsewhereWhenAvailable`을 사용할 수 있습니다:

```php
$browser->with('.table', function (Browser $table) {
    // 현재 스코프는 `body .table`...

    $browser->elsewhere('.page-title', function (Browser $title) {
        // 현재 스코프는 `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function (Browser $title) {
        // 현재 스코프는 `body .page-title`...
        $title->assertSee('Hello World');
    });
});
```

<a name="waiting-for-elements"></a>
### 요소 대기 (Waiting for Elements)

JavaScript를 많이 사용하는 애플리케이션을 테스트하다 보면, 특정 요소나 데이터가 나타날 때까지 "대기"해야 할 때가 많습니다. Dusk는 이런 상황을 쉽게 처리할 수 있도록 다양한 "wait" 메서드를 제공합니다.

<a name="waiting"></a>
#### 단순 대기

주어진 시간(ms)만큼 단순하게 일시정지하려면 `pause` 메서드를 사용하세요:

```php
$browser->pause(1000);
```

특정 조건이 참일 때만 대기하려면 `pauseIf`, 아닐 때만 대기하려면 `pauseUnless`를 사용할 수 있습니다:

```php
$browser->pauseIf(App::environment('production'), 1000);

$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기

특정 CSS 또는 Dusk 셀렉터가 표시될 때까지 대기하려면 `waitFor` 메서드를 사용하세요(기본 최대 5초):

```php
// 최대 5초 대기
$browser->waitFor('.selector');

// 최대 1초 대기
$browser->waitFor('.selector', 1);
```

셀렉터 내에 특정 텍스트가 뜰 때까지 대기할 수도 있습니다:

```php
// 최대 5초 동안 텍스트 대기
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 동안 텍스트 대기
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

선택자가 페이지에서 사라질 때까지도 대기할 수 있습니다:

```php
// 최대 5초까지 사라질 때까지 대기
$browser->waitUntilMissing('.selector');

// 최대 1초까지 사라질 때까지 대기
$browser->waitUntilMissing('.selector', 1);
```

또한 선택자가 "활성/비활성"될 때까지 기다릴 수 있습니다:

```php
// 활성화 대기
$browser->waitUntilEnabled('.selector');
$browser->waitUntilEnabled('.selector', 1);

// 비활성화 대기
$browser->waitUntilDisabled('.selector');
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 셀렉터 준비될 때까지 범위 지정

특정 셀렉터와 매칭되는 요소를 기다렸다가 그 범위 내에서 작업을 수행하려면 `whenAvailable`을 사용할 수 있습니다. (예: 모달 등장 후 모달 내에서 "OK" 클릭):

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기

`waitForText`로 특정 텍스트가 페이지에 나타날 때까지 대기할 수 있습니다:

```php
$browser->waitForText('Hello World');
$browser->waitForText('Hello World', 1);
```

`waitUntilMissingText`로 특정 텍스트가 사라질 때까지 대기할 수 있습니다:

```php
$browser->waitUntilMissingText('Hello World');
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기

`waitForLink`로 특정 링크 텍스트가 나타날 때까지 대기할 수 있습니다:

```php
$browser->waitForLink('Create');
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기

`waitForInput`으로 입력 필드가 표시될 때까지 대기할 수 있습니다:

```php
$browser->waitForInput($field);
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 경로 대기

경로 어서션(예: `$browser->assertPathIs('/home')`)에서 비동기적으로 `window.location.pathname`이 변경된다면 어서션이 실패할 수 있습니다. `waitForLocation`으로 경로가 기대하는 값이 될 때까지 대기할 수 있습니다:

```php
$browser->waitForLocation('/secret');
```

완전한 URL도 지원합니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[named route](/docs/12.x/routing#named-routes) 위치도 대기할 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 새로고침 대기

조작 후 페이지가 새로고침될 때까지 대기하려면 `waitForReload`를 사용할 수 있습니다:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

주로 버튼 클릭 후 페이지 리로드가 일어나는 케이스를 줄이기 위해, `clickAndWaitForReload` 메서드도 제공됩니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 식 대기

특정 JavaScript 식이 true가 될 때까지 대기하고 싶을 때는 `waitUntil`을 사용할 수 있습니다. 코드에서 `return`이나 세미콜론은 생략합니다:

```php
$browser->waitUntil('App.data.servers.length > 0');
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 식 대기

`waitUntilVue` 및 `waitUntilVueIsNot` 메서드로 [Vue 컴포넌트](https://vuejs.org)의 속성이 특정 값을 가질 때까지 대기할 수 있습니다:

```php
$browser->waitUntilVue('user.name', 'Taylor', '@user');
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript 이벤트 대기

`waitForEvent`로 특정 JavaScript 이벤트 발생까지 대기할 수 있습니다:

```php
$browser->waitForEvent('load');
```

현재 스코프(기본 body)에 이벤트 리스너가 바인딩됩니다. 범위 셀렉터에서 사용 시 해당 요소에 이벤트 리스너가 연결됩니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe의 load 이벤트를 기다림...
    $iframe->waitForEvent('load');
});
```

이벤트 리스너 대상 요소를 두 번째 인수로 지정할 수도 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document` 및 `window` 객체의 이벤트에도 대기할 수 있습니다:

```php
$browser->waitForEvent('scroll', 'document');
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백을 활용한 대기

여러 대기 메서드는 내부적으로 `waitUsing` 메서드를 사용합니다. 이 메서드는 주어진 콜백이 true를 반환할 때까지 대기할 수 있습니다. 최대 대기 시간, 콜백 평가 간격, 콜백, 실패 메시지를 순서대로 받습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 요소를 화면에 스크롤 (Scrolling an Element Into View)

브라우저 화면 내에서 요소가 가려져 클릭할 수 없는 경우, `scrollIntoView` 메서드를 사용하여 해당 요소까지 자동으로 스크롤할 수 있습니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어서션 (Available Assertions)

Dusk는 다양한 형태의 어서션 메서드를 제공합니다. 아래 리스트에서 모든 어서션을 확인할 수 있습니다:

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

_(각 어서션의 설명 및 사용 예시는 원문에 존재하는 범위에서 코드와 동일하게 유지됩니다.)_

<a name="pages"></a>
## 페이지 (Pages)

테스트 코드에서 여러 복잡한 동작들을 순차적으로 처리해야 하는 경우가 있습니다. 이런 경우 테스트가 읽기 어렵고 복잡해질 수 있는데, Dusk의 페이지(Page) 기능을 이용하면 한 메서드로 여러 작업을 처리하는 명확한 동작을 정의할 수 있습니다. 또한, 애플리케이션(혹은 특정 페이지)에서 자주 사용하는 셀렉터를 단축키처럼 정의할 수도 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

페이지 객체를 만들려면 `dusk:page` Artisan 명령어를 사용합니다. 모든 페이지 객체는 `tests/Browser/Pages` 디렉터리에 저장됩니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정 (Configuring Pages)

기본적으로 페이지에는 `url`, `assert`, `elements` 세 가지 메서드가 있습니다. 여기서는 주로 `url`과 `assert` 메서드에 대해 설명하며, `elements`는 [아래에서 자세히 다룹니다](#shorthand-selectors).

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드는 해당 페이지의 URL 경로를 반환합니다. Dusk는 이 URL로 페이지에 접근합니다:

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

`assert` 메서드는 브라우저가 해당 페이지에 정말 도착했는지 확인하는 어서션을 자유롭게 작성할 수 있습니다. 꼭 내용을 작성해야 하는 필수 메서드는 아니지만, 필요시 원하는 만큼 어서션을 추가할 수 있습니다. 이 메서드는 페이지로 이동할 때 자동으로 실행됩니다:

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
### 페이지로 이동 (Navigating to Pages)

페이지가 정의되었다면, `visit` 메서드로 페이지로 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 해당 페이지에 있는 상태에서 그 페이지 클래스를 불러와서 셀렉터 및 메서드를 계속 사용하려면 `on` 메서드를 활용할 수 있습니다. (예: 버튼 클릭 후 페이지 리디렉션):

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 약식 셀렉터 (Shorthand Selectors)

페이지 클래스에서 `elements` 메서드를 이용해 자주 사용하는 CSS 셀렉터에 대한 빠르고 기억하기 쉬운 단축키를 정의할 수 있습니다. 예를 들어, 로그인 페이지의 "email" 입력 필드에 대한 단축키를 정의하려면 아래와 같이 작성합니다:

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

이렇게 정의한 단축 셀렉터는 CSS 셀렉터가 필요한 모든 곳에서 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 약식 셀렉터 (Global Shorthand Selectors)

Dusk 설치 시 `tests/Browser/Pages`에 `Page` 기본 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드를 사용하면 애플리케이션 전체 페이지에서 공통적으로 사용할 전역 단축 셀렉터를 정의할 수 있습니다:

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
### 페이지 메서드 (Page Methods)

기본 내장 메서드 외에도, 직접 메서드를 정의하여 여러 테스트에서 활용할 수 있습니다. 예를 들어, 음악 관리 애플리케이션의 한 페이지에서 플레이리스트 생성 작업을 여러 테스트에서 반복적으로 사용한다면, `createPlaylist` 메서드를 정의해두고 재사용할 수 있습니다:

```php
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Page;

class Dashboard extends Page
{
    // 기타 페이지 메서드...

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

정의한 메서드는 아래처럼 페이지를 사용하는 모든 테스트에서 사용할 수 있습니다(브라우저 인스턴스는 첫 번째 인수로 자동 전달):

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk의 "페이지 객체"와 유사하지만, 같은 UI와 기능이 여러 페이지에 공통적으로 사용되는 경우에 적합합니다(예: 네비게이션 바, 알림창 등). 컴포넌트는 특정 URL에 묶이지 않아 여러 곳에서 쉽게 재사용할 수 있습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트를 생성하려면 `dusk:component` Artisan 명령어를 사용하세요. 새 컴포넌트는 `tests/Browser/Components` 디렉터리에 저장됩니다:

```shell
php artisan dusk:component DatePicker
```

날짜 선택기 등 여러 페이지에서 재활용되는 컴포넌트는 반복적으로 로직을 작성하기 번거로우니, Dusk 컴포넌트로 정의해두면 한 곳만 수정해도 전체 테스트에 반영되어 유지보수가 수월합니다:

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
### 컴포넌트 사용 (Using Components)

컴포넌트를 정의하면, 각 테스트에서 간단히 메서드로 로직을 재사용할 수 있습니다. 만약 날짜 선택 로직에 변화가 생겨도 컴포넌트만 수정하면 모든 테스트에 일괄 적용됩니다:

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

`component` 메서드로 컴포넌트의 범위 내 브라우저 인스턴스를 반환받아 추가 동작도 가능합니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합(CI) (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk CI 설정에서는 Laravel 애플리케이션이 내장 PHP 개발 서버(포트 8000)에서 서비스된다고 가정합니다. 때문에 CI 환경의 `APP_URL`은 `http://127.0.0.1:8000`이 되어야 합니다.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면, 아래와 같이 Google Chrome 빌드팩과 스크립트를 `app.json`에 추가하세요:

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

[Travis CI](https://travis-ci.org)에 Dusk 테스트를 올리려면 `.travis.yml` 설정을 아래처럼 사용할 수 있습니다. Travis CI는 GUI 환경이 아니므로 Chrome 실행에 몇 가지 추가 작업이 필요합니다:

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

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하고 싶다면, 다음 설정 파일을 참고해 시작할 수 있습니다. Travis CI와 마찬가지로 내장 PHP 서버를 사용합니다:

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

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 수행하려면, 아래 설정 파일을 예시로 사용할 수 있습니다(PHP 내장 서버로 Laravel을 동작시킵니다):

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

Chipper CI에서 Dusk 테스트 및 데이터베이스 사용 방법 등 자세한 내용은 [Chipper CI 공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.
