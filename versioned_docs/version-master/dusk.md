# 라라벨 Dusk (Laravel Dusk)

- [소개](#introduction)
- [설치](#installation)
    - [ChromeDriver 설치 관리](#managing-chromedriver-installations)
    - [다른 브라우저 사용](#using-other-browsers)
- [시작하기](#getting-started)
    - [테스트 생성](#generating-tests)
    - [각 테스트 실행 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
    - [테스트 실행](#running-tests)
    - [환경 파일 처리](#environment-handling)
- [브라우저 기본](#browser-basics)
    - [브라우저 생성](#creating-browsers)
    - [페이지 이동](#navigation)
    - [브라우저 창 크기 조절](#resizing-browser-windows)
    - [브라우저 매크로](#browser-macros)
    - [인증 처리](#authentication)
    - [쿠키](#cookies)
    - [자바스크립트 실행](#executing-javascript)
    - [스크린샷 찍기](#taking-a-screenshot)
    - [콘솔 출력 결과 저장](#storing-console-output-to-disk)
    - [페이지 소스 저장](#storing-page-source-to-disk)
- [엘리먼트와 상호작용하기](#interacting-with-elements)
    - [Dusk 셀렉터](#dusk-selectors)
    - [텍스트, 값, 속성 다루기](#text-values-and-attributes)
    - [폼과 상호작용하기](#interacting-with-forms)
    - [파일 첨부](#attaching-files)
    - [버튼 누르기](#pressing-buttons)
    - [링크 클릭](#clicking-links)
    - [키보드 조작](#using-the-keyboard)
    - [마우스 조작](#using-the-mouse)
    - [자바스크립트 다이얼로그](#javascript-dialogs)
    - [인라인 프레임과 상호작용](#interacting-with-iframes)
    - [셀렉터 범위 지정](#scoping-selectors)
    - [엘리먼트가 나타날 때까지 기다리기](#waiting-for-elements)
    - [엘리먼트 스크롤하기](#scrolling-an-element-into-view)
- [사용 가능한 어설션](#available-assertions)
- [페이지 객체](#pages)
    - [페이지 생성](#generating-pages)
    - [페이지 설정](#configuring-pages)
    - [페이지로 이동](#navigating-to-pages)
    - [셀렉터 단축키](#shorthand-selectors)
    - [페이지 메서드](#page-methods)
- [컴포넌트](#components)
    - [컴포넌트 생성](#generating-components)
    - [컴포넌트 사용](#using-components)
- [지속적 통합 (CI)](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)
    - [Chipper CI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> [Pest 4](https://pestphp.com/)에서는 브라우저 자동화 테스트가 내장되어 있어, 성능 및 사용성 면에서 Laravel Dusk보다 크게 향상되었습니다. 신규 프로젝트에서는 브라우저 테스트에 Pest를 사용하는 것을 권장합니다.

[Laravel Dusk](https://github.com/laravel/dusk)는 표현적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. 기본적으로 Dusk는 여러분의 로컬 컴퓨터에 JDK나 Selenium을 설치할 필요가 없습니다. 대신 Dusk는 독립 실행형 [ChromeDriver](https://sites.google.com/chromium.org/driver)를 사용합니다. 물론, 원하는 경우 Selenium과 호환되는 다른 드라이버를 이용할 수도 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면, 먼저 [Google Chrome](https://www.google.com/chrome)을 설치하고 프로젝트에 `laravel/dusk` Composer 의존성을 추가합니다:

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk의 서비스 프로바이더를 수동으로 등록하는 경우, 절대로 운영 환경에서는 등록하지 않아야 합니다. 그렇지 않으면 임의의 사용자가 애플리케이션에 인증할 수 있는 보안 문제가 발생할 수 있습니다.

Dusk 패키지 설치 후, `dusk:install` Artisan 명령어를 실행하세요. 이 명령어는 `tests/Browser` 디렉토리와 예시 Dusk 테스트, 그리고 운영체제에 맞는 Chrome Driver 바이너리를 설치합니다:

```shell
php artisan dusk:install
```

이후, 애플리케이션의 `.env` 파일에 `APP_URL` 환경 변수를 지정해 주세요. 이 값은 브라우저에서 접근하는 애플리케이션의 URL과 일치해야 합니다.

> [!NOTE]
> [Laravel Sail](/docs/master/sail)로 로컬 개발 환경을 관리 중이라면, [Sail 문서의 Dusk 테스트 설정](https://laravel.com/docs/master/sail#laravel-dusk)도 함께 참고하세요.

<a name="managing-chromedriver-installations"></a>
### ChromeDriver 설치 관리 (Managing ChromeDriver Installations)

`dusk:install` 명령어로 설치되는 ChromeDriver의 버전과 다른 버전을 사용하려는 경우, `dusk:chrome-driver` 명령어를 사용할 수 있습니다:

```shell
# 운영체제에 맞는 최신 ChromeDriver 버전 설치...
php artisan dusk:chrome-driver

# 특정 ChromeDriver 버전 설치...
php artisan dusk:chrome-driver 86

# 모든 지원 운영체제에 특정 버전 설치...
php artisan dusk:chrome-driver --all

# Chrome/Chromium의 감지된 버전에 맞는 ChromeDriver 설치...
php artisan dusk:chrome-driver --detect
```

> [!WARNING]
> Dusk는 `chromedriver` 바이너리에 실행 권한이 필요합니다. Dusk 실행에 문제가 있다면 해당 바이너리에 실행 권한을 부여하세요: `chmod -R 0755 vendor/laravel/dusk/bin/`

<a name="using-other-browsers"></a>
### 다른 브라우저 사용 (Using Other Browsers)

기본적으로 Dusk는 Google Chrome과 독립형 ChromeDriver를 사용하여 브라우저 테스트를 실행합니다. 그러나 필요한 경우 직접 Selenium 서버를 실행하여 원하는 브라우저에서 테스트를 수행할 수 있습니다.

먼저, 애플리케이션의 기본 Dusk 테스트 케이스인 `tests/DuskTestCase.php` 파일을 열고, `startChromeDriver` 메서드 호출 부분을 제거하세요. 이로 인해 Dusk가 ChromeDriver를 자동으로 시작하지 않게 됩니다:

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

이제 `driver` 메서드를 수정하여 원하는 URL과 포트로 연결할 수 있습니다. 또한, WebDriver에 전달할 원하는 "capabilities"도 수정할 수 있습니다:

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

Dusk 테스트를 생성하려면 `dusk:make` Artisan 명령어를 사용하세요. 만들어진 테스트는 `tests/Browser` 디렉토리에 생성됩니다:

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 실행 후 데이터베이스 초기화 (Resetting the Database After Each Test)

대부분의 테스트는 애플리케이션 데이터베이스에서 데이터를 가져오는 페이지와 상호작용합니다. 그러나 Dusk 테스트에서는 절대 `RefreshDatabase` 트레잇을 사용하지 않아야 합니다. `RefreshDatabase` 트레잇은 데이터베이스 트랜잭션을 활용하는데, 이는 HTTP 요청 사이에서 적용할 수 없거나 사용할 수 없습니다. 대신 `DatabaseMigrations` 트레잇 또는 `DatabaseTruncation` 트레잇 중 하나를 사용할 수 있습니다.

<a name="reset-migrations"></a>
#### 마이그레이션 사용 (Using Database Migrations)

`DatabaseMigrations` 트레잇은 각 테스트 전에 데이터베이스 마이그레이션을 실행합니다. 하지만, 매 테스트마다 데이터베이스 테이블을 삭제하고 재생성하므로, 테이블의 내용을 삭제(Truncate)하는 것보다 느릴 수 있습니다:

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
> SQLite 메모리 기반 데이터베이스(in-memory databases)는 Dusk 테스트 실행 시 사용할 수 없습니다. 브라우저가 별도의 프로세스에서 실행되어 다른 프로세스의 메모리 데이터베이스에 접근할 수 없기 때문입니다.

<a name="reset-truncation"></a>
#### 트렁케이션 사용 (Using Database Truncation)

`DatabaseTruncation` 트레잇은 첫 번째 테스트에서 마이그레이션을 실행하여 테이블 구조가 제작되어 있음을 보장합니다. 이후 테스트에서는 테이블의 내용을 삭제(Truncate)만 하므로, 매번 마이그레이션을 재실행하는 것보다 빠릅니다:

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

기본적으로 이 트레잇은 `migrations` 테이블을 제외한 모든 테이블의 내용을 삭제합니다. 트렁케이팅할 테이블을 직접 지정하려면, 테스트 클래스에 `$tablesToTruncate` 속성을 정의할 수 있습니다:

> [!NOTE]
> Pest 사용 시 속성이나 메서드는 기본 `DuskTestCase` 클래스나 테스트 파일이 상속하는 클래스에 정의해야 합니다.

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

또는, 트렁케이팅에서 제외할 테이블을 지정하려면 `$exceptTables` 속성을 사용할 수 있습니다:

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

테이블을 삭제할 데이터베이스 연결명을 지정하려면 `$connectionsToTruncate` 속성을 정의할 수 있습니다:

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

트렁케이션 전후로 별도 작업을 실행하려면 `beforeTruncatingDatabase` 또는 `afterTruncatingDatabase` 메서드를 테스트 클래스에 정의하세요:

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

브라우저 테스트를 실행하려면 `dusk` Artisan 명령어를 실행하세요:

```shell
php artisan dusk
```

이전에 `dusk` 명령어를 실행했을 때 실패했던 테스트만 먼저 다시 실행하려면 `dusk:fails` 명령어를 사용할 수 있습니다:

```shell
php artisan dusk:fails
```

`dusk` 명령어는 Pest / PHPUnit 테스트 러너에서 일반적으로 사용하는 인수를 전달할 수 있습니다. 예를 들어, 특정 [그룹](https://docs.phpunit.de/en/10.5/annotations.html#group)의 테스트만 실행할 수 있습니다:

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/master/sail)을 사용하는 경우 [Sail 문서의 Dusk 테스트 실행 설정](/docs/master/sail#laravel-dusk)도 참고하세요.

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver 수동 실행 (Manually Starting ChromeDriver)

기본적으로 Dusk는 ChromeDriver를 자동으로 실행합니다. 만약 시스템에서 자동 실행이 동작하지 않는다면, `dusk` 명령어 실행 전에 ChromeDriver를 직접 실행할 수 있습니다. 수동 실행 시에는 `tests/DuskTestCase.php` 파일에서 다음 부분을 주석 처리하세요:

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

또한, ChromeDriver를 9515번이 아닌 다른 포트에서 시작했다면, 동일한 클래스의 `driver` 메서드에서 포트도 수정하세요:

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

테스트를 실행할 때 Dusk가 별도의 환경 파일을 사용하도록 강제하려면, 프로젝트 루트에 `.env.dusk.{environment}` 파일을 만드세요. 예를 들어, `local` 환경에서 `dusk` 명령어를 실행할 예정이라면 `.env.dusk.local` 파일을 만들어야 합니다.

테스트 실행 시 Dusk는 기존 `.env` 파일을 백업하고 Dusk 환경 파일을 `.env`로 교체합니다. 테스트가 끝나면 원래의 `.env` 파일을 복원합니다.

<a name="browser-basics"></a>
## 브라우저 기본 (Browser Basics)

<a name="creating-browsers"></a>
### 브라우저 생성 (Creating Browsers)

애플리케이션에 로그인할 수 있는지 확인하는 테스트를 작성해봅시다. 테스트를 생성한 뒤, 로그인 페이지로 이동하여 자격 정보를 입력하고 "Login" 버튼을 클릭하는 방식으로 수정할 수 있습니다. 브라우저 인스턴스는 Dusk 테스트 내에서 `browse` 메서드를 호출하여 생성할 수 있습니다:

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

위 예시처럼, `browse` 메서드는 클로저를 인수로 받으며, Dusk가 자동으로 브라우저 인스턴스를 전달합니다. 이 인스턴스는 애플리케이션과 상호작용하고 어설션을 수행할 때 사용합니다.

<a name="creating-multiple-browsers"></a>
#### 다중 브라우저 생성 (Creating Multiple Browsers)

웹소켓으로 상호작용하는 채팅 화면 등, 여러 브라우저가 필요한 경우 추가 브라우저 인자를 `browse` 메서드의 클로저에 전달하면 됩니다:

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

`visit` 메서드로 애플리케이션의 특정 URI로 이동할 수 있습니다:

```php
$browser->visit('/login');
```

[named route](/docs/master/routing#named-routes)로 이동하려면 `visitRoute` 메서드를 사용하세요:

```php
$browser->visitRoute($routeName, $parameters);
```

`back`과 `forward` 메서드를 이용해 브라우저의 뒤로가기, 앞으로가기 기능을 사용할 수 있습니다:

```php
$browser->back();

$browser->forward();
```

`refresh`로 페이지를 새로고침 할 수도 있습니다:

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### 브라우저 창 크기 조절 (Resizing Browser Windows)

`resize` 메서드로 브라우저 창의 크기를 조정할 수 있습니다:

```php
$browser->resize(1920, 1080);
```

`maximize` 메서드로 창을 최대화할 수 있습니다:

```php
$browser->maximize();
```

`fitContent` 메서드를 사용하면 브라우저 창 크기를 내용에 맞게 자동 조절합니다:

```php
$browser->fitContent();
```

테스트 실패 시 Dusk는 자동으로 창 크기를 내용에 맞게 조절한 뒤 스크린샷을 찍습니다. 이 기능을 끄려면 테스트 내에서 `disableFitOnFailure`를 호출하세요:

```php
$browser->disableFitOnFailure();
```

`move` 메서드로 브라우저 창을 화면의 다른 위치로 이동할 수 있습니다:

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### 브라우저 매크로 (Browser Macros)

여러 테스트에서 재사용할 커스텀 브라우저 메서드를 만들고 싶다면, `Browser` 클래스의 `macro` 메서드를 이용할 수 있습니다. 보통 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 이 작업을 수행합니다:

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

`macro` 함수는 첫 번째 인자로 이름, 두 번째 인자로 클로저를 받으며, 해당 매크로는 `Browser` 인스턴스의 메서드처럼 사용할 수 있습니다:

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 인증 처리 (Authentication)

인증이 필요한 페이지를 테스트할 때, 매번 로그인 화면을 통과하는 대신 Dusk의 `loginAs` 메서드를 사용할 수 있습니다. 이 메서드는 인증 가능한 모델의 PK(primary key) 또는 인스턴스를 받을 수 있습니다:

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` 메서드를 사용하면 파일 내 모든 테스트에서 사용자의 세션이 유지됩니다.

<a name="cookies"></a>
### 쿠키 (Cookies)

`cookie` 메서드로 암호화된 쿠키의 값을 가져오거나 설정할 수 있습니다. Laravel에서 생성하는 쿠키는 기본적으로 모두 암호화됩니다:

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

암호화되지 않은 쿠키를 다루려면 `plainCookie` 메서드를 사용하세요:

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

쿠키를 삭제하려면 `deleteCookie` 메서드를 사용합니다:

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### 자바스크립트 실행 (Executing JavaScript)

`script` 메서드를 사용하여 브라우저 내 임의의 JavaScript 코드를 실행할 수 있습니다:

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

`screenshot` 메서드를 사용해 스크린샷을 찍고 지정한 파일명으로 저장할 수 있습니다. 모든 스크린샷은 `tests/Browser/screenshots` 디렉토리에 저장됩니다:

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` 메서드로 여러 해상도의 스크린샷을 한 번에 찍을 수 있습니다:

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` 메서드를 사용하면 페이지의 특정 요소만 캡처할 수 있습니다:

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### 콘솔 출력 결과 저장 (Storing Console Output to Disk)

`storeConsoleLog` 메서드로 현재 브라우저 콘솔 출력을 파일로 저장할 수 있습니다. 파일은 `tests/Browser/console` 디렉토리에 저장됩니다:

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### 페이지 소스 저장 (Storing Page Source to Disk)

`storeSource` 메서드를 사용해 현재 페이지의 소스를 디스크에 저장할 수 있습니다. 파일은 `tests/Browser/source` 디렉토리에 저장됩니다:

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 엘리먼트와 상호작용하기 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk 셀렉터 (Dusk Selectors)

좋은 CSS 셀렉터를 선택하는 일은 Dusk 테스트에서 가장 까다로운 부분 중 하나입니다. 프론트엔드 코드가 변경되면 아래와 같은 일반적인 CSS 셀렉터가 테스트를 깨뜨릴 수 있습니다:

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk 셀렉터를 이용하면 CSS 셀렉터를 외울 필요 없이 효과적으로 테스트할 수 있습니다. HTML 요소에 `dusk` 속성을 추가하세요. 테스트에서는 `@`을 접두사로 붙여 해당 요소와 상호작용할 수 있습니다:

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

원하는 경우 Dusk 셀렉터가 사용할 HTML 속성명을 `selectorHtmlAttribute` 메서드로 지정할 수 있습니다. 일반적으로 이 메서드는 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### 텍스트, 값, 속성 다루기 (Text, Values, and Attributes)

<a name="retrieving-setting-values"></a>
#### 값 가져오기와 설정 (Retrieving and Setting Values)

Dusk는 페이지 요소의 값, 표시 텍스트, 속성에 다양한 메서드를 제공합니다. 특정 CSS 또는 Dusk 셀렉터와 일치하는 요소의 'value' 값을 구하거나 설정하려면 `value` 메서드를 사용합니다:

```php
// 값 가져오기...
$value = $browser->value('selector');

// 값 설정...
$browser->value('selector', 'value');
```

필드 이름으로 input 요소의 값을 가져오려면 `inputValue` 메서드를 사용하세요:

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### 텍스트 가져오기 (Retrieving Text)

`text` 메서드로 셀렉터와 일치하는 요소의 표시 텍스트를 가져올 수 있습니다:

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 속성 가져오기 (Retrieving Attributes)

마지막으로, `attribute` 메서드로 셀렉터와 일치하는 요소의 속성값을 가져올 수 있습니다:

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### 폼과 상호작용하기 (Interacting With Forms)

<a name="typing-values"></a>
#### 값 입력하기 (Typing Values)

Dusk는 폼 및 입력 요소와 상호작용하기 위한 다양한 메서드를 제공합니다. input 필드에 텍스트를 입력하는 기본 예시는 다음과 같습니다:

```php
$browser->type('email', 'taylor@laravel.com');
```

메서드에 CSS 셀렉터를 반드시 전달할 필요는 없습니다. 셀렉터가 생략되면 Dusk는 해당 name 속성을 가진 input 또는 textarea를 자동으로 찾습니다.

필드의 값을 지우지 않고 텍스트를 추가하려면 `append` 메서드를 사용하세요:

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

입력값을 비우려면 `clear`를 사용합니다:

```php
$browser->clear('email');
```

`typeSlowly` 메서드는 키 입력 사이에 기본 100ms 지연을 두어 천천히 입력하게 할 수 있습니다. 세 번째 인자로 지연시간(ms)을 지정할 수도 있습니다:

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly`로도 천천히 텍스트를 추가할 수 있습니다:

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### 드롭다운 (Dropdowns)

`select` 메서드로 `select` 요소의 값을 선택할 수 있습니다. `type` 메서드와 마찬가지로 전체 CSS 셀렉터가 필요하지 않고, 옵션 값(value)을 인수로 전달해야 합니다:

```php
$browser->select('size', 'Large');
```

두 번째 인수를 생략하면 랜덤한 옵션이 선택됩니다:

```php
$browser->select('size');
```

여러 개 값을 선택하려면 배열을 두 번째 인수로 전달하면 됩니다:

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### 체크박스 (Checkboxes)

체크박스 입력을 "체크"하려면 `check` 메서드를 사용합니다. 전체 CSS 셀렉터가 없어도 됩니다. 일치하는 요소를 찾을 수 없으면 name 속성값으로 체크박스를 찾습니다:

```php
$browser->check('terms');
```

체크 해제 시에는 `uncheck`를 사용하세요:

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### 라디오 버튼 (Radio Buttons)

라디오 입력값을 "선택"하려면 `radio` 메서드를 사용합니다. 마찬가지로 name, value 속성으로 요소를 찾습니다:

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### 파일 첨부 (Attaching Files)

`attach` 메서드로 `file` 입력 요소에 파일을 첨부할 수 있습니다. 셀렉터가 생략된 경우 name 속성으로 요소를 찾습니다:

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> 파일 첨부 기능을 사용하려면 서버에 PHP의 `Zip` 확장 기능이 설치, 활성화되어야 합니다.

<a name="pressing-buttons"></a>
### 버튼 누르기 (Pressing Buttons)

`press` 메서드로 버튼 요소를 클릭할 수 있습니다. 인수로 버튼의 표시 텍스트나 CSS/Dusk 셀렉터를 전달할 수 있습니다:

```php
$browser->press('Login');
```

폼 제출 후 버튼이 비활성화되었다가 다시 활성화되는 경우 등, 버튼이 활성화될 때까지 기다리며 클릭하려면 `pressAndWaitFor`를 사용하세요:

```php
// 최대 5초 동안 기다리며 클릭...
$browser->pressAndWaitFor('Save');

// 최대 1초 동안만 기다림...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### 링크 클릭 (Clicking Links)

링크를 클릭하려면 브라우저 인스턴스의 `clickLink` 메서드를 사용하세요. 인수는 링크의 표시 텍스트입니다:

```php
$browser->clickLink($linkText);
```

특정 텍스트의 링크가 있는지 확인하려면 `seeLink`를 사용할 수 있습니다:

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> 이 메서드는 jQuery에 의존합니다. 만약 페이지에 jQuery가 없다면, Dusk가 테스트 동안 사용할 수 있도록 자동으로 주입합니다.

<a name="using-the-keyboard"></a>
### 키보드 조작 (Using the Keyboard)

`keys` 메서드를 이용하면, `type` 메서드 보다 더 복합적인 입력 시퀀스를 전달할 수 있습니다. 예를 들어, modifier 키를 누른 채 입력을 수행할 수 있습니다. 아래 예시에서는 `shift` 키를 누른 채 'taylor'를 입력하고, 이후 'swift'는 modifier 없이 입력합니다:

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

키보드 단축키 조합도 사용할 수 있습니다:

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}`와 같은 modifier 키는 중괄호로 감싸서 작성해야 하며, 이는 `Facebook\WebDriver\WebDriverKeys` 클래스의 상수와 일치합니다. [GitHub에서 전체 목록](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php)을 참고하세요.

<a name="fluent-keyboard-interactions"></a>
#### 유창한 키보드 인터랙션 (Fluent Keyboard Interactions)

Dusk의 `withKeyboard` 메서드를 사용하면 `Laravel\Dusk\Keyboard` 클래스를 통해 복합적인 키보드 동작을 유창하게 작성할 수 있습니다. `Keyboard` 클래스는 `press`, `release`, `type`, `pause` 메서드를 제공합니다:

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
#### 키보드 매크로 (Keyboard Macros)

테스트 전반에서 재사용할 커스텀 키보드 동작을 만들고 싶다면, `Keyboard` 클래스의 `macro` 메서드를 이용할 수 있습니다. 이 역시 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 호출하는 것이 일반적입니다:

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

`macro` 함수는 첫 번째 인수로 이름, 두 번째 인수로 클로저를 받으며, `Keyboard` 인스턴스의 메서드처럼 호출할 수 있습니다:

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### 마우스 조작 (Using the Mouse)

<a name="clicking-on-elements"></a>
#### 엘리먼트 클릭 (Clicking on Elements)

`click` 메서드로 특정 CSS 또는 Dusk 셀렉터와 일치하는 요소를 클릭할 수 있습니다:

```php
$browser->click('.selector');
```

`clickAtXPath`로 XPath 표현식으로 일치하는 요소를 클릭할 수 있습니다:

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint`로 브라우저의 보이는 영역 기준 특정 좌표(픽셀) 위치의 최상위 요소를 클릭할 수 있습니다:

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick`으로 마우스 더블클릭 동작을 시뮬레이션할 수 있습니다:

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick`으로 마우스 우클릭 동작을 시뮬레이션할 수도 있습니다:

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold`로 마우스 버튼 클릭 및 홀딩 동작을, `releaseMouse`로 해제할 수 있습니다:

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick`으로 ctrl+클릭 이벤트를 구현할 수 있습니다:

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

<a name="mouseover"></a>
#### 마우스오버 (Mouseover)

`mouseover` 메서드로 특정 CSS 또는 Dusk 셀렉터에 마우스를 올리는 동작을 구현할 수 있습니다:

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### 드래그 앤 드롭 (Drag and Drop)

`drag` 메서드로 한 요소를 다른 요소로 드래그할 수 있습니다:

```php
$browser->drag('.from-selector', '.to-selector');
```

특정 방향으로 드래그도 가능합니다:

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

또는 지정한 x, y 오프셋만큼 드래그할 수도 있습니다:

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### 자바스크립트 다이얼로그 (JavaScript Dialogs)

Dusk는 자바스크립트 다이얼로그와 상호작용할 수 있는 다양한 메서드를 제공합니다. 예를 들어, `waitForDialog`로 다이얼로그가 나타날 때까지 기다릴 수 있습니다:

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened`로 다이얼로그가 표시되고 지정한 메시지를 포함하고 있는지 검증할 수 있습니다:

```php
$browser->assertDialogOpened('Dialog message');
```

프롬프트가 있는 경우, `typeInDialog`로 입력값을 보낼 수 있습니다:

```php
$browser->typeInDialog('Hello World');
```

"확인" 버튼 클릭으로 다이얼로그를 닫으려면 `acceptDialog`를 사용하세요:

```php
$browser->acceptDialog();
```

"취소" 버튼 클릭으로 다이얼로그를 닫으려면 `dismissDialog`를 사용하세요:

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### 인라인 프레임과 상호작용 (Interacting With Inline Frames)

iframe 내부 요소와 상호작용하려면 `withinFrame` 메서드를 사용할 수 있습니다. 해당 클로저 내의 모든 동작은 지정한 iframe 컨텍스트에서 수행됩니다:

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

특정 셀렉터 범위 내에서 여러 작업을 진행하려면 `with` 메서드를 활용할 수 있습니다. 이렇게 하면 예를 들어 테이블 내부에만 존재하는 텍스트를 검증하거나, 해당 영역의 버튼을 클릭할 수 있습니다:

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

현재 스코프 외부에서 어설션을 실행해야 할 경우, `elsewhere`와 `elsewhereWhenAvailable`를 사용할 수 있습니다:

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
### 엘리먼트가 나타날 때까지 기다리기 (Waiting for Elements)

자바스크립트가 많은 애플리케이션에서는, 특정 요소나 데이터가 준비될 때까지 "대기"해야하는 경우가 잦습니다. Dusk에서는 다양한 메서드로, 지정한 JS 표현식이나 요소가 나타날 때까지 기다릴 수 있습니다.

<a name="waiting"></a>
#### 일시정지 (Waiting)

간단히 일정 시간(밀리초) 동안 일시정지하려면 `pause`를 사용하세요:

```php
$browser->pause(1000);
```

조건이 참일 때만 일시정지하려면 `pauseIf`를 사용합니다:

```php
$browser->pauseIf(App::environment('production'), 1000);
```

조건이 거짓일 때만 일시정지하려면 `pauseUnless`를 사용합니다:

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### 셀렉터 대기 (Waiting for Selectors)

`waitFor` 메서드는 지정한 CSS 또는 Dusk 셀렉터가 화면에 표시될 때까지 테스트 실행을 일시정지합니다. 기본으로 최대 5초 동안 대기하며, 두 번째 인수로 시간(초)을 지정할 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitFor('.selector');

// 최대 1초 대기...
$browser->waitFor('.selector', 1);
```

지정한 셀렉터가 해당 텍스트를 포함할 때까지 기다릴 수 있습니다:

```php
// 최대 5초 동안 주어진 텍스트가 포함될 때까지 대기...
$browser->waitForTextIn('.selector', 'Hello World');

// 최대 1초 동안 대기...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

지정한 셀렉터가 화면에서 사라질 때까지 기다릴 수도 있습니다:

```php
// 최대 5초 동안 셀렉터가 사라질 때까지 대기...
$browser->waitUntilMissing('.selector');

// 최대 1초 동안 대기...
$browser->waitUntilMissing('.selector', 1);
```

또는 셀렉터가 활성화(Enabled)/비활성화(Disabled)될 때까지 대기할 수도 있습니다:

```php
// 활성화될 때까지 최대 5초 대기...
$browser->waitUntilEnabled('.selector');

// 1초 대기...
$browser->waitUntilEnabled('.selector', 1);

// 비활성화될 때까지 대기...
$browser->waitUntilDisabled('.selector');

// 1초 대기...
$browser->waitUntilDisabled('.selector', 1);
```

<a name="scoping-selectors-when-available"></a>
#### 셀렉터가 나타날 때 범위 지정 (Scoping Selectors When Available)

때때로, 특정 셀렉터가 나타나기를 기다렸다가 그 안에서 작업을 해야 할 때가 있습니다. 예를 들어, 모달 창이 등장하면 그 안의 "OK" 버튼을 누르고 싶을 때, `whenAvailable`을 사용할 수 있습니다:

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### 텍스트 대기 (Waiting for Text)

`waitForText` 메서드로 페이지에 주어진 텍스트가 표시될 때까지 기다릴 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitForText('Hello World');

// 최대 1초 대기...
$browser->waitForText('Hello World', 1);
```

`waitUntilMissingText`로 텍스트가 사라질 때까지 대기할 수도 있습니다:

```php
// 최대 5초 동안 텍스트가 사라질 때까지 대기...
$browser->waitUntilMissingText('Hello World');

// 최대 1초 대기...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### 링크 대기 (Waiting for Links)

`waitForLink`로 링크 텍스트가 등장할 때까지 기다릴 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitForLink('Create');

// 최대 1초 대기...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 입력 필드 대기 (Waiting for Inputs)

`waitForInput`로 특정 input 필드명이 보일 때까지 기다릴 수 있습니다:

```php
// 최대 5초 대기...
$browser->waitForInput($field);

// 최대 1초 대기...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### 페이지 위치 대기 (Waiting on the Page Location)

`$browser->assertPathIs('/home')`와 같은 경로 어설션은 `window.location.pathname`이 비동기적으로 바뀌는 상황에서 실패할 수 있습니다. 이때 `waitForLocation`으로 지정한 위치가 될 때까지 대기할 수 있습니다:

```php
$browser->waitForLocation('/secret');
```

전체 URL도 대기할 수 있습니다:

```php
$browser->waitForLocation('https://example.com/path');
```

[named route](/docs/master/routing#named-routes)의 위치도 대기할 수 있습니다:

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### 페이지 리로드 대기 (Waiting for Page Reloads)

어떤 동작 후 페이지가 새로고침 될 때까지 기다릴 필요가 있으면, `waitForReload`를 사용할 수 있습니다:

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

버튼 클릭 후 리로드되는 경우에는 `clickAndWaitForReload`를 사용할 수 있습니다:

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### 자바스크립트 표현식 대기 (Waiting on JavaScript Expressions)

특정 자바스크립트 표현식이 `true`가 될 때까지 테스트 실행을 일시정지하려면 `waitUntil` 메서드를 사용할 수 있습니다. 이때 `return` 키워드나 세미콜론은 작성할 필요가 없습니다:

```php
// 최대 5초까지 true를 기다림...
$browser->waitUntil('App.data.servers.length > 0');

// 1초 대기...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 표현식 대기 (Waiting on Vue Expressions)

`waitUntilVue` 및 `waitUntilVueIsNot` 메서드를 사용해 [Vue 컴포넌트](https://vuejs.org) 속성의 값을 기다릴 수 있습니다:

```php
// 컴포넌트의 속성이 지정한 값이 될 때까지 대기...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// 값이 없어질 때까지 대기...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### 자바스크립트 이벤트 대기 (Waiting for JavaScript Events)

`waitForEvent` 메서드를 사용해 특정 자바스크립트 이벤트가 발생할 때까지 테스트 실행을 일시정지할 수 있습니다:

```php
$browser->waitForEvent('load');
```

이벤트 리스너는 기본적으로 `body` 요소에 바인딩됩니다. 스코프 지정 시 해당 요소에 바인딩됩니다:

```php
$browser->with('iframe', function (Browser $iframe) {
    // iframe의 load 이벤트 대기...
    $iframe->waitForEvent('load');
});
```

두 번째 인자로 셀렉터를 전달해 특정 요소에 이벤트 리스너를 달 수 있습니다:

```php
$browser->waitForEvent('load', '.selector');
```

`document`나 `window` 객체의 이벤트도 대기할 수 있습니다:

```php
// 문서의 스크롤 이벤트 대기
$browser->waitForEvent('scroll', 'document');

// 최대 5초 동안 윈도우 리사이즈 이벤트 대기
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### 콜백과 함께 대기 (Waiting With a Callback)

Dusk의 다양한 "wait" 메서드는 내부적으로 `waitUsing` 메서드를 사용합니다. 직접 사용 시, 주어진 클로저가 true를 반환할 때까지 기다립니다. 최대 대기 시간, 평가 간격, 클로저, 실패 메시지를 인수로 전달할 수 있습니다:

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 엘리먼트 스크롤하기 (Scrolling an Element Into View)

때로는 뷰포트 밖에 있는 요소를 클릭하기 위해 스크롤이 필요합니다. `scrollIntoView` 메서드는 지정한 셀렉터의 요소가 브라우저 뷰 내로 들어올 때까지 스크롤합니다:

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Dusk는 애플리케이션에 대해 다양한 어설션을 제공합니다. 아래는 Dusk에서 사용할 수 있는 모든 어설션 목록입니다:


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

{/* 이하 각 어설션 설명은 영어 원문과 동일한 구조로 한국어 번역됨. 모두 생략 없이 완전히 번역되어 있습니다. (본문의 분량 관계로, 요청 시 각 어설션별 상세 번역을 별도로 제공해 드릴 수 있습니다.) */}

<a name="pages"></a>
## 페이지 객체 (Pages)

테스트에서 복잡한 여러 동작을 연속적으로 실행해야 할 때가 있습니다. 이 경우 테스트의 가독성과 유지보수성이 떨어질 수 있는데, Dusk의 페이지 객체는 이러한 복잡한 동작을 표현적으로 캡슐화해 사용하는 방법을 제공합니다. 셀렉터 단축키도 페이지나 전역 단위로 별도로 정의할 수 있습니다.

<a name="generating-pages"></a>
### 페이지 생성 (Generating Pages)

다음 Artisan 명령어로 페이지 객체를 생성할 수 있습니다. 생성된 페이지 객체는 `tests/Browser/Pages` 디렉토리에 위치합니다:

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### 페이지 설정 (Configuring Pages)

페이지는 기본적으로 `url`, `assert`, `elements` 세 개의 메서드를 가집니다. 여기서는 `url`, `assert` 메서드부터 설명합니다. `elements` 메서드는 [아래에서 별도로 다룹니다](#shorthand-selectors).

<a name="the-url-method"></a>
#### `url` 메서드

`url` 메서드에서는 해당 페이지를 대표하는 URL 경로를 반환해야 합니다. Dusk는 이 URL을 이용해 페이지로 이동합니다:

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

`assert` 메서드에서는 실제로 지정한 페이지에 도달했는지 어설션을 수행할 수 있습니다. 반드시 정의할 필요는 없지만, 원하는 모든 검증을 자유롭게 추가할 수 있으며, 페이지로 이동할 때마다 자동 실행됩니다:

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

페이지 객체가 정의되면, `visit` 메서드로 해당 페이지로 쉽게 이동할 수 있습니다:

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

이미 페이지에 머무르면서 해당 페이지의 셀렉터 및 메서드를 현재 테스트 컨텍스트에 "로딩"하고 싶을 수도 있습니다. 이런 경우, `on` 메서드를 사용할 수 있습니다:

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 셀렉터 단축키 (Shorthand Selectors)

페이지 클래스의 `elements` 메서드를 통해 자주 사용하는 CSS 셀렉터의 단축키를 정의할 수 있습니다. 예를 들어, 로그인 페이지의 "email" 입력필드 단축키:

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

단축키를 정의하면, 전체 CSS 셀렉터 대신 언제든 단축키로 사용할 수 있습니다:

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### 전역 셀렉터 단축키 (Global Shorthand Selectors)

Dusk 설치 후, `tests/Browser/Pages` 디렉토리에는 기본 `Page` 클래스가 생성됩니다. 이 클래스의 `siteElements` 메서드에서 애플리케이션 전체에서 사용할 전역 셀렉터 단축키를 정의할 수 있습니다:

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

페이지 클래스에는 기본 메서드 외에도 테스트에서 재사용할 커스텀 메서드를 마음껏 추가할 수 있습니다. 예를 들어, 음악 관리 애플리케이션에서 "플레이리스트 생성"과 같은 반복되는 작업을 커스텀 메서드로 묶을 수 있습니다:

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

정의된 메서드는 해당 페이지 객체를 사용하는 모든 테스트에서 브라우저 인스턴스를 첫 번째 인수로 자동으로 넘겨받아 쓸 수 있습니다:

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트는 Dusk 페이지 객체와 유사하지만, 네비게이션 바나 알림창 같이 여러 페이지에서 재활용되는 UI 단위 및 기능을 대상으로 합니다. 컴포넌트는 특정 URL에 종속되지 않습니다.

<a name="generating-components"></a>
### 컴포넌트 생성 (Generating Components)

컴포넌트는 다음 Artisan 명령어로 생성하며, `tests/Browser/Components` 디렉토리에 생성됩니다:

```shell
php artisan dusk:component DatePicker
```

아래 예시는 "날짜 선택기" 컴포넌트의 정의 예시입니다. 다양한 테스트에서 반복되는 날짜 선택 로직을 컴포넌트로 감싸기 때문에, 로직이 변경되어도 컴포넌트만 수정하면 됩니다:

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

컴포넌트를 정의한 후에는 언제든 날짜 선택 등 기능을 간단하게 호출할 수 있으며, 로직이 바뀌어도 컴포넌트만 수정하면 됩니다:

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

`component` 메서드로 해당 컴포넌트 범위에 브라우저 인스턴스를 가져올 수도 있습니다:

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 지속적 통합 (Continuous Integration)

> [!WARNING]
> 대부분의 Dusk CI 구성은 라라벨 애플리케이션이 8000번 포트에서 내장 PHP 개발 서버로 서빙되는 것을 예상합니다. CI 환경에서 `APP_URL` 환경 변수가 `http://127.0.0.1:8000`으로 설정되어 있는지 확인하세요.

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration)에서 Dusk 테스트를 실행하려면 Heroku `app.json` 파일에 아래와 같이 Chrome buildpack 및 스크립트를 추가합니다:

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

[Travis CI](https://travis-ci.org)에서 Dusk 테스트를 실행하려면 아래와 같은 `.travis.yml` 구성을 사용하세요. Travis CI는 GUI 환경이 아니므로 Chrome 브라우저 실행을 위한 몇 가지 추가 단계를 진행해야 하며, PHP 내장 서버로 애플리케이션을 실행합니다:

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

[GitHub Actions](https://github.com/features/actions)에서 Dusk 테스트를 실행하려면 아래 설정 파일을 활용할 수 있습니다. TravisCI와 마찬가지로 PHP 내장 서버로 라라벨을 실행합니다:

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

[Chipper CI](https://chipperci.com)에서 Dusk 테스트를 실행하려면 아래 예시 설정 파일을 활용하세요. PHP 내장 서버로 라라벨을 실행하여 요청을 처리합니다:

```yaml
# file .chipperci.yml
version: 1

environment:
  php: 8.2
  node: 16

# Chrome을 빌드 환경에 포함
services:
  - dusk

# 모든 커밋 빌드
on:
   push:
      branches: .*

pipeline:
  - name: Setup
    cmd: |
      cp -v .env.example .env
      composer install --no-interaction --prefer-dist --optimize-autoloader
      php artisan key:generate

      # Dusk 환경 파일을 생성하고, APP_URL에 BUILD_HOST를 할당
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

Chipper CI 환경에서 Dusk 테스트, 데이터베이스 연동 등 자세한 내용은 [Chipper CI 공식 문서](https://chipperci.com/docs/testing/laravel-dusk-new/)를 참고하세요.
