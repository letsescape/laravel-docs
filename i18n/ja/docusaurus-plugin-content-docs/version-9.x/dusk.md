<!-- # Laravel Dusk -->
# Laravel Dusk

- [Introduction](#introduction)
- [Installation](#installation)
    - [Managing ChromeDriver Installations](#managing-chromedriver-installations)
    - [Using Other Browsers](#using-other-browsers)
- [Getting Started](#getting-started)
    - [Generating Tests](#generating-tests)
    - [Resetting The Database After Each Test](#resetting-the-database-after-each-test)
    - [Running Tests](#running-tests)
    - [Environment Handling](#environment-handling)
- [Browser Basics](#browser-basics)
    - [Creating Browsers](#creating-browsers)
    - [Navigation](#navigation)
    - [Resizing Browser Windows](#resizing-browser-windows)
    - [Browser Macros](#browser-macros)
    - [Authentication](#authentication)
    - [Cookies](#cookies)
    - [Executing JavaScript](#executing-javascript)
    - [Taking A Screenshot](#taking-a-screenshot)
    - [Storing Console Output To Disk](#storing-console-output-to-disk)
    - [Storing Page Source To Disk](#storing-page-source-to-disk)
- [Interacting With Elements](#interacting-with-elements)
    - [Dusk Selectors](#dusk-selectors)
    - [Text, Values, & Attributes](#text-values-and-attributes)
    - [Interacting With Forms](#interacting-with-forms)
    - [Attaching Files](#attaching-files)
    - [Pressing Buttons](#pressing-buttons)
    - [Clicking Links](#clicking-links)
    - [Using The Keyboard](#using-the-keyboard)
    - [Using The Mouse](#using-the-mouse)
    - [JavaScript Dialogs](#javascript-dialogs)
    - [Scoping Selectors](#scoping-selectors)
    - [Waiting For Elements](#waiting-for-elements)
    - [Scrolling An Element Into View](#scrolling-an-element-into-view)
- [Available Assertions](#available-assertions)
- [Pages](#pages)
    - [Generating Pages](#generating-pages)
    - [Configuring Pages](#configuring-pages)
    - [Navigating To Pages](#navigating-to-pages)
    - [Shorthand Selectors](#shorthand-selectors)
    - [Page Methods](#page-methods)
- [Components](#components)
    - [Generating Components](#generating-components)
    - [Using Components](#using-components)
- [Continuous Integration](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [Travis CI](#running-tests-on-travis-ci)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Dusk](https://github.com/laravel/dusk) provides an expressive, easy-to-use browser automation and testing API. By default, Dusk does not require you to install JDK or Selenium on your local computer. Instead, Dusk uses a standalone [ChromeDriver](https://sites.google.com/chromium.org/driver) installation. However, you are free to utilize any other Selenium compatible driver you wish. -->
[Laravel Dusk](https://github.com/laravel/dusk) は、表現力豊かで使いやすいブラウザ自動化およびテスト API を提供します。デフォルトでは、Dusk ではローカル コンピューターに JDK または Selenium をインストールする必要はありません。代わりに、Dusk はスタンドアロン [ChromeDriver](https://sites.google.com/chromium.org/driver) インストールを使用します。ただし、他の Selenium 互換ドライバを自由に利用できます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, you should install [Google Chrome](https://www.google.com/chrome) and add the `laravel/dusk` Composer dependency to your project: -->
まず、[Google Chrome](https://www.google.com/chrome) をインストールし、`laravel/dusk` Composer 依存関係をプロジェクトに追加する必要があります。

```shell
composer require --dev laravel/dusk
```

> [!WARNING]
> Dusk のサービスプロバイダを手動で登録する場合は、運用環境では決して登録しないでください。登録すると、任意のユーザーがアプリケーションで認証できる可能性があります。

<!-- After installing the Dusk package, execute the `dusk:install` Artisan command. The `dusk:install` command will create a `tests/Browser` directory, an example Dusk test, and install the Chrome Driver binary for your operating system: -->
Dusk パッケージをインストールした後、`dusk:install` Artisan コマンドを実行します。 `dusk:install` コマンドは、Dusk テストのサンプルである `tests/Browser` ディレクトリを作成し、オペレーティング システム用の Chrome ドライバ バイナリをインストールします。

```shell
php artisan dusk:install
```

<!-- Next, set the `APP_URL` environment variable in your application's `.env` file. This value should match the URL you use to access your application in a browser. -->
次に、アプリケーションの `.env` ファイルに `APP_URL` 環境変数を設定します。この値は、ブラウザでアプリケーションにアクセスするために使用する URL と一致する必要があります。

> [!NOTE]
> [Laravel Sail](/docs/9.x/sail) を使用してローカル開発環境を管理している場合は、[configuring and running Dusk tests](/docs/9.x/sail#laravel-dusk) の Sail ドキュメントも参照してください。

<a name="managing-chromedriver-installations"></a>
<!-- ### Managing ChromeDriver Installations -->
### Managing ChromeDriver Installations

<!-- If you would like to install a different version of ChromeDriver than what is installed by Laravel Dusk via the `dusk:install` command, you may use the `dusk:chrome-driver` command: -->
Laravel Dusk によって `dusk:install` コマンドを使用してインストールされるものとは異なるバージョンの ChromeDriver をインストールしたい場合は、`dusk:chrome-driver` コマンドを使用できます。

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
> Dusk では、`chromedriver` バイナリが実行可能である必要があります。 Dusk の実行に問題がある場合は、コマンド `chmod -R 0755 vendor/laravel/dusk/bin/` を使用してバイナリが実行可能であることを確認する必要があります。

<a name="using-other-browsers"></a>
<!-- ### Using Other Browsers -->
### Using Other Browsers

<!-- By default, Dusk uses Google Chrome and a standalone [ChromeDriver](https://sites.google.com/chromium.org/driver) installation to run your browser tests. However, you may start your own Selenium server and run your tests against any browser you wish. -->
デフォルトでは、Dusk は Google Chrome とスタンドアロン [ChromeDriver](https://sites.google.com/chromium.org/driver) インストールを使用してブラウザ テストを実行します。ただし、独自の Selenium サーバーを起動し、任意のブラウザに対してテストを実行することもできます。

<!-- To get started, open your `tests/DuskTestCase.php` file, which is the base Dusk test case for your application. Within this file, you can remove the call to the `startChromeDriver` method. This will stop Dusk from automatically starting the ChromeDriver: -->
まず、アプリケーションのベース Dusk テスト ケースである `tests/DuskTestCase.php` ファイルを開きます。このファイル内で、`startChromeDriver` メソッドの呼び出しを削除できます。これにより、Dusk が ChromeDriver を自動的に起動しなくなります。

```
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 * @return void
 */
public static function prepare()
{
    // static::startChromeDriver();
}
```

<!-- Next, you may modify the `driver` method to connect to the URL and port of your choice. In addition, you may modify the "desired capabilities" that should be passed to the WebDriver: -->
次に、選択した URL とポートに接続するように `driver` メソッドを変更できます。さらに、WebDriver に渡す必要がある「必要な機能」を変更することもできます。

```
/**
 * Create the RemoteWebDriver instance.
 *
 * @return \Facebook\WebDriver\Remote\RemoteWebDriver
 */
protected function driver()
{
    return RemoteWebDriver::create(
        'http://localhost:4444/wd/hub', DesiredCapabilities::phantomjs()
    );
}
```

<a name="getting-started"></a>
<!-- ## Getting Started -->
## Getting Started

<a name="generating-tests"></a>
<!-- ### Generating Tests -->
### Generating Tests

<!-- To generate a Dusk test, use the `dusk:make` Artisan command. The generated test will be placed in the `tests/Browser` directory: -->
Dusk テストを生成するには、`dusk:make` Artisan コマンドを使用します。生成されたテストは、`tests/Browser` ディレクトリに配置されます。

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
<!-- ### Resetting The Database After Each Test -->
### Resetting The Database After Each Test

<!-- Most of the tests you write will interact with pages that retrieve data from your application's database; however, your Dusk tests should never use the `RefreshDatabase` trait. The `RefreshDatabase` trait leverages database transactions which will not be applicable or available across HTTP requests. Instead, you have two options: the `DatabaseMigrations` trait and the `DatabaseTruncation` trait. -->
作成するテストのほとんどは、アプリケーションのデータベースからデータを取得するページと対話します。ただし、Dusk テストでは `RefreshDatabase` 特性を使用しないでください。 `RefreshDatabase` トレイトは、HTTP リクエスト全体では適用できない、または使用できないデータベース トランザクションを利用します。代わりに、`DatabaseMigrations` トレイトと `DatabaseTruncation` トレイトの 2 つのオプションがあります。

<a name="reset-migrations"></a>
<!-- #### Using Database Migrations -->
#### Using Database Migrations

<!-- The `DatabaseMigrations` trait will run your database migrations before each test. However, dropping and re-creating your database tables for each test is typically slower than truncating the tables: -->
`DatabaseMigrations` トレイトは、各テストの前にデータベースの移行を実行します。ただし、テストごとにデータベース テーブルを削除して再作成するのは、通常、テーブルを切り捨てるよりも時間がかかります。

```
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Chrome;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;
}
```

> [!WARNING]
> Dusk テストの実行時には SQLite インメモリ データベースを使用できない場合があります。ブラウザは独自のプロセス内で実行されるため、他のプロセスのメモリ内データベースにアクセスすることはできません。

<a name="reset-truncation"></a>
<!-- #### Using Database Truncation -->
#### Using Database Truncation

<!-- Before using the `DatabaseTruncation` trait, you must install the `doctrine/dbal` package using the Composer package manager: -->
`DatabaseTruncation` トレイトを使用する前に、Composer パッケージ マネージャーを使用して `doctrine/dbal` パッケージをインストールする必要があります。

```shell
composer require --dev doctrine/dbal
```

<!-- The `DatabaseTruncation` trait will migrate your database on the first test in order to ensure your database tables have been properly created. However, on subsequent tests, the database's tables will simply be truncated - providing a speed boost over re-running all of your database migrations: -->
`DatabaseTruncation` トレイトは、データベース テーブルが適切に作成されたことを確認するために、最初のテストでデータベースを移行します。ただし、後続のテストではデータベースのテーブルが単純に切り捨てられるため、すべてのデータベース移行を再実行するよりも速度が向上します。

```
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTruncation;
use Laravel\Dusk\Chrome;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseTruncation;
}
```

<!-- By default, this trait will truncate all tables except the `migrations` table. If you would like to customize the tables that should be truncated, you may define a `$tablesToTruncate` property on your test class: -->
デフォルトでは、この特性は `migrations` テーブルを除くすべてのテーブルを切り捨てます。切り詰めるテーブルをカスタマイズしたい場合は、テスト クラスで `$tablesToTruncate` プロパティを定義できます。

```
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

<!-- Alternatively, you may define an `$exceptTables` property on your test class to specify which tables should be excluded from truncation: -->
あるいは、テスト クラスで `$exceptTables` プロパティを定義して、切り捨てから除外するテーブルを指定することもできます。

```
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

<!-- To specify the database connections that should have their tables truncated, you may define a `$connectionsToTruncate` property on your test class: -->
テーブルを切り詰める必要があるデータベース接続を指定するには、テスト クラスで `$connectionsToTruncate` プロパティを定義できます。

```
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

<a name="running-tests"></a>
<!-- ### Running Tests -->
### Running Tests

<!-- To run your browser tests, execute the `dusk` Artisan command: -->
ブラウザーのテストを実行するには、`dusk` Artisan コマンドを実行します。

```shell
php artisan dusk
```

<!-- If you had test failures the last time you ran the `dusk` command, you may save time by re-running the failing tests first using the `dusk:fails` command: -->
前回 `dusk` コマンドを実行したときにテストが失敗した場合は、最初に `dusk:fails` コマンドを使用して、失敗したテストを再実行することで時間を節約できます。

```shell
php artisan dusk:fails
```

<!-- The `dusk` command accepts any argument that is normally accepted by the PHPUnit test runner, such as allowing you to only run the tests for a given [group](https://phpunit.readthedocs.io/en/9.5/annotations.html#group): -->
`dusk` コマンドは、特定の [group](https://phpunit.readthedocs.io/en/9.5/annotations.html#group) のテストのみを実行できるようにするなど、PHPUnit テスト ランナーによって通常受け入れられる任意の引数を受け入れます。

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/9.x/sail) を使用してローカル開発環境を管理している場合は、[configuring and running Dusk tests](/docs/9.x/sail#laravel-dusk) の Sail ドキュメントを参照してください。

<a name="manually-starting-chromedriver"></a>
<!-- #### Manually Starting ChromeDriver -->
#### Manually Starting ChromeDriver

<!-- By default, Dusk will automatically attempt to start ChromeDriver. If this does not work for your particular system, you may manually start ChromeDriver before running the `dusk` command. If you choose to start ChromeDriver manually, you should comment out the following line of your `tests/DuskTestCase.php` file: -->
デフォルトでは、Dusk は自動的に ChromeDriver の起動を試みます。これが特定のシステムで機能しない場合は、`dusk` コマンドを実行する前に ChromeDriver を手動で起動できます。 ChromeDriver を手動で開始することを選択した場合は、`tests/DuskTestCase.php` ファイルの次の行をコメント アウトする必要があります。

```
/**
 * Prepare for Dusk test execution.
 *
 * @beforeClass
 * @return void
 */
public static function prepare()
{
    // static::startChromeDriver();
}
```

<!-- In addition, if you start ChromeDriver on a port other than 9515, you should modify the `driver` method of the same class to reflect the correct port: -->
さらに、9515 以外のポートで ChromeDriver を起動する場合は、同じクラスの `driver` メソッドを変更して、正しいポートを反映する必要があります。

```
/**
 * Create the RemoteWebDriver instance.
 *
 * @return \Facebook\WebDriver\Remote\RemoteWebDriver
 */
protected function driver()
{
    return RemoteWebDriver::create(
        'http://localhost:9515', DesiredCapabilities::chrome()
    );
}
```

<a name="environment-handling"></a>
<!-- ### Environment Handling -->
### Environment Handling

<!-- To force Dusk to use its own environment file when running tests, create a `.env.dusk.{environment}` file in the root of your project. For example, if you will be initiating the `dusk` command from your `local` environment, you should create a `.env.dusk.local` file. -->
テストの実行時に Dusk に独自の環境ファイルを使用させるには、プロジェクトのルートに `.env.dusk.{environment}` ファイルを作成します。たとえば、`local` 環境から `dusk` コマンドを開始する場合は、`.env.dusk.local` ファイルを作成する必要があります。

<!-- When running tests, Dusk will back-up your `.env` file and rename your Dusk environment to `.env`. Once the tests have completed, your `.env` file will be restored. -->
テストを実行するとき、Dusk は `.env` ファイルをバックアップし、Dusk 環境の名前を `.env` に変更します。テストが完了すると、`.env` ファイルが復元されます。

<a name="browser-basics"></a>
<!-- ## Browser Basics -->
## Browser Basics

<a name="creating-browsers"></a>
<!-- ### Creating Browsers -->
### Creating Browsers

<!-- To get started, let's write a test that verifies we can log into our application. After generating a test, we can modify it to navigate to the login page, enter some credentials, and click the "Login" button. To create a browser instance, you may call the `browse` method from within your Dusk test: -->
まず、アプリケーションにログインできることを確認するテストを作成しましょう。テストを生成した後、ログイン ページに移動し、資格情報を入力して、[ログイン] ボタンをクリックするようにテストを変更できます。ブラウザー インスタンスを作成するには、Dusk テスト内から `browse` メソッドを呼び出すことができます。

```
<?php

namespace Tests\Browser;

use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Chrome;
use Tests\DuskTestCase;

class ExampleTest extends DuskTestCase
{
    use DatabaseMigrations;

    /**
     * A basic browser test example.
     *
     * @return void
     */
    public function test_basic_example()
    {
        $user = User::factory()->create([
            'email' => 'taylor@laravel.com',
        ]);

        $this->browse(function ($browser) use ($user) {
            $browser->visit('/login')
                    ->type('email', $user->email)
                    ->type('password', 'password')
                    ->press('Login')
                    ->assertPathIs('/home');
        });
    }
}
```

<!-- As you can see in the example above, the `browse` method accepts a closure. A browser instance will automatically be passed to this closure by Dusk and is the main object used to interact with and make assertions against your application. -->
上の例でわかるように、`browse` メソッドはクロージャを受け入れます。ブラウザ インスタンスは、Dusk によって自動的にこのクロージャに渡され、アプリケーションと対話したり、アプリケーションに対してアサーションを行ったりするために使用される主要なオブジェクトです。

<a name="creating-multiple-browsers"></a>
<!-- #### Creating Multiple Browsers -->
#### Creating Multiple Browsers

<!-- Sometimes you may need multiple browsers in order to properly carry out a test. For example, multiple browsers may be needed to test a chat screen that interacts with websockets. To create multiple browsers, simply add more browser arguments to the signature of the closure given to the `browse` method: -->
テストを適切に実行するために複数のブラウザが必要になる場合があります。たとえば、WebSocket と対話するチャット画面をテストするには、複数のブラウザーが必要になる場合があります。複数のブラウザを作成するには、`browse` メソッドに指定されたクロージャのシグネチャにブラウザ引数を追加するだけです。

```
$this->browse(function ($first, $second) {
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
<!-- ### Navigation -->
### Navigation

<!-- The `visit` method may be used to navigate to a given URI within your application: -->
`visit` メソッドは、アプリケーション内の特定の URI に移動するために使用できます。

```
$browser->visit('/login');
```

<!-- You may use the `visitRoute` method to navigate to a [named route](/docs/9.x/routing#named-routes): -->
`visitRoute` メソッドを使用して、[named route](/docs/9.x/routing#named-routes) に移動できます。

```
$browser->visitRoute('login');
```

<!-- You may navigate "back" and "forward" using the `back` and `forward` methods: -->
`back` メソッドと `forward` メソッドを使用して、「戻る」と「進む」に移動できます。

```
$browser->back();

$browser->forward();
```

<!-- You may use the `refresh` method to refresh the page: -->
`refresh` メソッドを使用してページを更新できます。

```
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
<!-- ### Resizing Browser Windows -->
### Resizing Browser Windows

<!-- You may use the `resize` method to adjust the size of the browser window: -->
`resize` メソッドを使用して、ブラウザ ウィンドウのサイズを調整できます。

```
$browser->resize(1920, 1080);
```

<!-- The `maximize` method may be used to maximize the browser window: -->
`maximize` メソッドは、ブラウザ ウィンドウを最大化するために使用できます。

```
$browser->maximize();
```

<!-- The `fitContent` method will resize the browser window to match the size of its content: -->
`fitContent` メソッドは、コンテンツのサイズに合わせてブラウザ ウィンドウのサイズを変更します。

```
$browser->fitContent();
```

<!-- When a test fails, Dusk will automatically resize the browser to fit the content prior to taking a screenshot. You may disable this feature by calling the `disableFitOnFailure` method within your test: -->
テストが失敗すると、Dusk はスクリーンショットを撮る前に、コンテンツに合わせてブラウザのサイズを自動的に変更します。テスト内で `disableFitOnFailure` メソッドを呼び出すことで、この機能を無効にすることができます。

```
$browser->disableFitOnFailure();
```

<!-- You may use the `move` method to move the browser window to a different position on your screen: -->
`move` メソッドを使用して、ブラウザ ウィンドウを画面上の別の位置に移動できます。

```
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
<!-- ### Browser Macros -->
### Browser Macros

<!-- If you would like to define a custom browser method that you can re-use in a variety of your tests, you may use the `macro` method on the `Browser` class. Typically, you should call this method from a [service provider's](/docs/9.x/providers) `boot` method: -->
さまざまなテストで再利用できるカスタム ブラウザ メソッドを定義したい場合は、`Browser` クラスの `macro` メソッドを使用できます。通常、このメソッドは [service provider's](/docs/9.x/providers) `boot` メソッドから呼び出す必要があります。

```
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Dusk\Browser;

class DuskServiceProvider extends ServiceProvider
{
    /**
     * Register Dusk's browser macros.
     *
     * @return void
     */
    public function boot()
    {
        Browser::macro('scrollToElement', function ($element = null) {
            $this->script("$('html, body').animate({ scrollTop: $('$element').offset().top }, 0);");

            return $this;
        });
    }
}
```

<!-- The `macro` function accepts a name as its first argument, and a closure as its second. The macro's closure will be executed when calling the macro as a method on a `Browser` instance: -->
`macro` 関数は、最初の引数として名前を受け入れ、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャは、`Browser` インスタンスのメソッドとしてマクロを呼び出すときに実行されます。

```
$this->browse(function ($browser) use ($user) {
    $browser->visit('/pay')
            ->scrollToElement('#credit-card-details')
            ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<!-- Often, you will be testing pages that require authentication. You can use Dusk's `loginAs` method in order to avoid interacting with your application's login screen during every test. The `loginAs` method accepts a primary key associated with your authenticatable model or an authenticatable model instance: -->
多くの場合、認証が必要なページをテストすることになります。 Dusk の `loginAs` メソッドを使用すると、テストのたびにアプリケーションのログイン画面との対話を避けることができます。 `loginAs` メソッドは、認証可能なモデルまたは認証可能なモデル インスタンスに関連付けられた主キーを受け入れます。

```
use App\Models\User;

$this->browse(function ($browser) {
    $browser->loginAs(User::find(1))
          ->visit('/home');
});
```

> [!WARNING]
> `loginAs` メソッドを使用した後、ユーザー セッションはファイル内のすべてのテストに対して維持されます。

<a name="cookies"></a>
<!-- ### Cookies -->
### Cookies

<!-- You may use the `cookie` method to get or set an encrypted cookie's value. By default, all of the cookies created by Laravel are encrypted: -->
`cookie` メソッドを使用して、暗号化された Cookie の値を取得または設定できます。デフォルトでは、Laravel によって作成されたすべての Cookie は暗号化されます。

```
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

<!-- You may use the `plainCookie` method to get or set an unencrypted cookie's value: -->
`plainCookie` メソッドを使用して、暗号化されていない Cookie の値を取得または設定できます。

```
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

<!-- You may use the `deleteCookie` method to delete the given cookie: -->
`deleteCookie` メソッドを使用して、指定された Cookie を削除できます。

```
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
<!-- ### Executing JavaScript -->
### Executing JavaScript

<!-- You may use the `script` method to execute arbitrary JavaScript statements within the browser: -->
`script` メソッドを使用して、ブラウザ内で任意の JavaScript ステートメントを実行できます。

```
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
<!-- ### Taking A Screenshot -->
### Taking A Screenshot

<!-- You may use the `screenshot` method to take a screenshot and store it with the given filename. All screenshots will be stored within the `tests/Browser/screenshots` directory: -->
`screenshot` メソッドを使用してスクリーンショットを撮り、指定されたファイル名で保存できます。すべてのスクリーンショットは、`tests/Browser/screenshots` ディレクトリ内に保存されます。

```
$browser->screenshot('filename');
```

<!-- The `responsiveScreenshots` method may be used to take a series of screenshots at various breakpoints: -->
`responsiveScreenshots` メソッドを使用すると、さまざまなブレークポイントで一連のスクリーンショットを取得できます。

```
$browser->responsiveScreenshots('filename');
```

<a name="storing-console-output-to-disk"></a>
<!-- ### Storing Console Output To Disk -->
### Storing Console Output To Disk

<!-- You may use the `storeConsoleLog` method to write the current browser's console output to disk with the given filename. Console output will be stored within the `tests/Browser/console` directory: -->
`storeConsoleLog` メソッドを使用して、現在のブラウザのコンソール出力を指定されたファイル名でディスクに書き込むことができます。コンソール出力は、`tests/Browser/console` ディレクトリ内に保存されます。

```
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
<!-- ### Storing Page Source To Disk -->
### Storing Page Source To Disk

<!-- You may use the `storeSource` method to write the current page's source to disk with the given filename. The page source will be stored within the `tests/Browser/source` directory: -->
`storeSource` メソッドを使用して、現在のページのソースを指定されたファイル名でディスクに書き込むことができます。ページのソースは、`tests/Browser/source` ディレクトリ内に保存されます。

```
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
<!-- ## Interacting With Elements -->
## Interacting With Elements

<a name="dusk-selectors"></a>
<!-- ### Dusk Selectors -->
### Dusk Selectors

<!-- Choosing good CSS selectors for interacting with elements is one of the hardest parts of writing Dusk tests. Over time, frontend changes can cause CSS selectors like the following to break your tests: -->
要素と対話するための適切な CSS セレクターを選択することは、Dusk テストを作成する際に最も難しい部分の 1 つです。時間の経過とともに、フロントエンドの変更により、次のような CSS セレクターがテストを中断する可能性があります。

```
// HTML...

<button>Login</button>

// Test...

$browser->click('.login-page .container div > button');
```

<!-- Dusk selectors allow you to focus on writing effective tests rather than remembering CSS selectors. To define a selector, add a `dusk` attribute to your HTML element. Then, when interacting with a Dusk browser, prefix the selector with `@` to manipulate the attached element within your test: -->
Dusk セレクターを使用すると、CSS セレクターを覚えるのではなく、効果的なテストの作成に集中できます。セレクターを定義するには、HTML 要素に `dusk` 属性を追加します。次に、Dusk ブラウザを操作するときに、セレクターの先頭に `@` を付けて、テスト内で添付された要素を操作します。

```
// HTML...

<button dusk="login-button">Login</button>

// Test...

$browser->click('@login-button');
```

<a name="text-values-and-attributes"></a>
<!-- ### Text, Values, & Attributes -->
### Text, Values, & Attributes

<a name="retrieving-setting-values"></a>
<!-- #### Retrieving & Setting Values -->
#### Retrieving & Setting Values

<!-- Dusk provides several methods for interacting with the current value, display text, and attributes of elements on the page. For example, to get the "value" of an element that matches a given CSS or Dusk selector, use the `value` method: -->
Dusk は、ページ上の要素の現在の値、表示テキスト、および属性を操作するためのメソッドをいくつか提供します。たとえば、特定の CSS または Dusk セレクターに一致する要素の「値」を取得するには、`value` メソッドを使用します。

```
// Retrieve the value...
$value = $browser->value('selector');

// Set the value...
$browser->value('selector', 'value');
```

<!-- You may use the `inputValue` method to get the "value" of an input element that has a given field name: -->
`inputValue` メソッドを使用して、指定されたフィールド名を持つ入力要素の「値」を取得できます。

```
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
<!-- #### Retrieving Text -->
#### Retrieving Text

<!-- The `text` method may be used to retrieve the display text of an element that matches the given selector: -->
`text` メソッドは、指定されたセレクターに一致する要素の表示テキストを取得するために使用できます。

```
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
<!-- #### Retrieving Attributes -->
#### Retrieving Attributes

<!-- Finally, the `attribute` method may be used to retrieve the value of an attribute of an element matching the given selector: -->
最後に、`attribute` メソッドを使用して、指定されたセレクターに一致する要素の属性の値を取得できます。

```
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
<!-- ### Interacting With Forms -->
### Interacting With Forms

<a name="typing-values"></a>
<!-- #### Typing Values -->
#### Typing Values

<!-- Dusk provides a variety of methods for interacting with forms and input elements. First, let's take a look at an example of typing text into an input field: -->
Dusk は、フォームや入力要素を操作するためのさまざまなメソッドを提供します。まず、入力フィールドにテキストを入力する例を見てみましょう。

```
$browser->type('email', 'taylor@laravel.com');
```

<!-- Note that, although the method accepts one if necessary, we are not required to pass a CSS selector into the `type` method. If a CSS selector is not provided, Dusk will search for an `input` or `textarea` field with the given `name` attribute. -->
このメソッドは必要に応じて CSS セレクターを受け入れますが、CSS セレクターを `type` メソッドに渡す必要はないことに注意してください。 CSS セレクターが提供されていない場合、Dusk は指定された `name` 属性を持つ `input` または `textarea` フィールドを検索します。

<!-- To append text to a field without clearing its content, you may use the `append` method: -->
内容をクリアせずにフィールドにテキストを追加するには、`append` メソッドを使用できます。

```
$browser->type('tags', 'foo')
        ->append('tags', ', bar, baz');
```

<!-- You may clear the value of an input using the `clear` method: -->
`clear` メソッドを使用して入力の値をクリアできます。

```
$browser->clear('email');
```

<!-- You can instruct Dusk to type slowly using the `typeSlowly` method. By default, Dusk will pause for 100 milliseconds between key presses. To customize the amount of time between key presses, you may pass the appropriate number of milliseconds as the third argument to the method: -->
`typeSlowly` メソッドを使用して、Dusk にゆっくり入力するように指示できます。デフォルトでは、Dusk はキーを押すまでの間に 100 ミリ秒間一時停止します。キーを押すまでの時間をカスタマイズするには、メソッドの 3 番目の引数として適切なミリ秒数を渡します。

```
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

<!-- You may use the `appendSlowly` method to append text slowly: -->
`appendSlowly` メソッドを使用すると、テキストをゆっくり追加できます。

```
$browser->type('tags', 'foo')
        ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
<!-- #### Dropdowns -->
#### Dropdowns

<!-- To select a value available on a `select` element, you may use the `select` method. Like the `type` method, the `select` method does not require a full CSS selector. When passing a value to the `select` method, you should pass the underlying option value instead of the display text: -->
`select` 要素で使用可能な値を選択するには、`select` メソッドを使用できます。 `type` メソッドと同様、`select` メソッドには完全な CSS セレクターは必要ありません。 `select` メソッドに値を渡すときは、表示テキストの代わりに基になるオプション値を渡す必要があります。

```
$browser->select('size', 'Large');
```

<!-- You may select a random option by omitting the second argument: -->
2 番目の引数を省略すると、ランダムなオプションを選択できます。

```
$browser->select('size');
```

<!-- By providing an array as the second argument to the `select` method, you can instruct the method to select multiple options: -->
`select` メソッドの 2 番目の引数として配列を指定すると、メソッドに複数のオプションを選択するように指示できます。

```
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
<!-- #### Checkboxes -->
#### Checkboxes

<!-- To "check" a checkbox input, you may use the `check` method. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a checkbox with a matching `name` attribute: -->
チェックボックスの入力を「チェック」するには、`check` メソッドを使用できます。他の多くの入力関連メソッドと同様、完全な CSS セレクターは必要ありません。 CSS セレクターの一致が見つからない場合、Dusk は一致する `name` 属性を持つチェックボックスを検索します。

```
$browser->check('terms');
```

<!-- The `uncheck` method may be used to "uncheck" a checkbox input: -->
`uncheck` メソッドは、チェックボックスの入力を「オフ」にするために使用できます。

```
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
<!-- #### Radio Buttons -->
#### Radio Buttons

<!-- To "select" a `radio` input option, you may use the `radio` method. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a `radio` input with matching `name` and `value` attributes: -->
`radio` 入力オプションを「選択」するには、`radio` メソッドを使用できます。他の多くの入力関連メソッドと同様、完全な CSS セレクターは必要ありません。 CSS セレクターの一致が見つからない場合、Dusk は `name` 属性と `value` 属性が一致する `radio` 入力を検索します。

```
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
<!-- ### Attaching Files -->
### Attaching Files

<!-- The `attach` method may be used to attach a file to a `file` input element. Like many other input related methods, a full CSS selector is not required. If a CSS selector match can't be found, Dusk will search for a `file` input with a matching `name` attribute: -->
`attach` メソッドは、`file` 入力要素にファイルを添付するために使用できます。他の多くの入力関連メソッドと同様、完全な CSS セレクターは必要ありません。 CSS セレクターの一致が見つからない場合、Dusk は一致する `name` 属性を持つ `file` 入力を検索します。

```
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> アタッチ機能を使用するには、`Zip` PHP 拡張機能がサーバーにインストールされ、有効になっている必要があります。

<a name="pressing-buttons"></a>
<!-- ### Pressing Buttons -->
### Pressing Buttons

<!-- The `press` method may be used to click a button element on the page. The argument given to the `press` method may be either the display text of the button or a CSS / Dusk selector: -->
`press` メソッドは、ページ上のボタン要素をクリックするために使用できます。 `press` メソッドに指定される引数は、ボタンの表示テキストまたは CSS / Dusk セレクターのいずれかです。

```
$browser->press('Login');
```

<!-- When submitting forms, many applications disable the form's submission button after it is pressed and then re-enable the button when the form submission's HTTP request is complete. To press a button and wait for the button to be re-enabled, you may use the `pressAndWaitFor` method: -->
フォームを送信するとき、多くのアプリケーションは、フォームの送信ボタンが押された後に無効にし、フォーム送信の HTTP リクエストが完了するとボタンを再度有効にします。ボタンを押してボタンが再び有効になるまで待つには、`pressAndWaitFor` メソッドを使用できます。

```
// Press the button and wait a maximum of 5 seconds for it to be enabled...
$browser->pressAndWaitFor('Save');

// Press the button and wait a maximum of 1 second for it to be enabled...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
<!-- ### Clicking Links -->
### Clicking Links

<!-- To click a link, you may use the `clickLink` method on the browser instance. The `clickLink` method will click the link that has the given display text: -->
リンクをクリックするには、ブラウザ インスタンスで `clickLink` メソッドを使用できます。 `clickLink` メソッドは、指定された表示テキストを持つリンクをクリックします。

```
$browser->clickLink($linkText);
```

<!-- You may use the `seeLink` method to determine if a link with the given display text is visible on the page: -->
`seeLink` メソッドを使用して、指定された表示テキストを持つリンクがページ上に表示されるかどうかを判断できます。

```
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> これらのメソッドは jQuery と対話します。ページで jQuery が使用できない場合、Dusk はそれをページに自動的に挿入し、テスト期間中使用できるようにします。

<a name="using-the-keyboard"></a>
<!-- ### Using The Keyboard -->
### Using The Keyboard

<!-- The `keys` method allows you to provide more complex input sequences to a given element than normally allowed by the `type` method. For example, you may instruct Dusk to hold modifier keys while entering values. In this example, the `shift` key will be held while `taylor` is entered into the element matching the given selector. After `taylor` is typed, `swift` will be typed without any modifier keys: -->
`keys` メソッドを使用すると、`type` メソッドで通常許可されるよりも複雑な入力シーケンスを特定の要素に提供できます。たとえば、値を入力するときに修飾キーを押し続けるように Dusk に指示できます。この例では、指定されたセレクターに一致する要素に `taylor` が入力されている間、`shift` キーが保持されます。 `taylor` を入力すると、修飾キーなしで `swift` が入力されます。

```
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

<!-- Another valuable use case for the `keys` method is sending a "keyboard shortcut" combination to the primary CSS selector for your application: -->
`keys` メソッドのもう 1 つの有益な使用例は、「キーボード ショートカット」の組み合わせをアプリケーションのプライマリ CSS セレクターに送信することです。

```
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` などのすべての修飾キーは、`{}` 文字でラップされ、`Facebook\WebDriver\WebDriverKeys` クラスで定義された定数 ([found on GitHub](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php) など) と一致します。

<a name="using-the-mouse"></a>
<!-- ### Using The Mouse -->
### Using The Mouse

<a name="clicking-on-elements"></a>
<!-- #### Clicking On Elements -->
#### Clicking On Elements

<!-- The `click` method may be used to click on an element matching the given CSS or Dusk selector: -->
`click` メソッドは、指定された CSS または Dusk セレクターに一致する要素をクリックするために使用できます。

```
$browser->click('.selector');
```

<!-- The `clickAtXPath` method may be used to click on an element matching the given XPath expression: -->
`clickAtXPath` メソッドは、指定された XPath 式に一致する要素をクリックするために使用できます。

```
$browser->clickAtXPath('//div[@class = "selector"]');
```

<!-- The `clickAtPoint` method may be used to click on the topmost element at a given pair of coordinates relative to the viewable area of the browser: -->
`clickAtPoint` メソッドを使用すると、ブラウザの表示可能領域を基準とした特定の座標ペアで最上位の要素をクリックできます。

```
$browser->clickAtPoint($x = 0, $y = 0);
```

<!-- The `doubleClick` method may be used to simulate the double click of a mouse: -->
`doubleClick` メソッドは、マウスのダブルクリックをシミュレートするために使用できます。

```
$browser->doubleClick();
```

<!-- The `rightClick` method may be used to simulate the right click of a mouse: -->
`rightClick` メソッドは、マウスの右クリックをシミュレートするために使用できます。

```
$browser->rightClick();

$browser->rightClick('.selector');
```

<!-- The `clickAndHold` method may be used to simulate a mouse button being clicked and held down. A subsequent call to the `releaseMouse` method will undo this behavior and release the mouse button: -->
`clickAndHold` メソッドは、マウス ボタンをクリックして押し続けることをシミュレートするために使用できます。後続の `releaseMouse` メソッドの呼び出しにより、この動作は元に戻され、マウス ボタンが放されます。

```
$browser->clickAndHold()
        ->pause(1000)
        ->releaseMouse();
```

<a name="mouseover"></a>
<!-- #### Mouseover -->
#### Mouseover

<!-- The `mouseover` method may be used when you need to move the mouse over an element matching the given CSS or Dusk selector: -->
`mouseover` メソッドは、指定された CSS または Dusk セレクターに一致する要素上にマウスを移動する必要がある場合に使用できます。

```
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
<!-- #### Drag & Drop -->
#### Drag & Drop

<!-- The `drag` method may be used to drag an element matching the given selector to another element: -->
`drag` メソッドは、指定されたセレクターに一致する要素を別の要素にドラッグするために使用できます。

```
$browser->drag('.from-selector', '.to-selector');
```

<!-- Or, you may drag an element in a single direction: -->
または、要素を単一方向にドラッグすることもできます。

```
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

<!-- Finally, you may drag an element by a given offset: -->
最後に、指定されたオフセットだけ要素をドラッグできます。

```
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
<!-- ### JavaScript Dialogs -->
### JavaScript Dialogs

<!-- Dusk provides various methods to interact with JavaScript Dialogs. For example, you may use the `waitForDialog` method to wait for a JavaScript dialog to appear. This method accepts an optional argument indicating how many seconds to wait for the dialog to appear: -->
Dusk は、JavaScript ダイアログを操作するためのさまざまなメソッドを提供します。たとえば、`waitForDialog` メソッドを使用して、JavaScript ダイアログが表示されるのを待つことができます。このメソッドは、ダイアログが表示されるまで待機する秒数を示すオプションの引数を受け取ります。

```
$browser->waitForDialog($seconds = null);
```

<!-- The `assertDialogOpened` method may be used to assert that a dialog has been displayed and contains the given message: -->
`assertDialogOpened` メソッドは、ダイアログが表示され、指定されたメッセージが含まれていることをアサートするために使用できます。

```
$browser->assertDialogOpened('Dialog message');
```

<!-- If the JavaScript dialog contains a prompt, you may use the `typeInDialog` method to type a value into the prompt: -->
JavaScript ダイアログにプロンプ​​トが含​​まれている場合は、`typeInDialog` メソッドを使用してプロンプトに値を入力できます。

```
$browser->typeInDialog('Hello World');
```

<!-- To close an open JavaScript dialog by clicking the "OK" button, you may invoke the `acceptDialog` method: -->
「OK」ボタンをクリックして開いている JavaScript ダイアログを閉じるには、`acceptDialog` メソッドを呼び出すことができます。

```
$browser->acceptDialog();
```

<!-- To close an open JavaScript dialog by clicking the "Cancel" button, you may invoke the `dismissDialog` method: -->
[キャンセル] ボタンをクリックして開いている JavaScript ダイアログを閉じるには、`dismissDialog` メソッドを呼び出すことができます。

```
$browser->dismissDialog();
```

<a name="scoping-selectors"></a>
<!-- ### Scoping Selectors -->
### Scoping Selectors

<!-- Sometimes you may wish to perform several operations while scoping all of the operations within a given selector. For example, you may wish to assert that some text exists only within a table and then click a button within that table. You may use the `with` method to accomplish this. All operations performed within the closure given to the `with` method will be scoped to the original selector: -->
場合によっては、特定のセレクター内ですべての操作をスコープしながら、複数の操作を実行したい場合があります。たとえば、一部のテキストがテーブル内にのみ存在することを主張し、そのテーブル内のボタンをクリックしたい場合があります。これを実現するには、`with` メソッドを使用できます。 `with` メソッドに指定されたクロージャー内で実行されるすべての操作は、元のセレクターにスコープされます。

```
$browser->with('.table', function ($table) {
    $table->assertSee('Hello World')
          ->clickLink('Delete');
});
```

<!-- You may occasionally need to execute assertions outside of the current scope. You may use the `elsewhere` and `elsewhereWhenAvailable` methods to accomplish this: -->
現在のスコープ外でアサーションを実行する必要がある場合があります。これを実現するには、`elsewhere` メソッドと `elsewhereWhenAvailable` メソッドを使用できます。

```
 $browser->with('.table', function ($table) {
    // Current scope is `body .table`...

    $browser->elsewhere('.page-title', function ($title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });

    $browser->elsewhereWhenAvailable('.page-title', function ($title) {
        // Current scope is `body .page-title`...
        $title->assertSee('Hello World');
    });
 });
```

<a name="waiting-for-elements"></a>
<!-- ### Waiting For Elements -->
### Waiting For Elements

<!-- When testing applications that use JavaScript extensively, it often becomes necessary to "wait" for certain elements or data to be available before proceeding with a test. Dusk makes this a cinch. Using a variety of methods, you may wait for elements to become visible on the page or even wait until a given JavaScript expression evaluates to `true`. -->
JavaScript を広範囲に使用するアプリケーションをテストする場合、多くの場合、テストを続行する前に、特定の要素またはデータが使用可能になるまで「待つ」必要があります。Dusk時はこれが楽になります。さまざまな方法を使用して、要素がページ上に表示されるまで待機したり、特定の JavaScript 式が `true` と評価されるまで待機したりできます。

<a name="waiting"></a>
<!-- #### Waiting -->
#### Waiting

<!-- If you just need to pause the test for a given number of milliseconds, use the `pause` method: -->
指定したミリ秒数だけテストを一時停止する必要がある場合は、`pause` メソッドを使用します。

```
$browser->pause(1000);
```

<!-- If you need to pause the test only if a given condition is `true`, use the `pauseIf` method: -->
特定の条件が `true` の場合にのみテストを一時停止する必要がある場合は、`pauseIf` メソッドを使用します。

```
$browser->pauseIf(App::environment('production'), 1000);
```

<!-- Likewise, if you need to pause the test unless a given condition is `true`, you may use the `pauseUnless` method: -->
同様に、特定の条件が `true` でない限りテストを一時停止する必要がある場合は、`pauseUnless` メソッドを使用できます。

```
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
<!-- #### Waiting For Selectors -->
#### Waiting For Selectors

<!-- The `waitFor` method may be used to pause the execution of the test until the element matching the given CSS or Dusk selector is displayed on the page. By default, this will pause the test for a maximum of five seconds before throwing an exception. If necessary, you may pass a custom timeout threshold as the second argument to the method: -->
`waitFor` メソッドを使用すると、指定された CSS または Dusk セレクターに一致する要素がページに表示されるまでテストの実行を一時停止できます。デフォルトでは、例外がスローされる前にテストが最大 5 秒間一時停止されます。必要に応じて、カスタム タイムアウトしきい値を 2 番目の引数としてメソッドに渡すことができます。

```
// Wait a maximum of five seconds for the selector...
$browser->waitFor('.selector');

// Wait a maximum of one second for the selector...
$browser->waitFor('.selector', 1);
```

<!-- You may also wait until the element matching the given selector contains the given text: -->
指定されたセレクターに一致する要素に指定されたテキストが含まれるまで待つこともできます。

```
// Wait a maximum of five seconds for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World');

// Wait a maximum of one second for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

<!-- You may also wait until the element matching the given selector is missing from the page: -->
指定されたセレクターに一致する要素がページからなくなるまで待つこともできます。

```
// Wait a maximum of five seconds until the selector is missing...
$browser->waitUntilMissing('.selector');

// Wait a maximum of one second until the selector is missing...
$browser->waitUntilMissing('.selector', 1);
```

<!-- Or, you may wait until the element matching the given selector is enabled or disabled: -->
または、指定されたセレクターに一致する要素が有効または無効になるまで待つこともできます。

```
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
<!-- #### Scoping Selectors When Available -->
#### Scoping Selectors When Available

<!-- Occasionally, you may wish to wait for an element to appear that matches a given selector and then interact with the element. For example, you may wish to wait until a modal window is available and then press the "OK" button within the modal. The `whenAvailable` method may be used to accomplish this. All element operations performed within the given closure will be scoped to the original selector: -->
場合によっては、特定のセレクターに一致する要素が表示されるのを待ってから、その要素を操作したい場合があります。たとえば、モーダル ウィンドウが使用可能になるまで待ってから、モーダル内の [OK] ボタンを押すとよいでしょう。これを実現するには、`whenAvailable` メソッドを使用できます。指定されたクロージャー内で実行されるすべての要素操作は、元のセレクターにスコープされます。

```
$browser->whenAvailable('.modal', function ($modal) {
    $modal->assertSee('Hello World')
          ->press('OK');
});
```

<a name="waiting-for-text"></a>
<!-- #### Waiting For Text -->
#### Waiting For Text

<!-- The `waitForText` method may be used to wait until the given text is displayed on the page: -->
`waitForText` メソッドは、指定されたテキストがページに表示されるまで待機するために使用できます。

```
// Wait a maximum of five seconds for the text...
$browser->waitForText('Hello World');

// Wait a maximum of one second for the text...
$browser->waitForText('Hello World', 1);
```

<!-- You may use the `waitUntilMissingText` method to wait until the displayed text has been removed from the page: -->
`waitUntilMissingText` メソッドを使用して、表示されたテキストがページから削除されるまで待つことができます。

```
// Wait a maximum of five seconds for the text to be removed...
$browser->waitUntilMissingText('Hello World');

// Wait a maximum of one second for the text to be removed...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
<!-- #### Waiting For Links -->
#### Waiting For Links

<!-- The `waitForLink` method may be used to wait until the given link text is displayed on the page: -->
`waitForLink` メソッドは、指定されたリンク テキストがページに表示されるまで待機するために使用できます。

```
// Wait a maximum of five seconds for the link...
$browser->waitForLink('Create');

// Wait a maximum of one second for the link...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
<!-- #### Waiting For Inputs -->
#### Waiting For Inputs

<!-- The `waitForInput` method may be used to wait until the given input field is visible on the page: -->
`waitForInput` メソッドは、指定された入力フィールドがページに表示されるまで待機するために使用できます。

```
// Wait a maximum of five seconds for the input...
$browser->waitForInput($field);

// Wait a maximum of one second for the input...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
<!-- #### Waiting On The Page Location -->
#### Waiting On The Page Location

<!-- When making a path assertion such as `$browser->assertPathIs('/home')`, the assertion can fail if `window.location.pathname` is being updated asynchronously. You may use the `waitForLocation` method to wait for the location to be a given value: -->
`$browser->assertPathIs('/home')` などのパス アサーションを作成する場合、`window.location.pathname` が非同期的に更新されている場合、アサーションが失敗する可能性があります。 `waitForLocation` メソッドを使用して、場所が指定された値になるまで待機できます。

```
$browser->waitForLocation('/secret');
```

<!-- The `waitForLocation` method can also be used to wait for the current window location to be a fully qualified URL: -->
`waitForLocation` メソッドを使用して、現在のウィンドウの位置が完全修飾 URL になるのを待つこともできます。

```
$browser->waitForLocation('https://example.com/path');
```

<!-- You may also wait for a [named route's](/docs/9.x/routing#named-routes) location: -->
[named route's](/docs/9.x/routing#named-routes) の場所を待つこともできます。

```
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
<!-- #### Waiting For Page Reloads -->
#### Waiting For Page Reloads

<!-- If you need to wait for a page to reload after performing an action, use the `waitForReload` method: -->
アクションの実行後にページがリロードされるまで待機する必要がある場合は、`waitForReload` メソッドを使用します。

```
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

<!-- Since the need to wait for the page to reload typically occurs after clicking a button, you may use the `clickAndWaitForReload` method for convenience: -->
通常、ボタンをクリックした後にページがリロードされるまで待機する必要があるため、便宜上 `clickAndWaitForReload` メソッドを使用できます。

```
$browser->clickAndWaitForReload('.selector')
        ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
<!-- #### Waiting On JavaScript Expressions -->
#### Waiting On JavaScript Expressions

<!-- Sometimes you may wish to pause the execution of a test until a given JavaScript expression evaluates to `true`. You may easily accomplish this using the `waitUntil` method. When passing an expression to this method, you do not need to include the `return` keyword or an ending semi-colon: -->
場合によっては、特定の JavaScript 式が `true` と評価されるまで、テストの実行を一時停止したい場合があります。これは、`waitUntil` メソッドを使用して簡単に実行できます。このメソッドに式を渡す場合、`return` キーワードや末尾のセミコロンを含める必要はありません。

```
// Wait a maximum of five seconds for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0');

// Wait a maximum of one second for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
<!-- #### Waiting On Vue Expressions -->
#### Waiting On Vue Expressions

<!-- The `waitUntilVue` and `waitUntilVueIsNot` methods may be used to wait until a [Vue component](https://vuejs.org) attribute has a given value: -->
`waitUntilVue` メソッドと `waitUntilVueIsNot` メソッドは、[Vue component](https://vuejs.org) 属性が指定された値になるまで待機するために使用できます。

```
// Wait until the component attribute contains the given value...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// Wait until the component attribute doesn't contain the given value...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
<!-- #### Waiting For JavaScript Events -->
#### Waiting For JavaScript Events

<!-- The `waitForEvent` method can be used to pause the execution of a test until a JavaScript event occurs: -->
`waitForEvent` メソッドを使用すると、JavaScript イベントが発生するまでテストの実行を一時停止できます。

```
$browser->waitForEvent('load');
```

<!-- The event listener is attached to the current scope, which is the `body` element by default. When using a scoped selector, the event listener will be attached to the matching element: -->
イベント リスナは現在のスコープ (デフォルトでは `body` 要素) にアタッチされます。スコープ付きセレクターを使用する場合、イベント リスナは一致する要素にアタッチされます。

```
$browser->with('iframe', function ($iframe) {
    // Wait for the iframe's load event...
    $iframe->waitForEvent('load');
});
```

<!-- You may also provide a selector as the second argument to the `waitForEvent` method to attach the event listener to a specific element: -->
`waitForEvent` メソッドの 2 番目の引数としてセレクターを指定して、イベント リスナを特定の要素にアタッチすることもできます。

```
$browser->waitForEvent('load', '.selector');
```

<!-- You may also wait for events on the `document` and `window` objects: -->
`document` および `window` オブジェクトのイベントを待つこともできます。

```
// Wait until the document is scrolled...
$browser->waitForEvent('scroll', 'document');

// Wait a maximum of five seconds until the window is resized...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
<!-- #### Waiting With A Callback -->
#### Waiting With A Callback

<!-- Many of the "wait" methods in Dusk rely on the underlying `waitUsing` method. You may use this method directly to wait for a given closure to return `true`. The `waitUsing` method accepts the maximum number of seconds to wait, the interval at which the closure should be evaluated, the closure, and an optional failure message: -->
Dusk の「待機」メソッドの多くは、基礎となる `waitUsing` メソッドに依存しています。このメソッドを直接使用して、特定のクロージャが `true` を返すのを待つことができます。 `waitUsing` メソッドは、待機する最大秒数、クロージャを評価する間隔、クロージャ、およびオプションの失敗メッセージを受け入れます。

```
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
<!-- ### Scrolling An Element Into View -->
### Scrolling An Element Into View

<!-- Sometimes you may not be able to click on an element because it is outside of the viewable area of the browser. The `scrollIntoView` method will scroll the browser window until the element at the given selector is within the view: -->
要素がブラウザの表示領域外にあるため、要素をクリックできない場合があります。 `scrollIntoView` メソッドは、指定されたセレクターの要素がビュー内に表示されるまでブラウザ ウィンドウをスクロールします。

```
$browser->scrollIntoView('.selector')
        ->click('.selector');
```

<a name="available-assertions"></a>
<!-- ## Available Assertions -->
## Available Assertions

<!-- Dusk provides a variety of assertions that you may make against your application. All of the available assertions are documented in the list below: -->
Dusk は、アプリケーションに対して行うことができるさまざまなアサーションを提供します。利用可能なアサーションはすべて、以下のリストに記載されています。

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
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
[assertAttributeContains](#assert-attribute-contains)
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
[assertVueDoesNotContain](#assert-vue-does-not-contain)
-->
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
[assertAttributeContains](#assert-attribute-contains)
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
[assertVueDoesNotContain](#assert-vue-does-not-contain)

<!-- </div> -->
</div>

<a name="assert-title"></a>
<!-- #### assertTitle -->
#### assertTitle

<!-- Assert that the page title matches the given text: -->
ページ タイトルが指定されたテキストと一致することをアサートします。

```
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
<!-- #### assertTitleContains -->
#### assertTitleContains

<!-- Assert that the page title contains the given text: -->
ページ タイトルに指定されたテキストが含まれていることをアサートします。

```
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
<!-- #### assertUrlIs -->
#### assertUrlIs

<!-- Assert that the current URL (without the query string) matches the given string: -->
現在の URL (クエリ文字列なし) が指定された文字列と一致することをアサートします。

```
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
<!-- #### assertSchemeIs -->
#### assertSchemeIs

<!-- Assert that the current URL scheme matches the given scheme: -->
現在の URL スキームが指定されたスキームと一致することをアサートします。

```
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
<!-- #### assertSchemeIsNot -->
#### assertSchemeIsNot

<!-- Assert that the current URL scheme does not match the given scheme: -->
現在の URL スキームが指定されたスキームと一致しないことをアサートします。

```
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
<!-- #### assertHostIs -->
#### assertHostIs

<!-- Assert that the current URL host matches the given host: -->
現在の URL ホストが指定されたホストと一致することをアサートします。

```
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
<!-- #### assertHostIsNot -->
#### assertHostIsNot

<!-- Assert that the current URL host does not match the given host: -->
現在の URL ホストが指定されたホストと一致しないことをアサートします。

```
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
<!-- #### assertPortIs -->
#### assertPortIs

<!-- Assert that the current URL port matches the given port: -->
現在の URL ポートが指定されたポートと一致することをアサートします。

```
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
<!-- #### assertPortIsNot -->
#### assertPortIsNot

<!-- Assert that the current URL port does not match the given port: -->
現在の URL ポートが指定されたポートと一致しないことをアサートします。

```
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
<!-- #### assertPathBeginsWith -->
#### assertPathBeginsWith

<!-- Assert that the current URL path begins with the given path: -->
現在の URL パスが指定されたパスで始まることをアサートします。

```
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-is"></a>
<!-- #### assertPathIs -->
#### assertPathIs

<!-- Assert that the current path matches the given path: -->
現在のパスが指定されたパスと一致することをアサートします。

```
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
<!-- #### assertPathIsNot -->
#### assertPathIsNot

<!-- Assert that the current path does not match the given path: -->
現在のパスが指定されたパスと一致しないことをアサートします。

```
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
<!-- #### assertRouteIs -->
#### assertRouteIs

<!-- Assert that the current URL matches the given [named route's](/docs/9.x/routing#named-routes) URL: -->
現在の URL が指定された [named route's](/docs/9.x/routing#named-routes) URL と一致することをアサートします。

```
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
<!-- #### assertQueryStringHas -->
#### assertQueryStringHas

<!-- Assert that the given query string parameter is present: -->
指定されたクエリ文字列パラメータが存在することをアサートします。

```
$browser->assertQueryStringHas($name);
```

<!-- Assert that the given query string parameter is present and has a given value: -->
指定されたクエリ文字列パラメータが存在し、指定された値を持つことをアサートします。

```
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
<!-- #### assertQueryStringMissing -->
#### assertQueryStringMissing

<!-- Assert that the given query string parameter is missing: -->
指定されたクエリ文字列パラメータが欠落していることをアサートします。

```
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
<!-- #### assertFragmentIs -->
#### assertFragmentIs

<!-- Assert that the URL's current hash fragment matches the given fragment: -->
URL の現在のハッシュ フラグメントが指定されたフラグメントと一致することをアサートします。

```
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
<!-- #### assertFragmentBeginsWith -->
#### assertFragmentBeginsWith

<!-- Assert that the URL's current hash fragment begins with the given fragment: -->
URL の現在のハッシュ フラグメントが指定されたフラグメントで始まることをアサートします。

```
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
<!-- #### assertFragmentIsNot -->
#### assertFragmentIsNot

<!-- Assert that the URL's current hash fragment does not match the given fragment: -->
URL の現在のハッシュ フラグメントが指定されたフラグメントと一致しないことをアサートします。

```
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
<!-- #### assertHasCookie -->
#### assertHasCookie

<!-- Assert that the given encrypted cookie is present: -->
指定された暗号化された Cookie が存在することをアサートします。

```
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
<!-- #### assertHasPlainCookie -->
#### assertHasPlainCookie

<!-- Assert that the given unencrypted cookie is present: -->
指定された暗号化されていない Cookie が存在することをアサートします。

```
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
<!-- #### assertCookieMissing -->
#### assertCookieMissing

<!-- Assert that the given encrypted cookie is not present: -->
指定された暗号化された Cookie が存在しないことをアサートします。

```
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
<!-- #### assertPlainCookieMissing -->
#### assertPlainCookieMissing

<!-- Assert that the given unencrypted cookie is not present: -->
指定された暗号化されていない Cookie が存在しないことをアサートします。

```
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
<!-- #### assertCookieValue -->
#### assertCookieValue

<!-- Assert that an encrypted cookie has a given value: -->
暗号化された Cookie が指定された値を持つことをアサートします。

```
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
<!-- #### assertPlainCookieValue -->
#### assertPlainCookieValue

<!-- Assert that an unencrypted cookie has a given value: -->
暗号化されていない Cookie が指定された値を持つことをアサートします。

```
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
<!-- #### assertSee -->
#### assertSee

<!-- Assert that the given text is present on the page: -->
指定されたテキストがページ上に存在することをアサートします。

```
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
<!-- #### assertDontSee -->
#### assertDontSee

<!-- Assert that the given text is not present on the page: -->
指定されたテキストがページ上に存在しないことをアサートします。

```
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
<!-- #### assertSeeIn -->
#### assertSeeIn

<!-- Assert that the given text is present within the selector: -->
指定されたテキストがセレクター内に存在することをアサートします。

```
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
<!-- #### assertDontSeeIn -->
#### assertDontSeeIn

<!-- Assert that the given text is not present within the selector: -->
指定されたテキストがセレクター内に存在しないことをアサートします。

```
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
<!-- #### assertSeeAnythingIn -->
#### assertSeeAnythingIn

<!-- Assert that any text is present within the selector: -->
セレクター内にテキストが存在することをアサートします。

```
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
<!-- #### assertSeeNothingIn -->
#### assertSeeNothingIn

<!-- Assert that no text is present within the selector: -->
セレクター内にテキストが存在しないことをアサートします。

```
$browser->assertSeeNothingIn($selector);
```

<a name="assert-script"></a>
<!-- #### assertScript -->
#### assertScript

<!-- Assert that the given JavaScript expression evaluates to the given value: -->
指定された JavaScript 式が指定された値に評価されることをアサートします。

```
$browser->assertScript('window.isLoaded')
        ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
<!-- #### assertSourceHas -->
#### assertSourceHas

<!-- Assert that the given source code is present on the page: -->
指定されたソース コードがページ上に存在することをアサートします。

```
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
<!-- #### assertSourceMissing -->
#### assertSourceMissing

<!-- Assert that the given source code is not present on the page: -->
指定されたソース コードがページ上に存在しないことをアサートします。

```
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
<!-- #### assertSeeLink -->
#### assertSeeLink

<!-- Assert that the given link is present on the page: -->
指定されたリンクがページ上に存在することをアサートします。

```
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
<!-- #### assertDontSeeLink -->
#### assertDontSeeLink

<!-- Assert that the given link is not present on the page: -->
指定されたリンクがページ上に存在しないことをアサートします。

```
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
<!-- #### assertInputValue -->
#### assertInputValue

<!-- Assert that the given input field has the given value: -->
指定された入力フィールドに指定された値があることをアサートします。

```
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
<!-- #### assertInputValueIsNot -->
#### assertInputValueIsNot

<!-- Assert that the given input field does not have the given value: -->
指定された入力フィールドに指定された値が存在しないことをアサートします。

```
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
<!-- #### assertChecked -->
#### assertChecked

<!-- Assert that the given checkbox is checked: -->
指定されたチェックボックスがチェックされていることをアサートします。

```
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
<!-- #### assertNotChecked -->
#### assertNotChecked

<!-- Assert that the given checkbox is not checked: -->
指定されたチェックボックスがチェックされていないことをアサートします。

```
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
<!-- #### assertIndeterminate -->
#### assertIndeterminate

<!-- Assert that the given checkbox is in an indeterminate state: -->
指定されたチェックボックスが不定状態であることをアサートします。

```
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
<!-- #### assertRadioSelected -->
#### assertRadioSelected

<!-- Assert that the given radio field is selected: -->
指定された無線フィールドが選択されていることをアサートします。

```
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
<!-- #### assertRadioNotSelected -->
#### assertRadioNotSelected

<!-- Assert that the given radio field is not selected: -->
指定された無線フィールドが選択されていないことをアサートします。

```
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
<!-- #### assertSelected -->
#### assertSelected

<!-- Assert that the given dropdown has the given value selected: -->
指定されたドロップダウンで指定された値が選択されていることをアサートします。

```
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
<!-- #### assertNotSelected -->
#### assertNotSelected

<!-- Assert that the given dropdown does not have the given value selected: -->
指定されたドロップダウンに指定された値が選択されていないことをアサートします。

```
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
<!-- #### assertSelectHasOptions -->
#### assertSelectHasOptions

<!-- Assert that the given array of values are available to be selected: -->
指定された値の配列が選択可能であることをアサートします。

```
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
<!-- #### assertSelectMissingOptions -->
#### assertSelectMissingOptions

<!-- Assert that the given array of values are not available to be selected: -->
指定された値の配列が選択できないことをアサートします。

```
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
<!-- #### assertSelectHasOption -->
#### assertSelectHasOption

<!-- Assert that the given value is available to be selected on the given field: -->
指定された値が指定されたフィールドで選択できることをアサートします。

```
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
<!-- #### assertSelectMissingOption -->
#### assertSelectMissingOption

<!-- Assert that the given value is not available to be selected: -->
指定された値が選択できないことをアサートします。

```
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
<!-- #### assertValue -->
#### assertValue

<!-- Assert that the element matching the given selector has the given value: -->
指定されたセレクターに一致する要素が指定された値を持つことをアサートします。

```
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
<!-- #### assertValueIsNot -->
#### assertValueIsNot

<!-- Assert that the element matching the given selector does not have the given value: -->
指定されたセレクターに一致する要素が指定された値を持たないことをアサートします。

```
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
<!-- #### assertAttribute -->
#### assertAttribute

<!-- Assert that the element matching the given selector has the given value in the provided attribute: -->
指定されたセレクターに一致する要素が、指定された属性に指定された値を持つことをアサートします。

```
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-contains"></a>
<!-- #### assertAttributeContains -->
#### assertAttributeContains

<!-- Assert that the element matching the given selector contains the given value in the provided attribute: -->
指定されたセレクターに一致する要素に、指定された属性に指定された値が含まれていることをアサートします。

```
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
<!-- #### assertAriaAttribute -->
#### assertAriaAttribute

<!-- Assert that the element matching the given selector has the given value in the provided aria attribute: -->
指定されたセレクターに一致する要素が、指定された aria 属性に指定された値を持つことをアサートします。

```
$browser->assertAriaAttribute($selector, $attribute, $value);
```

<!-- For example, given the markup `<button aria-label="Add"></button>`, you may assert against the `aria-label` attribute like so: -->
たとえば、マークアップ `<button aria-label="Add"></button>` がある場合、次のように `aria-label` 属性に対してアサートできます。

```
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
<!-- #### assertDataAttribute -->
#### assertDataAttribute

<!-- Assert that the element matching the given selector has the given value in the provided data attribute: -->
指定されたセレクターに一致する要素が、指定されたデータ属性に指定された値を持つことをアサートします。

```
$browser->assertDataAttribute($selector, $attribute, $value);
```

<!-- For example, given the markup `<tr id="row-1" data-content="attendees"></tr>`, you may assert against the `data-label` attribute like so: -->
たとえば、マークアップ `<tr id="row-1" data-content="attendees"></tr>` がある場合、次のように `data-label` 属性に対してアサートできます。

```
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
<!-- #### assertVisible -->
#### assertVisible

<!-- Assert that the element matching the given selector is visible: -->
指定されたセレクターに一致する要素が表示されていることをアサートします。

```
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
<!-- #### assertPresent -->
#### assertPresent

<!-- Assert that the element matching the given selector is present in the source: -->
指定されたセレクターに一致する要素がソース内に存在することをアサートします。

```
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
<!-- #### assertNotPresent -->
#### assertNotPresent

<!-- Assert that the element matching the given selector is not present in the source: -->
指定されたセレクターに一致する要素がソースに存在しないことをアサートします。

```
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
<!-- #### assertMissing -->
#### assertMissing

<!-- Assert that the element matching the given selector is not visible: -->
指定されたセレクターに一致する要素が表示されていないことをアサートします。

```
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
<!-- #### assertInputPresent -->
#### assertInputPresent

<!-- Assert that an input with the given name is present: -->
指定された名前の入力が存在することをアサートします。

```
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
<!-- #### assertInputMissing -->
#### assertInputMissing

<!-- Assert that an input with the given name is not present in the source: -->
指定された名前の入力がソースに存在しないことをアサートします。

```
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
<!-- #### assertDialogOpened -->
#### assertDialogOpened

<!-- Assert that a JavaScript dialog with the given message has been opened: -->
指定されたメッセージを含む JavaScript ダイアログが開いたことをアサートします。

```
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
<!-- #### assertEnabled -->
#### assertEnabled

<!-- Assert that the given field is enabled: -->
指定されたフィールドが有効であることをアサートします。

```
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
<!-- #### assertDisabled -->
#### assertDisabled

<!-- Assert that the given field is disabled: -->
指定されたフィールドが無効であることをアサートします。

```
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
<!-- #### assertButtonEnabled -->
#### assertButtonEnabled

<!-- Assert that the given button is enabled: -->
指定されたボタンが有効であることをアサートします。

```
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
<!-- #### assertButtonDisabled -->
#### assertButtonDisabled

<!-- Assert that the given button is disabled: -->
指定されたボタンが無効になっていることをアサートします。

```
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
<!-- #### assertFocused -->
#### assertFocused

<!-- Assert that the given field is focused: -->
指定されたフィールドがフォーカスされていることをアサートします。

```
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
<!-- #### assertNotFocused -->
#### assertNotFocused

<!-- Assert that the given field is not focused: -->
指定されたフィールドがフォーカスされていないことをアサートします。

```
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
<!-- #### assertAuthenticated -->
#### assertAuthenticated

<!-- Assert that the user is authenticated: -->
ユーザーが認証されていることをアサートします。

```
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
<!-- #### assertGuest -->
#### assertGuest

<!-- Assert that the user is not authenticated: -->
ユーザーが認証されていないことをアサートします。

```
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
<!-- #### assertAuthenticatedAs -->
#### assertAuthenticatedAs

<!-- Assert that the user is authenticated as the given user: -->
ユーザーが指定されたユーザーとして認証されていることをアサートします。

```
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
<!-- #### assertVue -->
#### assertVue

<!-- Dusk even allows you to make assertions on the state of [Vue component](https://vuejs.org) data. For example, imagine your application contains the following Vue component: -->
Dusk では、[Vue component](https://vuejs.org) データの状態についてアサーションを行うこともできます。たとえば、アプリケーションに次の Vue コンポーネントが含まれていると想像してください。

```
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
```

<!-- You may assert on the state of the Vue component like so: -->
次のように Vue コンポーネントの状態をアサートできます。

```
/**
 * A basic Vue test example.
 *
 * @return void
 */
public function testVue()
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/')
                ->assertVue('user.name', 'Taylor', '@profile-component');
    });
}
```

<a name="assert-vue-is-not"></a>
<!-- #### assertVueIsNot -->
#### assertVueIsNot

<!-- Assert that a given Vue component data property does not match the given value: -->
指定された Vue コンポーネント データ プロパティが指定された値と一致しないことをアサートします。

```
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
<!-- #### assertVueContains -->
#### assertVueContains

<!-- Assert that a given Vue component data property is an array and contains the given value: -->
指定された Vue コンポーネント データ プロパティが配列であり、指定された値が含まれていることをアサートします。

```
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-does-not-contain"></a>
<!-- #### assertVueDoesNotContain -->
#### assertVueDoesNotContain

<!-- Assert that a given Vue component data property is an array and does not contain the given value: -->
指定された Vue コンポーネント データ プロパティが配列であり、指定された値が含まれていないことをアサートします。

```
$browser->assertVueDoesNotContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
<!-- ## Pages -->
## Pages

<!-- Sometimes, tests require several complicated actions to be performed in sequence. This can make your tests harder to read and understand. Dusk Pages allow you to define expressive actions that may then be performed on a given page via a single method. Pages also allow you to define short-cuts to common selectors for your application or for a single page. -->
場合によっては、テストではいくつかの複雑なアクションを順番に実行する必要があります。これにより、テストが読みにくくなり、理解しにくくなる可能性があります。 Dusk Pages を使用すると、単一のメソッドを介して特定のページで実行できる表現アクションを定義できます。ページを使用すると、アプリケーションまたは単一ページの共通セレクターへのショートカットを定義することもできます。

<a name="generating-pages"></a>
<!-- ### Generating Pages -->
### Generating Pages

<!-- To generate a page object, execute the `dusk:page` Artisan command. All page objects will be placed in your application's `tests/Browser/Pages` directory: -->
ページ オブジェクトを生成するには、`dusk:page` Artisan コマンドを実行します。すべてのページ オブジェクトは、アプリケーションの `tests/Browser/Pages` ディレクトリに配置されます。

```
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
<!-- ### Configuring Pages -->
### Configuring Pages

<!-- By default, pages have three methods: `url`, `assert`, and `elements`. We will discuss the `url` and `assert` methods now. The `elements` method will be [discussed in more detail below](#shorthand-selectors). -->
デフォルトでは、ページには `url`、`assert`、および `elements` の 3 つのメソッドがあります。ここでは、`url` メソッドと `assert` メソッドについて説明します。 `elements` メソッドは [discussed in more detail below](#shorthand-selectors) になります。

<a name="the-url-method"></a>
<!-- #### The `url` Method -->
#### The `url` Method

<!-- The `url` method should return the path of the URL that represents the page. Dusk will use this URL when navigating to the page in the browser: -->
`url` メソッドは、ページを表す URL のパスを返す必要があります。 Dusk はブラウザでページに移動するときにこの URL を使用します。

```
/**
 * Get the URL for the page.
 *
 * @return string
 */
public function url()
{
    return '/login';
}
```

<a name="the-assert-method"></a>
<!-- #### The `assert` Method -->
#### The `assert` Method

<!-- The `assert` method may make any assertions necessary to verify that the browser is actually on the given page. It is not actually necessary to place anything within this method; however, you are free to make these assertions if you wish. These assertions will be run automatically when navigating to the page: -->
`assert` メソッドは、ブラウザーが実際に指定されたページに存在することを確認するために必要なアサーションを行うことができます。実際には、このメソッド内に何も配置する必要はありません。ただし、必要に応じてこれらの主張を自由に行うことができます。これらのアサーションは、ページに移動すると自動的に実行されます。

```
/**
 * Assert that the browser is on the page.
 *
 * @return void
 */
public function assert(Browser $browser)
{
    $browser->assertPathIs($this->url());
}
```

<a name="navigating-to-pages"></a>
<!-- ### Navigating To Pages -->
### Navigating To Pages

<!-- Once a page has been defined, you may navigate to it using the `visit` method: -->
ページが定義されたら、`visit` メソッドを使用してそのページに移動できます。

```
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

<!-- Sometimes you may already be on a given page and need to "load" the page's selectors and methods into the current test context. This is common when pressing a button and being redirected to a given page without explicitly navigating to it. In this situation, you may use the `on` method to load the page: -->
場合によっては、すでに特定のページにいて、そのページのセレクターとメソッドを現在のテスト コンテキストに「ロード」する必要がある場合があります。これは、ボタンを押すと、明示的に移動せずに特定のページにリダイレクトされる場合によく発生します。この状況では、`on` メソッドを使用してページをロードできます。

```
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
        ->clickLink('Create Playlist')
        ->on(new CreatePlaylist)
        ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
<!-- ### Shorthand Selectors -->
### Shorthand Selectors

<!-- The `elements` method within page classes allows you to define quick, easy-to-remember shortcuts for any CSS selector on your page. For example, let's define a shortcut for the "email" input field of the application's login page: -->
ページ クラス内の `elements` メソッドを使用すると、ページ上の CSS セレクターにすばやく覚えやすいショートカットを定義できます。たとえば、アプリケーションのログイン ページの「電子メール」入力フィールドのショートカットを定義してみましょう。

```
/**
 * Get the element shortcuts for the page.
 *
 * @return array
 */
public function elements()
{
    return [
        '@email' => 'input[name=email]',
    ];
}
```

<!-- Once the shortcut has been defined, you may use the shorthand selector anywhere you would typically use a full CSS selector: -->
ショートカットが定義されたら、通常は完全な CSS セレクターを使用する場所であればどこでも短縮セレクターを使用できます。

```
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
<!-- #### Global Shorthand Selectors -->
#### Global Shorthand Selectors

<!-- After installing Dusk, a base `Page` class will be placed in your `tests/Browser/Pages` directory. This class contains a `siteElements` method which may be used to define global shorthand selectors that should be available on every page throughout your application: -->
Dusk をインストールすると、基本 `Page` クラスが `tests/Browser/Pages` ディレクトリに配置されます。このクラスには、アプリケーション全体のすべてのページで使用できるグローバル短縮セレクターを定義するために使用できる `siteElements` メソッドが含まれています。

```
/**
 * Get the global element shortcuts for the site.
 *
 * @return array
 */
public static function siteElements()
{
    return [
        '@element' => '#selector',
    ];
}
```

<a name="page-methods"></a>
<!-- ### Page Methods -->
### Page Methods

<!-- In addition to the default methods defined on pages, you may define additional methods which may be used throughout your tests. For example, let's imagine we are building a music management application. A common action for one page of the application might be to create a playlist. Instead of re-writing the logic to create a playlist in each test, you may define a `createPlaylist` method on a page class: -->
ページで定義されているデフォルトのメソッドに加えて、テスト全体で使用できる追加のメソッドを定義できます。たとえば、音楽管理アプリケーションを構築していると想像してみましょう。アプリケーションの 1 ページに対する一般的なアクションは、プレイリストの作成です。各テストでプレイリストを作成するロジックを書き直す代わりに、ページ クラスで `createPlaylist` メソッドを定義できます。

```
<?php

namespace Tests\Browser\Pages;

use Laravel\Dusk\Browser;

class Dashboard extends Page
{
    // Other page methods...

    /**
     * Create a new playlist.
     *
     * @param  \Laravel\Dusk\Browser  $browser
     * @param  string  $name
     * @return void
     */
    public function createPlaylist(Browser $browser, $name)
    {
        $browser->type('name', $name)
                ->check('share')
                ->press('Create Playlist');
    }
}
```

<!-- Once the method has been defined, you may use it within any test that utilizes the page. The browser instance will automatically be passed as the first argument to custom page methods: -->
メソッドを定義したら、そのページを利用するテスト内でそのメソッドを使用できます。ブラウザー インスタンスは、カスタム ページ メソッドの最初の引数として自動的に渡されます。

```
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
        ->createPlaylist('My Playlist')
        ->assertSee('My Playlist');
```

<a name="components"></a>
<!-- ## Components -->
## Components

<!-- Components are similar to Dusk’s “page objects”, but are intended for pieces of UI and functionality that are re-used throughout your application, such as a navigation bar or notification window. As such, components are not bound to specific URLs. -->
コンポーネントは Dusk の「ページ オブジェクト」に似ていますが、ナビゲーション バーや通知ウィンドウなど、アプリケーション全体で再利用される UI や機能の一部を対象としています。そのため、コンポーネントは特定の URL にバインドされません。

<a name="generating-components"></a>
<!-- ### Generating Components -->
### Generating Components

<!-- To generate a component, execute the `dusk:component` Artisan command. New components are placed in the `tests/Browser/Components` directory: -->
コンポーネントを生成するには、`dusk:component` Artisan コマンドを実行します。新しいコンポーネントは `tests/Browser/Components` ディレクトリに配置されます。

```
php artisan dusk:component DatePicker
```

<!-- As shown above, a "date picker" is an example of a component that might exist throughout your application on a variety of pages. It can become cumbersome to manually write the browser automation logic to select a date in dozens of tests throughout your test suite. Instead, we can define a Dusk component to represent the date picker, allowing us to encapsulate that logic within the component: -->
上に示したように、「日付ピッカー」は、アプリケーション全体のさまざまなページに存在する可能性があるコンポーネントの例です。テスト スイート全体の数十のテストで日付を選択するためにブラウザ自動化ロジックを手動で記述するのは面倒になる場合があります。代わりに、日付ピッカーを表す Dusk コンポーネントを定義して、そのロジックをコンポーネント内にカプセル化できます。

```
<?php

namespace Tests\Browser\Components;

use Laravel\Dusk\Browser;
use Laravel\Dusk\Component as BaseComponent;

class DatePicker extends BaseComponent
{
    /**
     * Get the root selector for the component.
     *
     * @return string
     */
    public function selector()
    {
        return '.date-picker';
    }

    /**
     * Assert that the browser page contains the component.
     *
     * @param  Browser  $browser
     * @return void
     */
    public function assert(Browser $browser)
    {
        $browser->assertVisible($this->selector());
    }

    /**
     * Get the element shortcuts for the component.
     *
     * @return array
     */
    public function elements()
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
     *
     * @param  \Laravel\Dusk\Browser  $browser
     * @param  int  $year
     * @param  int  $month
     * @param  int  $day
     * @return void
     */
    public function selectDate(Browser $browser, $year, $month, $day)
    {
        $browser->click('@date-field')
                ->within('@year-list', function ($browser) use ($year) {
                    $browser->click($year);
                })
                ->within('@month-list', function ($browser) use ($month) {
                    $browser->click($month);
                })
                ->within('@day-list', function ($browser) use ($day) {
                    $browser->click($day);
                });
    }
}
```

<a name="using-components"></a>
<!-- ### Using Components -->
### Using Components

<!-- Once the component has been defined, we can easily select a date within the date picker from any test. And, if the logic necessary to select a date changes, we only need to update the component: -->
コンポーネントが定義されたら、任意のテストから日付ピッカー内の日付を簡単に選択できます。また、日付の選択に必要なロジックが変更された場合は、コンポーネントを更新するだけで済みます。

```
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
     *
     * @return void
     */
    public function testBasicExample()
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/')
                    ->within(new DatePicker, function ($browser) {
                        $browser->selectDate(2019, 1, 30);
                    })
                    ->assertSee('January');
        });
    }
}
```

<a name="continuous-integration"></a>
<!-- ## Continuous Integration -->
## Continuous Integration

> [!WARNING]
> ほとんどの Dusk 継続的統合構成では、Laravel アプリケーションがポート 8000 の組み込み PHP 開発サーバーを使用して提供されることを想定しています。 したがって、続行する前に、継続的統合環境の `APP_URL` 環境変数値が `http://127.0.0.1:8000` であることを確認する必要があります。

<a name="running-tests-on-heroku-ci"></a>
<!-- ### Heroku CI -->
### Heroku CI

<!-- To run Dusk tests on [Heroku CI](https://www.heroku.com/continuous-integration), add the following Google Chrome buildpack and scripts to your Heroku `app.json` file: -->
[Heroku CI](https://www.heroku.com/continuous-integration) で Dusk テストを実行するには、次の Google Chrome ビルドパックとスクリプトを Heroku `app.json` ファイルに追加します。

```
{
  "environments": {
    "test": {
      "buildpacks": [
        { "url": "heroku/php" },
        { "url": "https://github.com/heroku/heroku-buildpack-google-chrome" }
      ],
      "scripts": {
        "test-setup": "cp .env.testing .env",
        "test": "nohup bash -c './vendor/laravel/dusk/bin/chromedriver-linux > /dev/null 2>&1 &' && nohup bash -c 'php artisan serve --no-reload > /dev/null 2>&1 &' && php artisan dusk"
      }
    }
  }
}
```

<a name="running-tests-on-travis-ci"></a>
<!-- ### Travis CI -->
### Travis CI

<!-- To run your Dusk tests on [Travis CI](https://travis-ci.org), use the following `.travis.yml` configuration. Since Travis CI is not a graphical environment, we will need to take some extra steps in order to launch a Chrome browser. In addition, we will use `php artisan serve` to launch PHP's built-in web server: -->
[Travis CI](https://travis-ci.org) で Dusk テストを実行するには、次の `.travis.yml` 構成を使用します。 Travis CI はグラフィカル環境ではないため、Chrome ブラウザを起動するには追加の手順を実行する必要があります。さらに、`php artisan serve` を使用して、PHP の組み込み Web サーバーを起動します。

```yaml
language: php

php:
  - 7.3

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
<!-- ### GitHub Actions -->
### GitHub Actions

<!-- If you are using [GitHub Actions](https://github.com/features/actions) to run your Dusk tests, you may use the following configuration file as a starting point. Like TravisCI, we will use the `php artisan serve` command to launch PHP's built-in web server: -->
[GitHub Actions](https://github.com/features/actions) を使用して Dusk テストを実行している場合は、開始点として次の構成ファイルを使用できます。 TravisCI と同様に、`php artisan serve` コマンドを使用して、PHP の組み込み Web サーバーを起動します。

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
      - uses: actions/checkout@v3
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
        run: ./vendor/laravel/dusk/bin/chromedriver-linux &
      - name: Run Laravel Server
        run: php artisan serve --no-reload &
      - name: Run Dusk Tests
        run: php artisan dusk
      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: screenshots
          path: tests/Browser/screenshots
      - name: Upload Console Logs
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: console
          path: tests/Browser/console
```

