# Laravel Dusk (Laravel Dusk)

- [Introduction](#introduction)
- [Installation](#installation)
    - [ChromeDriver インストールの管理](#managing-chromedriver-installations)
    - [他のブラウザの使用](#using-other-browsers)
- [はじめる](#getting-started)
    - [テストの生成](#generating-tests)
    - [各テスト後のデータベースのリセット](#resetting-the-database-after-each-test)
    - [テストの実行](#running-tests)
    - [環境への対応](#environment-handling)
- [ブラウザの基本](#browser-basics)
    - [ブラウザの作成](#creating-browsers)
    - [Navigation](#navigation)
    - [ブラウザウィンドウのサイズ変更](#resizing-browser-windows)
    - [ブラウザマクロ](#browser-macros)
    - [Authentication](#authentication)
    - [Cookies](#cookies)
    - [JavaScriptの実行](#executing-javascript)
    - [スクリーンショットを撮る](#taking-a-screenshot)
    - [コンソール出力をディスクに保存する](#storing-console-output-to-disk)
    - [ページソースをディスクに保存する](#storing-page-source-to-disk)
- [要素との対話](#interacting-with-elements)
    - [Dusk セレクタ](#dusk-selectors)
    - [テキスト、値、および属性](#text-values-and-attributes)
    - [フォームの操作](#interacting-with-forms)
    - [ファイルの添付](#attaching-files)
    - [ボタンを押す](#pressing-buttons)
    - [リンクをクリックする](#clicking-links)
    - [キーボードの使用](#using-the-keyboard)
    - [マウスの使用](#using-the-mouse)
    - [JavaScript ダイアログ](#javascript-dialogs)
    - [インラインフレームの操作](#interacting-with-iframes)
    - [スコープセレクター](#scoping-selectors)
    - [要素を待っています](#waiting-for-elements)
    - [要素をスクロールして表示する](#scrolling-an-element-into-view)
- [利用可能なアサーション](#available-assertions)
- [Pages](#pages)
    - [ページの生成](#generating-pages)
    - [ページの構成](#configuring-pages)
    - [ページへの移動](#navigating-to-pages)
    - [短縮表記セレクター](#shorthand-selectors)
    - [ページメソッド](#page-methods)
- [Components](#components)
    - [コンポーネントの生成](#generating-components)
    - [コンポーネントの使用](#using-components)
- [継続的インテグレーション](#continuous-integration)
    - [Heroku CI](#running-tests-on-heroku-ci)
    - [トラヴィスCI](#running-tests-on-travis-ci)
    - [GitHub アクション](#running-tests-on-github-actions)
    - [チッパーCI](#running-tests-on-chipper-ci)

<a name="introduction"></a>
## 導入 (Introduction)

> [!WARNING]
> [害虫4](https://pestphp.com/) には自動ブラウザテストが含まれるようになり、Laravel Dusk と比較してパフォーマンスと使いやすさが大幅に向上しました。新しいプロジェクトの場合は、ブラウザーのテストに Pest を使用することをお勧めします。

[Laravel Dusk](https://github.com/laravel/dusk) は、表現力豊かで使いやすいブラウザ自動化およびテスト API を提供します。デフォルトでは、Dusk ではローカル コンピューターに JDK または Selenium をインストールする必要はありません。代わりに、Dusk はスタンドアロン [ChromeDriver](https://sites.google.com/chromium.org/driver) インストールを使用します。ただし、他の Selenium 互換ドライバを自由に利用できます。

<a name="installation"></a>
## インストール (Installation)

まず、[Google Chrome](https://www.google.com/chrome) をインストールし、`laravel/dusk` Composer 依存関係をプロジェクトに追加する必要があります。

```shell
composer require laravel/dusk --dev
```

> [!WARNING]
> Dusk のサービスプロバイダを手動で登録する場合は、運用環境では決して登録しないでください。登録すると、任意のユーザーがアプリケーションで認証できる可能性があります。

Dusk パッケージをインストールした後、`dusk:install` Artisan コマンドを実行します。 `dusk:install` コマンドは、Dusk テストのサンプルである `tests/Browser` ディレクトリを作成し、オペレーティング システム用の Chrome ドライバ バイナリをインストールします。

```shell
php artisan dusk:install
```

次に、アプリケーションの `.env` ファイルに `APP_URL` 環境変数を設定します。この値は、ブラウザでアプリケーションにアクセスするために使用する URL と一致する必要があります。

> [!NOTE]
> [Laravel Sail](/docs/{{version}}/sail) を使用してローカル開発環境を管理している場合は、[Dusk テストの構成と実行](/docs/{{version}}/sail#laravel-dusk) の Sail ドキュメントも参照してください。

<a name="managing-chromedriver-installations"></a>
### ChromeDriver インストールの管理

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
### 他のブラウザの使用

デフォルトでは、Dusk は Google Chrome とスタンドアロン [ChromeDriver](https://sites.google.com/chromium.org/driver) インストールを使用してブラウザ テストを実行します。ただし、独自の Selenium サーバーを起動し、任意のブラウザに対してテストを実行することもできます。

まず、アプリケーションのベース Dusk テスト ケースである `tests/DuskTestCase.php` ファイルを開きます。このファイル内で、`startChromeDriver` メソッドの呼び出しを削除できます。これにより、Dusk が ChromeDriver を自動的に起動しなくなります。

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

次に、選択した URL とポートに接続するように `driver` メソッドを変更できます。さらに、WebDriver に渡す必要がある「必要な機能」を変更することもできます。

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
## はじめる (Getting Started)

<a name="generating-tests"></a>
### テストの生成

Dusk テストを生成するには、`dusk:make` Artisan コマンドを使用します。生成されたテストは、`tests/Browser` ディレクトリに配置されます。

```shell
php artisan dusk:make LoginTest
```

<a name="resetting-the-database-after-each-test"></a>
### 各テスト後のデータベースのリセット

作成するテストのほとんどは、アプリケーションのデータベースからデータを取得するページと対話します。ただし、Dusk テストでは `RefreshDatabase` 特性を使用しないでください。 `RefreshDatabase` トレイトは、HTTP リクエスト全体では適用できない、または使用できないデータベース トランザクションを利用します。代わりに、`DatabaseMigrations` トレイトと `DatabaseTruncation` トレイトの 2 つのオプションがあります。

<a name="reset-migrations"></a>
#### データベース移行の使用

`DatabaseMigrations` トレイトは、各テストの前にデータベースの移行を実行します。ただし、テストごとにデータベース テーブルを削除して再作成するのは、通常、テーブルを切り捨てるよりも時間がかかります。

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
> Dusk テストの実行時には SQLite インメモリ データベースを使用できない場合があります。ブラウザは独自のプロセス内で実行されるため、他のプロセスのメモリ内データベースにアクセスすることはできません。

<a name="reset-truncation"></a>
#### データベースのトランケーションの使用

`DatabaseTruncation` トレイトは、データベース テーブルが適切に作成されたことを確認するために、最初のテストでデータベースを移行します。ただし、後続のテストではデータベースのテーブルが単純に切り捨てられるため、すべてのデータベース移行を再実行するよりも速度が向上します。

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

デフォルトでは、この特性は `migrations` テーブルを除くすべてのテーブルを切り捨てます。切り詰めるテーブルをカスタマイズしたい場合は、テスト クラスで `$tablesToTruncate` プロパティを定義できます。

> [!NOTE]
> Pest を使用している場合は、基本 `DuskTestCase` クラス、またはテスト ファイルが拡張するクラスでプロパティまたはメソッドを定義する必要があります。

```php
/**
 * Indicates which tables should be truncated.
 *
 * @var array
 */
protected $tablesToTruncate = ['users'];
```

あるいは、テスト クラスで `$exceptTables` プロパティを定義して、切り捨てから除外するテーブルを指定することもできます。

```php
/**
 * Indicates which tables should be excluded from truncation.
 *
 * @var array
 */
protected $exceptTables = ['users'];
```

テーブルを切り詰める必要があるデータベース接続を指定するには、テスト クラスで `$connectionsToTruncate` プロパティを定義できます。

```php
/**
 * Indicates which connections should have their tables truncated.
 *
 * @var array
 */
protected $connectionsToTruncate = ['mysql'];
```

データベースの切り捨てが実行される前または後にコードを実行したい場合は、テスト クラスで `beforeTruncatingDatabase` メソッドまたは `afterTruncatingDatabase` メソッドを定義できます。

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
### テストの実行

ブラウザーのテストを実行するには、`dusk` Artisan コマンドを実行します。

```shell
php artisan dusk
```

前回 `dusk` コマンドを実行したときにテストが失敗した場合は、最初に `dusk:fails` コマンドを使用して、失敗したテストを再実行することで時間を節約できます。

```shell
php artisan dusk:fails
```

`dusk` コマンドは、特定の [group](https://docs.phpunit.de/en/10.5/annotations.html#group) のテストのみを実行できるようにするなど、Pest / PHPUnit テスト ランナーによって通常受け入れられる引数を受け入れます。

```shell
php artisan dusk --group=foo
```

> [!NOTE]
> [Laravel Sail](/docs/{{version}}/sail) を使用してローカル開発環境を管理している場合は、[Dusk テストの構成と実行](/docs/{{version}}/sail#laravel-dusk) の Sail ドキュメントを参照してください。

<a name="manually-starting-chromedriver"></a>
#### ChromeDriver を手動で起動する

デフォルトでは、Dusk は自動的に ChromeDriver の起動を試みます。これが特定のシステムで機能しない場合は、`dusk` コマンドを実行する前に ChromeDriver を手動で起動できます。 ChromeDriver を手動で開始することを選択した場合は、`tests/DuskTestCase.php` ファイルの次の行をコメント アウトする必要があります。

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

さらに、9515 以外のポートで ChromeDriver を起動する場合は、同じクラスの `driver` メソッドを変更して、正しいポートを反映する必要があります。

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
### 環境への対応

テストの実行時に Dusk に独自の環境ファイルを使用させるには、プロジェクトのルートに `.env.dusk.{environment}` ファイルを作成します。たとえば、`local` 環境から `dusk` コマンドを開始する場合は、`.env.dusk.local` ファイルを作成する必要があります。

テストを実行するとき、Dusk は `.env` ファイルをバックアップし、Dusk 環境の名前を `.env` に変更します。テストが完了すると、`.env` ファイルが復元されます。

<a name="browser-basics"></a>
## ブラウザの基本 (Browser Basics)

<a name="creating-browsers"></a>
### ブラウザの作成

まず、アプリケーションにログインできることを確認するテストを作成しましょう。テストを生成した後、ログイン ページに移動し、資格情報を入力して、[ログイン] ボタンをクリックするようにテストを変更できます。ブラウザー インスタンスを作成するには、Dusk テスト内から `browse` メソッドを呼び出すことができます。

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

上の例でわかるように、`browse` メソッドはクロージャを受け入れます。ブラウザ インスタンスは、Dusk によって自動的にこのクロージャに渡され、アプリケーションと対話したり、アプリケーションに対してアサーションを行ったりするために使用される主要なオブジェクトです。

<a name="creating-multiple-browsers"></a>
#### 複数のブラウザの作成

テストを適切に実行するために複数のブラウザが必要になる場合があります。たとえば、WebSocket と対話するチャット画面をテストするには、複数のブラウザーが必要になる場合があります。複数のブラウザを作成するには、`browse` メソッドに指定されたクロージャのシグネチャにブラウザ引数を追加するだけです。

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
### ナビゲーション

`visit` メソッドは、アプリケーション内の特定の URI に移動するために使用できます。

```php
$browser->visit('/login');
```

`visitRoute` メソッドを使用して、[名前付きルート](/docs/{{version}}/routing#named-routes) に移動できます。

```php
$browser->visitRoute($routeName, $parameters);
```

`back` メソッドと `forward` メソッドを使用して、「戻る」と「進む」に移動できます。

```php
$browser->back();

$browser->forward();
```

`refresh` メソッドを使用してページを更新できます。

```php
$browser->refresh();
```

<a name="resizing-browser-windows"></a>
### ブラウザウィンドウのサイズ変更

`resize` メソッドを使用して、ブラウザ ウィンドウのサイズを調整できます。

```php
$browser->resize(1920, 1080);
```

`maximize` メソッドは、ブラウザ ウィンドウを最大化するために使用できます。

```php
$browser->maximize();
```

`fitContent` メソッドは、コンテンツのサイズに合わせてブラウザ ウィンドウのサイズを変更します。

```php
$browser->fitContent();
```

テストが失敗すると、Dusk はスクリーンショットを撮る前に、コンテンツに合わせてブラウザのサイズを自動的に変更します。テスト内で `disableFitOnFailure` メソッドを呼び出すことで、この機能を無効にすることができます。

```php
$browser->disableFitOnFailure();
```

`move` メソッドを使用して、ブラウザ ウィンドウを画面上の別の位置に移動できます。

```php
$browser->move($x = 100, $y = 100);
```

<a name="browser-macros"></a>
### ブラウザマクロ

さまざまなテストで再利用できるカスタム ブラウザ メソッドを定義したい場合は、`Browser` クラスの `macro` メソッドを使用できます。通常、このメソッドは [サービスプロバイダの](/docs/{{version}}/providers) `boot` メソッドから呼び出す必要があります。

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

`macro` 関数は、最初の引数として名前を受け入れ、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャは、`Browser` インスタンスのメソッドとしてマクロを呼び出すときに実行されます。

```php
$this->browse(function (Browser $browser) use ($user) {
    $browser->visit('/pay')
        ->scrollToElement('#credit-card-details')
        ->assertSee('Enter Credit Card Details');
});
```

<a name="authentication"></a>
### 認証

多くの場合、認証が必要なページをテストすることになります。 Dusk の `loginAs` メソッドを使用すると、テストのたびにアプリケーションのログイン画面との対話を避けることができます。 `loginAs` メソッドは、認証可能なモデルまたは認証可能なモデル インスタンスに関連付けられた主キーを受け入れます。

```php
use App\Models\User;
use Laravel\Dusk\Browser;

$this->browse(function (Browser $browser) {
    $browser->loginAs(User::find(1))
        ->visit('/home');
});
```

> [!WARNING]
> `loginAs` メソッドを使用した後、ユーザー セッションはファイル内のすべてのテストに対して維持されます。

<a name="cookies"></a>
### クッキー

`cookie` メソッドを使用して、暗号化された Cookie の値を取得または設定できます。デフォルトでは、Laravel によって作成されたすべての Cookie は暗号化されます。

```php
$browser->cookie('name');

$browser->cookie('name', 'Taylor');
```

`plainCookie` メソッドを使用して、暗号化されていない Cookie の値を取得または設定できます。

```php
$browser->plainCookie('name');

$browser->plainCookie('name', 'Taylor');
```

`deleteCookie` メソッドを使用して、指定された Cookie を削除できます。

```php
$browser->deleteCookie('name');
```

<a name="executing-javascript"></a>
### JavaScriptの実行

`script` メソッドを使用して、ブラウザ内で任意の JavaScript ステートメントを実行できます。

```php
$browser->script('document.documentElement.scrollTop = 0');

$browser->script([
    'document.body.scrollTop = 0',
    'document.documentElement.scrollTop = 0',
]);

$output = $browser->script('return window.location.pathname');
```

<a name="taking-a-screenshot"></a>
### スクリーンショットを撮る

`screenshot` メソッドを使用してスクリーンショットを撮り、指定されたファイル名で保存できます。すべてのスクリーンショットは、`tests/Browser/screenshots` ディレクトリ内に保存されます。

```php
$browser->screenshot('filename');
```

`responsiveScreenshots` メソッドを使用すると、さまざまなブレークポイントで一連のスクリーンショットを取得できます。

```php
$browser->responsiveScreenshots('filename');
```

`screenshotElement` メソッドは、ページ上の特定の要素のスクリーンショットを撮るために使用できます。

```php
$browser->screenshotElement('#selector', 'filename');
```

<a name="storing-console-output-to-disk"></a>
### コンソール出力をディスクに保存する

`storeConsoleLog` メソッドを使用して、現在のブラウザのコンソール出力を指定されたファイル名でディスクに書き込むことができます。コンソール出力は、`tests/Browser/console` ディレクトリ内に保存されます。

```php
$browser->storeConsoleLog('filename');
```

<a name="storing-page-source-to-disk"></a>
### ページソースをディスクに保存する

`storeSource` メソッドを使用して、現在のページのソースを指定されたファイル名でディスクに書き込むことができます。ページのソースは、`tests/Browser/source` ディレクトリ内に保存されます。

```php
$browser->storeSource('filename');
```

<a name="interacting-with-elements"></a>
## 要素との対話 (Interacting With Elements)

<a name="dusk-selectors"></a>
### Dusk セレクタ

要素と対話するための適切な CSS セレクターを選択することは、Dusk テストを作成する際に最も難しい部分の 1 つです。時間の経過とともに、フロントエンドの変更により、次のような CSS セレクターがテストを中断する可能性があります。

```html
// HTML...

<button>Login</button>
```

```php
// Test...

$browser->click('.login-page .container div > button');
```

Dusk セレクターを使用すると、CSS セレクターを覚えるのではなく、効果的なテストの作成に集中できます。セレクターを定義するには、HTML 要素に `dusk` 属性を追加します。次に、Dusk ブラウザを操作するときに、セレクターの先頭に `@` を付けて、テスト内で添付された要素を操作します。

```html
// HTML...

<button dusk="login-button">Login</button>
```

```php
// Test...

$browser->click('@login-button');
```

必要に応じて、`selectorHtmlAttribute` メソッドを介して Dusk セレクターが使用する HTML 属性をカスタマイズできます。通常、このメソッドは、アプリケーションの `AppServiceProvider` の `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Dusk\Dusk;

Dusk::selectorHtmlAttribute('data-dusk');
```

<a name="text-values-and-attributes"></a>
### テキスト、値、および属性

<a name="retrieving-setting-values"></a>
#### 値の取得と設定

Dusk は、ページ上の要素の現在の値、表示テキスト、および属性を操作するためのメソッドをいくつか提供します。たとえば、特定の CSS または Dusk セレクターに一致する要素の「値」を取得するには、`value` メソッドを使用します。

```php
// Retrieve the value...
$value = $browser->value('selector');

// Set the value...
$browser->value('selector', 'value');
```

`inputValue` メソッドを使用して、指定されたフィールド名を持つ入力要素の「値」を取得できます。

```php
$value = $browser->inputValue('field');
```

<a name="retrieving-text"></a>
#### テキストの取得

`text` メソッドは、指定されたセレクターに一致する要素の表示テキストを取得するために使用できます。

```php
$text = $browser->text('selector');
```

<a name="retrieving-attributes"></a>
#### 属性の取得

最後に、`attribute` メソッドを使用して、指定されたセレクターに一致する要素の属性の値を取得できます。

```php
$attribute = $browser->attribute('selector', 'value');
```

<a name="interacting-with-forms"></a>
### フォームの操作

<a name="typing-values"></a>
#### 値の入力

Dusk は、フォームや入力要素を操作するためのさまざまなメソッドを提供します。まず、入力フィールドにテキストを入力する例を見てみましょう。

```php
$browser->type('email', 'taylor@laravel.com');
```

このメソッドは必要に応じて CSS セレクターを受け入れますが、CSS セレクターを `type` メソッドに渡す必要はないことに注意してください。 CSS セレクターが提供されていない場合、Dusk は指定された `name` 属性を持つ `input` または `textarea` フィールドを検索します。

内容をクリアせずにフィールドにテキストを追加するには、`append` メソッドを使用できます。

```php
$browser->type('tags', 'foo')
    ->append('tags', ', bar, baz');
```

`clear` メソッドを使用して入力の値をクリアできます。

```php
$browser->clear('email');
```

`typeSlowly` メソッドを使用して、Dusk にゆっくり入力するように指示できます。デフォルトでは、Dusk はキーを押すまでの間に 100 ミリ秒間一時停止します。キーを押すまでの時間をカスタマイズするには、メソッドの 3 番目の引数として適切なミリ秒数を渡します。

```php
$browser->typeSlowly('mobile', '+1 (202) 555-5555');

$browser->typeSlowly('mobile', '+1 (202) 555-5555', 300);
```

`appendSlowly` メソッドを使用すると、テキストをゆっくり追加できます。

```php
$browser->type('tags', 'foo')
    ->appendSlowly('tags', ', bar, baz');
```

<a name="dropdowns"></a>
#### ドロップダウン

`select` 要素で使用可能な値を選択するには、`select` メソッドを使用できます。 `type` メソッドと同様、`select` メソッドには完全な CSS セレクターは必要ありません。 `select` メソッドに値を渡すときは、表示テキストの代わりに基になるオプション値を渡す必要があります。

```php
$browser->select('size', 'Large');
```

2 番目の引数を省略すると、ランダムなオプションを選択できます。

```php
$browser->select('size');
```

`select` メソッドの 2 番目の引数として配列を指定すると、メソッドに複数のオプションを選択するように指示できます。

```php
$browser->select('categories', ['Art', 'Music']);
```

<a name="checkboxes"></a>
#### チェックボックス

チェックボックスの入力を「チェック」するには、`check` メソッドを使用できます。他の多くの入力関連メソッドと同様、完全な CSS セレクターは必要ありません。 CSS セレクターの一致が見つからない場合、Dusk は一致する `name` 属性を持つチェックボックスを検索します。

```php
$browser->check('terms');
```

`uncheck` メソッドは、チェックボックスの入力を「オフ」にするために使用できます。

```php
$browser->uncheck('terms');
```

<a name="radio-buttons"></a>
#### ラジオボタン

`radio` 入力オプションを「選択」するには、`radio` メソッドを使用できます。他の多くの入力関連メソッドと同様、完全な CSS セレクターは必要ありません。 CSS セレクターの一致が見つからない場合、Dusk は `name` 属性と `value` 属性が一致する `radio` 入力を検索します。

```php
$browser->radio('size', 'large');
```

<a name="attaching-files"></a>
### ファイルの添付

`attach` メソッドは、`file` 入力要素にファイルを添付するために使用できます。他の多くの入力関連メソッドと同様、完全な CSS セレクターは必要ありません。 CSS セレクターの一致が見つからない場合、Dusk は一致する `name` 属性を持つ `file` 入力を検索します。

```php
$browser->attach('photo', __DIR__.'/photos/mountains.png');
```

> [!WARNING]
> アタッチ機能を使用するには、`Zip` PHP 拡張機能がサーバーにインストールされ、有効になっている必要があります。

<a name="pressing-buttons"></a>
### ボタンを押す

`press` メソッドは、ページ上のボタン要素をクリックするために使用できます。 `press` メソッドに指定される引数は、ボタンの表示テキストまたは CSS / Dusk セレクターのいずれかです。

```php
$browser->press('Login');
```

フォームを送信するとき、多くのアプリケーションは、フォームの送信ボタンが押された後に無効にし、フォーム送信の HTTP リクエストが完了するとボタンを再度有効にします。ボタンを押してボタンが再び有効になるまで待つには、`pressAndWaitFor` メソッドを使用できます。

```php
// Press the button and wait a maximum of 5 seconds for it to be enabled...
$browser->pressAndWaitFor('Save');

// Press the button and wait a maximum of 1 second for it to be enabled...
$browser->pressAndWaitFor('Save', 1);
```

<a name="clicking-links"></a>
### リンクをクリックする

リンクをクリックするには、ブラウザ インスタンスで `clickLink` メソッドを使用できます。 `clickLink` メソッドは、指定された表示テキストを持つリンクをクリックします。

```php
$browser->clickLink($linkText);
```

`seeLink` メソッドを使用して、指定された表示テキストを持つリンクがページ上に表示されるかどうかを判断できます。

```php
if ($browser->seeLink($linkText)) {
    // ...
}
```

> [!WARNING]
> これらのメソッドは jQuery と対話します。ページで jQuery が使用できない場合、Dusk はそれをページに自動的に挿入し、テスト期間中使用できるようにします。

<a name="using-the-keyboard"></a>
### キーボードの使用

`keys` メソッドを使用すると、`type` メソッドで通常許可されるよりも複雑な入力シーケンスを特定の要素に提供できます。たとえば、値を入力するときに修飾キーを押し続けるように Dusk に指示できます。この例では、指定されたセレクターに一致する要素に `taylor` が入力されている間、`shift` キーが保持されます。 `taylor` を入力すると、修飾キーなしで `swift` が入力されます。

```php
$browser->keys('selector', ['{shift}', 'taylor'], 'swift');
```

`keys` メソッドのもう 1 つの有益な使用例は、「キーボード ショートカット」の組み合わせをアプリケーションのプライマリ CSS セレクターに送信することです。

```php
$browser->keys('.app', ['{command}', 'j']);
```

> [!NOTE]
> `{command}` などのすべての修飾キーは、`{}` 文字でラップされ、`Facebook\WebDriver\WebDriverKeys` クラスで定義された定数 ([GitHub で見つかりました](https://github.com/php-webdriver/php-webdriver/blob/master/lib/WebDriverKeys.php) など) と一致します。

<a name="fluent-keyboard-interactions"></a>
#### 流暢なキーボード操作

Dusk は `withKeyboard` メソッドも提供しており、`Laravel\Dusk\Keyboard` クラスを介して複雑なキーボード操作をスムーズに実行できます。 `Keyboard` クラスは、`press`、`release`、`type`、および `pause` メソッドを提供します。

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
#### キーボードマクロ

テスト スイート全体で簡単に再利用できるカスタム キーボード インタラクションを定義したい場合は、`Keyboard` クラスによって提供される `macro` メソッドを使用できます。通常、このメソッドは [サービスプロバイダの](/docs/{{version}}/providers) `boot` メソッドから呼び出す必要があります。

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

`macro` 関数は、最初の引数として名前を受け入れ、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャは、`Keyboard` インスタンスのメソッドとしてマクロを呼び出すときに実行されます。

```php
$browser->click('@textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->copy())
    ->click('@another-textarea')
    ->withKeyboard(fn (Keyboard $keyboard) => $keyboard->paste());
```

<a name="using-the-mouse"></a>
### マウスの使用

<a name="clicking-on-elements"></a>
#### 要素をクリックする

`click` メソッドは、指定された CSS または Dusk セレクターに一致する要素をクリックするために使用できます。

```php
$browser->click('.selector');
```

`clickAtXPath` メソッドは、指定された XPath 式に一致する要素をクリックするために使用できます。

```php
$browser->clickAtXPath('//div[@class = "selector"]');
```

`clickAtPoint` メソッドを使用すると、ブラウザの表示可能領域を基準とした特定の座標ペアで最上位の要素をクリックできます。

```php
$browser->clickAtPoint($x = 0, $y = 0);
```

`doubleClick` メソッドは、マウスのダブルクリックをシミュレートするために使用できます。

```php
$browser->doubleClick();

$browser->doubleClick('.selector');
```

`rightClick` メソッドは、マウスの右クリックをシミュレートするために使用できます。

```php
$browser->rightClick();

$browser->rightClick('.selector');
```

`clickAndHold` メソッドは、マウス ボタンをクリックして押し続けることをシミュレートするために使用できます。後続の `releaseMouse` メソッドの呼び出しにより、この動作は元に戻され、マウス ボタンが放されます。

```php
$browser->clickAndHold('.selector');

$browser->clickAndHold()
    ->pause(1000)
    ->releaseMouse();
```

`controlClick` メソッドは、ブラウザ内で `ctrl+click` イベントをシミュレートするために使用できます。

```php
$browser->controlClick();

$browser->controlClick('.selector');
```

`clickWhenVisible` メソッドまたは `clickWhenEnabled` メソッドを使用すると、要素を 1 回だけクリックする前に、要素の準備が完了するまで待機できます。

```php
$browser->clickWhenVisible('@save-button');
$browser->clickWhenEnabled('@submit-button');
```

<a name="mouseover"></a>
#### マウスオーバー

`mouseover` メソッドは、指定された CSS または Dusk セレクターに一致する要素上にマウスを移動する必要がある場合に使用できます。

```php
$browser->mouseover('.selector');
```

<a name="drag-drop"></a>
#### ドラッグアンドドロップ

`drag` メソッドは、指定されたセレクターに一致する要素を別の要素にドラッグするために使用できます。

```php
$browser->drag('.from-selector', '.to-selector');
```

または、要素を単一方向にドラッグすることもできます。

```php
$browser->dragLeft('.selector', $pixels = 10);
$browser->dragRight('.selector', $pixels = 10);
$browser->dragUp('.selector', $pixels = 10);
$browser->dragDown('.selector', $pixels = 10);
```

最後に、指定されたオフセットだけ要素をドラッグできます。

```php
$browser->dragOffset('.selector', $x = 10, $y = 10);
```

<a name="javascript-dialogs"></a>
### JavaScript ダイアログ

Dusk は、JavaScript ダイアログを操作するためのさまざまなメソッドを提供します。たとえば、`waitForDialog` メソッドを使用して、JavaScript ダイアログが表示されるのを待つことができます。このメソッドは、ダイアログが表示されるまで待機する秒数を示すオプションの引数を受け取ります。

```php
$browser->waitForDialog($seconds = null);
```

`assertDialogOpened` メソッドは、ダイアログが表示され、指定されたメッセージが含まれていることをアサートするために使用できます。

```php
$browser->assertDialogOpened('Dialog message');
```

JavaScript ダイアログにプロンプ​​トが含​​まれている場合は、`typeInDialog` メソッドを使用してプロンプトに値を入力できます。

```php
$browser->typeInDialog('Hello World');
```

「OK」ボタンをクリックして開いている JavaScript ダイアログを閉じるには、`acceptDialog` メソッドを呼び出すことができます。

```php
$browser->acceptDialog();
```

[キャンセル] ボタンをクリックして開いている JavaScript ダイアログを閉じるには、`dismissDialog` メソッドを呼び出すことができます。

```php
$browser->dismissDialog();
```

<a name="interacting-with-iframes"></a>
### インラインフレームの操作

iframe 内の要素を操作する必要がある場合は、`withinFrame` メソッドを使用できます。 `withinFrame` メソッドに提供されたクロージャー内で行われるすべての要素の対話は、指定された iframe のコンテキストにスコープされます。

```php
$browser->withinFrame('#credit-card-details', function ($browser) {
    $browser->type('input[name="cardnumber"]', '4242424242424242')
        ->type('input[name="exp-date"]', '1224')
        ->type('input[name="cvc"]', '123')
        ->press('Pay');
});
```

<a name="scoping-selectors"></a>
### スコープセレクター

場合によっては、特定のセレクター内ですべての操作をスコープしながら、複数の操作を実行したい場合があります。たとえば、一部のテキストがテーブル内にのみ存在することを主張し、そのテーブル内のボタンをクリックしたい場合があります。これを実現するには、`with` メソッドを使用できます。 `with` メソッドに指定されたクロージャー内で実行されるすべての操作は、元のセレクターにスコープされます。

```php
$browser->with('.table', function (Browser $table) {
    $table->assertSee('Hello World')
        ->clickLink('Delete');
});
```

現在のスコープ外でアサーションを実行する必要がある場合があります。これを実現するには、`elsewhere` メソッドと `elsewhereWhenAvailable` メソッドを使用できます。

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
### 要素を待っています

JavaScript を広範囲に使用するアプリケーションをテストする場合、多くの場合、テストを続行する前に、特定の要素またはデータが使用可能になるまで「待つ」必要があります。Dusk時はこれが楽になります。さまざまな方法を使用して、要素がページ上に表示されるまで待機したり、特定の JavaScript 式が `true` と評価されるまで待機したりできます。

<a name="waiting"></a>
#### 待っている

指定したミリ秒数だけテストを一時停止する必要がある場合は、`pause` メソッドを使用します。

```php
$browser->pause(1000);
```

特定の条件が `true` の場合にのみテストを一時停止する必要がある場合は、`pauseIf` メソッドを使用します。

```php
$browser->pauseIf(App::environment('production'), 1000);
```

同様に、特定の条件が `true` でない限りテストを一時停止する必要がある場合は、`pauseUnless` メソッドを使用できます。

```php
$browser->pauseUnless(App::environment('testing'), 1000);
```

<a name="waiting-for-selectors"></a>
#### セレクタを待っています

`waitFor` メソッドを使用すると、指定された CSS または Dusk セレクターに一致する要素がページに表示されるまでテストの実行を一時停止できます。デフォルトでは、例外がスローされる前にテストが最大 5 秒間一時停止されます。必要に応じて、カスタム タイムアウトしきい値を 2 番目の引数としてメソッドに渡すことができます。

```php
// Wait a maximum of five seconds for the selector...
$browser->waitFor('.selector');

// Wait a maximum of one second for the selector...
$browser->waitFor('.selector', 1);
```

指定されたセレクターに一致する要素に指定されたテキストが含まれるまで待つこともできます。

```php
// Wait a maximum of five seconds for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World');

// Wait a maximum of one second for the selector to contain the given text...
$browser->waitForTextIn('.selector', 'Hello World', 1);
```

指定されたセレクターに一致する要素がページからなくなるまで待つこともできます。

```php
// Wait a maximum of five seconds until the selector is missing...
$browser->waitUntilMissing('.selector');

// Wait a maximum of one second until the selector is missing...
$browser->waitUntilMissing('.selector', 1);
```

または、指定されたセレクターに一致する要素が有効または無効になるまで待つこともできます。

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
#### 有効な場合のスコープ セレクター

場合によっては、特定のセレクターに一致する要素が表示されるのを待ってから、その要素を操作したい場合があります。たとえば、モーダル ウィンドウが使用可能になるまで待ってから、モーダル内の [OK] ボタンを押すとよいでしょう。これを実現するには、`whenAvailable` メソッドを使用できます。指定されたクロージャー内で実行されるすべての要素操作は、元のセレクターにスコープされます。

```php
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Hello World')
        ->press('OK');
});
```

<a name="waiting-for-text"></a>
#### テキストを待っています

`waitForText` メソッドは、指定されたテキストがページに表示されるまで待機するために使用できます。

```php
// Wait a maximum of five seconds for the text...
$browser->waitForText('Hello World');

// Wait a maximum of one second for the text...
$browser->waitForText('Hello World', 1);
```

`waitUntilMissingText` メソッドを使用して、表示されたテキストがページから削除されるまで待つことができます。

```php
// Wait a maximum of five seconds for the text to be removed...
$browser->waitUntilMissingText('Hello World');

// Wait a maximum of one second for the text to be removed...
$browser->waitUntilMissingText('Hello World', 1);
```

<a name="waiting-for-links"></a>
#### リンクを待っています

`waitForLink` メソッドは、指定されたリンク テキストがページに表示されるまで待機するために使用できます。

```php
// Wait a maximum of five seconds for the link...
$browser->waitForLink('Create');

// Wait a maximum of one second for the link...
$browser->waitForLink('Create', 1);
```

<a name="waiting-for-inputs"></a>
#### 入力を待っています

`waitForInput` メソッドは、指定された入力フィールドがページに表示されるまで待機するために使用できます。

```php
// Wait a maximum of five seconds for the input...
$browser->waitForInput($field);

// Wait a maximum of one second for the input...
$browser->waitForInput($field, 1);
```

<a name="waiting-on-the-page-location"></a>
#### ページの場所を待っています

`$browser->assertPathIs('/home')` などのパス アサーションを作成する場合、`window.location.pathname` が非同期的に更新されている場合、アサーションが失敗する可能性があります。 `waitForLocation` メソッドを使用して、場所が指定された値になるまで待機できます。

```php
$browser->waitForLocation('/secret');
```

`waitForLocation` メソッドを使用して、現在のウィンドウの位置が完全修飾 URL になるのを待つこともできます。

```php
$browser->waitForLocation('https://example.com/path');
```

[名前付きルートの](/docs/{{version}}/routing#named-routes) の場所を待つこともできます。

```php
$browser->waitForRoute($routeName, $parameters);
```

<a name="waiting-for-page-reloads"></a>
#### ページのリロードを待機しています

アクションの実行後にページがリロードされるまで待機する必要がある場合は、`waitForReload` メソッドを使用します。

```php
use Laravel\Dusk\Browser;

$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})
->assertSee('Success!');
```

通常、ボタンをクリックした後にページがリロードされるまで待機する必要があるため、便宜上 `clickAndWaitForReload` メソッドを使用できます。

```php
$browser->clickAndWaitForReload('.selector')
    ->assertSee('something');
```

<a name="waiting-on-javascript-expressions"></a>
#### JavaScript 式を待機しています

場合によっては、特定の JavaScript 式が `true` と評価されるまで、テストの実行を一時停止したい場合があります。これは、`waitUntil` メソッドを使用して簡単に実行できます。このメソッドに式を渡す場合、`return` キーワードや末尾のセミコロンを含める必要はありません。

```php
// Wait a maximum of five seconds for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0');

// Wait a maximum of one second for the expression to be true...
$browser->waitUntil('App.data.servers.length > 0', 1);
```

<a name="waiting-on-vue-expressions"></a>
#### Vue 式を待機しています

`waitUntilVue` メソッドと `waitUntilVueIsNot` メソッドは、[Vue コンポーネント](https://vuejs.org) 属性が指定された値になるまで待機するために使用できます。

```php
// Wait until the component attribute contains the given value...
$browser->waitUntilVue('user.name', 'Taylor', '@user');

// Wait until the component attribute doesn't contain the given value...
$browser->waitUntilVueIsNot('user.name', null, '@user');
```

<a name="waiting-for-javascript-events"></a>
#### JavaScript イベントを待機しています

`waitForEvent` メソッドを使用すると、JavaScript イベントが発生するまでテストの実行を一時停止できます。

```php
$browser->waitForEvent('load');
```

イベント リスナは現在のスコープ (デフォルトでは `body` 要素) にアタッチされます。スコープ付きセレクターを使用する場合、イベント リスナは一致する要素にアタッチされます。

```php
$browser->with('iframe', function (Browser $iframe) {
    // Wait for the iframe's load event...
    $iframe->waitForEvent('load');
});
```

`waitForEvent` メソッドの 2 番目の引数としてセレクターを指定して、イベント リスナを特定の要素にアタッチすることもできます。

```php
$browser->waitForEvent('load', '.selector');
```

`document` および `window` オブジェクトのイベントを待つこともできます。

```php
// Wait until the document is scrolled...
$browser->waitForEvent('scroll', 'document');

// Wait a maximum of five seconds until the window is resized...
$browser->waitForEvent('resize', 'window', 5);
```

<a name="waiting-with-a-callback"></a>
#### コールバックで待機する

Dusk の「待機」メソッドの多くは、基礎となる `waitUsing` メソッドに依存しています。このメソッドを直接使用して、特定のクロージャが `true` を返すのを待つことができます。 `waitUsing` メソッドは、待機する最大秒数、クロージャを評価する間隔、クロージャ、およびオプションの失敗メッセージを受け入れます。

```php
$browser->waitUsing(10, 1, function () use ($something) {
    return $something->isReady();
}, "Something wasn't ready in time.");
```

<a name="scrolling-an-element-into-view"></a>
### 要素をスクロールして表示する

要素がブラウザの表示領域外にあるため、要素をクリックできない場合があります。 `scrollIntoView` メソッドは、指定されたセレクターの要素がビュー内に表示されるまでブラウザ ウィンドウをスクロールします。

```php
$browser->scrollIntoView('.selector')
    ->click('.selector');
```

<a name="available-assertions"></a>
## 利用可能なアサーション (Available Assertions)

Dusk は、アプリケーションに対して行うことができるさまざまなアサーションを提供します。利用可能なアサーションはすべて、以下のリストに記載されています。

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
#### アサートタイトル

ページ タイトルが指定されたテキストと一致することをアサートします。

```php
$browser->assertTitle($title);
```

<a name="assert-title-contains"></a>
#### アサートタイトル次を含む

ページ タイトルに指定されたテキストが含まれていることをアサートします。

```php
$browser->assertTitleContains($title);
```

<a name="assert-url-is"></a>
#### アサートURL

現在の URL (クエリ文字列なし) が指定された文字列と一致することをアサートします。

```php
$browser->assertUrlIs($url);
```

<a name="assert-scheme-is"></a>
#### アサートスキーム

現在の URL スキームが指定されたスキームと一致することをアサートします。

```php
$browser->assertSchemeIs($scheme);
```

<a name="assert-scheme-is-not"></a>
#### アサートスキームがありません

現在の URL スキームが指定されたスキームと一致しないことをアサートします。

```php
$browser->assertSchemeIsNot($scheme);
```

<a name="assert-host-is"></a>
#### アサートホスト

現在の URL ホストが指定されたホストと一致することをアサートします。

```php
$browser->assertHostIs($host);
```

<a name="assert-host-is-not"></a>
#### ホストが存在しないことをアサート

現在の URL ホストが指定されたホストと一致しないことをアサートします。

```php
$browser->assertHostIsNot($host);
```

<a name="assert-port-is"></a>
#### アサートポートI

現在の URL ポートが指定されたポートと一致することをアサートします。

```php
$browser->assertPortIs($port);
```

<a name="assert-port-is-not"></a>
#### アサートポートがありません

現在の URL ポートが指定されたポートと一致しないことをアサートします。

```php
$browser->assertPortIsNot($port);
```

<a name="assert-path-begins-with"></a>
#### アサートパスの始まり

現在の URL パスが指定されたパスで始まることをアサートします。

```php
$browser->assertPathBeginsWith('/home');
```

<a name="assert-path-ends-with"></a>
#### assertPathEndsWith

現在の URL パスが指定されたパスで終わることをアサートします。

```php
$browser->assertPathEndsWith('/home');
```

<a name="assert-path-contains"></a>
#### アサートパスが含まれる

現在の URL パスに指定されたパスが含まれていることをアサートします。

```php
$browser->assertPathContains('/home');
```

<a name="assert-path-is"></a>
#### アサートパス

現在のパスが指定されたパスと一致することをアサートします。

```php
$browser->assertPathIs('/home');
```

<a name="assert-path-is-not"></a>
#### アサートパスがありません

現在のパスが指定されたパスと一致しないことをアサートします。

```php
$browser->assertPathIsNot('/home');
```

<a name="assert-route-is"></a>
#### アサートルートI

現在の URL が指定された [名前付きルートの](/docs/{{version}}/routing#named-routes) URL と一致することをアサートします。

```php
$browser->assertRouteIs($name, $parameters);
```

<a name="assert-query-string-has"></a>
#### assertQueryStringHas

指定されたクエリ文字列パラメータが存在することをアサートします。

```php
$browser->assertQueryStringHas($name);
```

指定されたクエリ文字列パラメータが存在し、指定された値を持つことをアサートします。

```php
$browser->assertQueryStringHas($name, $value);
```

<a name="assert-query-string-missing"></a>
#### assertQueryStringMissing

指定されたクエリ文字列パラメータが欠落していることをアサートします。

```php
$browser->assertQueryStringMissing($name);
```

<a name="assert-fragment-is"></a>
#### アサートフラグメントIs

URL の現在のハッシュ フラグメントが指定されたフラグメントと一致することをアサートします。

```php
$browser->assertFragmentIs('anchor');
```

<a name="assert-fragment-begins-with"></a>
#### アサートフラグメントで始まる

URL の現在のハッシュ フラグメントが指定されたフラグメントで始まることをアサートします。

```php
$browser->assertFragmentBeginsWith('anchor');
```

<a name="assert-fragment-is-not"></a>
#### アサートフラグメントはありません

URL の現在のハッシュ フラグメントが指定されたフラグメントと一致しないことをアサートします。

```php
$browser->assertFragmentIsNot('anchor');
```

<a name="assert-has-cookie"></a>
#### アサートはCookieを持っています

指定された暗号化された Cookie が存在することをアサートします。

```php
$browser->assertHasCookie($name);
```

<a name="assert-has-plain-cookie"></a>
#### アサートHasPlainCookie

指定された暗号化されていない Cookie が存在することをアサートします。

```php
$browser->assertHasPlainCookie($name);
```

<a name="assert-cookie-missing"></a>
#### アサートクッキーがありません

指定された暗号化された Cookie が存在しないことをアサートします。

```php
$browser->assertCookieMissing($name);
```

<a name="assert-plain-cookie-missing"></a>
#### assertPlainCookieMissing

指定された暗号化されていない Cookie が存在しないことをアサートします。

```php
$browser->assertPlainCookieMissing($name);
```

<a name="assert-cookie-value"></a>
#### アサートクッキー値

暗号化された Cookie が指定された値を持つことをアサートします。

```php
$browser->assertCookieValue($name, $value);
```

<a name="assert-plain-cookie-value"></a>
#### アサートプレーンクッキー値

暗号化されていない Cookie が指定された値を持つことをアサートします。

```php
$browser->assertPlainCookieValue($name, $value);
```

<a name="assert-see"></a>
#### アサートを参照

指定されたテキストがページ上に存在することをアサートします。

```php
$browser->assertSee($text);
```

<a name="assert-dont-see"></a>
#### 主張しないでください

指定されたテキストがページ上に存在しないことをアサートします。

```php
$browser->assertDontSee($text);
```

<a name="assert-see-in"></a>
#### アサート見る

指定されたテキストがセレクター内に存在することをアサートします。

```php
$browser->assertSeeIn($selector, $text);
```

<a name="assert-dont-see-in"></a>
#### 主張しないで見てください

指定されたテキストがセレクター内に存在しないことをアサートします。

```php
$browser->assertDontSeeIn($selector, $text);
```

<a name="assert-see-anything-in"></a>
#### アサート何でも見る

セレクター内にテキストが存在することをアサートします。

```php
$browser->assertSeeAnythingIn($selector);
```

<a name="assert-see-nothing-in"></a>
#### アサートSeeNothingIn

セレクター内にテキストが存在しないことをアサートします。

```php
$browser->assertSeeNothingIn($selector);
```

<a name="assert-count"></a>
#### アサートカウント

指定されたセレクターに一致する要素が指定された回数出現することをアサートします。

```php
$browser->assertCount($selector, $count);
```

<a name="assert-script"></a>
#### アサートスクリプト

指定された JavaScript 式が指定された値に評価されることをアサートします。

```php
$browser->assertScript('window.isLoaded')
    ->assertScript('document.readyState', 'complete');
```

<a name="assert-source-has"></a>
#### アサートソースが持っています

指定されたソース コードがページ上に存在することをアサートします。

```php
$browser->assertSourceHas($code);
```

<a name="assert-source-missing"></a>
#### アサートソースが見つかりません

指定されたソース コードがページ上に存在しないことをアサートします。

```php
$browser->assertSourceMissing($code);
```

<a name="assert-see-link"></a>
#### アサートリンクを参照

指定されたリンクがページ上に存在することをアサートします。

```php
$browser->assertSeeLink($linkText);
```

<a name="assert-dont-see-link"></a>
#### アサートドントシーリンク

指定されたリンクがページ上に存在しないことをアサートします。

```php
$browser->assertDontSeeLink($linkText);
```

<a name="assert-input-value"></a>
#### アサート入力値

指定された入力フィールドに指定された値があることをアサートします。

```php
$browser->assertInputValue($field, $value);
```

<a name="assert-input-value-is-not"></a>
#### アサート入力値がありません

指定された入力フィールドに指定された値が存在しないことをアサートします。

```php
$browser->assertInputValueIsNot($field, $value);
```

<a name="assert-checked"></a>
#### アサートチェック済み

指定されたチェックボックスがチェックされていることをアサートします。

```php
$browser->assertChecked($field);
```

<a name="assert-not-checked"></a>
#### アサート未チェック

指定されたチェックボックスがチェックされていないことをアサートします。

```php
$browser->assertNotChecked($field);
```

<a name="assert-indeterminate"></a>
#### アサート不定

指定されたチェックボックスが不定状態であることをアサートします。

```php
$browser->assertIndeterminate($field);
```

<a name="assert-radio-selected"></a>
#### アサートラジオ選択済み

指定された無線フィールドが選択されていることをアサートします。

```php
$browser->assertRadioSelected($field, $value);
```

<a name="assert-radio-not-selected"></a>
#### アサートラジオが選択されていません

指定された無線フィールドが選択されていないことをアサートします。

```php
$browser->assertRadioNotSelected($field, $value);
```

<a name="assert-selected"></a>
#### アサート選択済み

指定されたドロップダウンで指定された値が選択されていることをアサートします。

```php
$browser->assertSelected($field, $value);
```

<a name="assert-not-selected"></a>
#### アサート未選択

指定されたドロップダウンに指定された値が選択されていないことをアサートします。

```php
$browser->assertNotSelected($field, $value);
```

<a name="assert-select-has-options"></a>
#### assertSelectHasOptions

指定された値の配列が選択可能であることをアサートします。

```php
$browser->assertSelectHasOptions($field, $values);
```

<a name="assert-select-missing-options"></a>
#### アサート選択欠落オプション

指定された値の配列が選択できないことをアサートします。

```php
$browser->assertSelectMissingOptions($field, $values);
```

<a name="assert-select-has-option"></a>
#### assertSelectHasOption

指定された値が指定されたフィールドで選択できることをアサートします。

```php
$browser->assertSelectHasOption($field, $value);
```

<a name="assert-select-missing-option"></a>
#### アサート選択欠落オプション

指定された値が選択できないことをアサートします。

```php
$browser->assertSelectMissingOption($field, $value);
```

<a name="assert-value"></a>
#### アサート値

指定されたセレクターに一致する要素が指定された値を持つことをアサートします。

```php
$browser->assertValue($selector, $value);
```

<a name="assert-value-is-not"></a>
#### アサート値はありません

指定されたセレクターに一致する要素が指定された値を持たないことをアサートします。

```php
$browser->assertValueIsNot($selector, $value);
```

<a name="assert-attribute"></a>
#### アサート属性

指定されたセレクターに一致する要素が、指定された属性に指定された値を持つことをアサートします。

```php
$browser->assertAttribute($selector, $attribute, $value);
```

<a name="assert-attribute-missing"></a>
#### アサート属性がありません

指定されたセレクターに一致する要素に、指定された属性が欠落していることをアサートします。

```php
$browser->assertAttributeMissing($selector, $attribute);
```

<a name="assert-attribute-contains"></a>
#### assertAttributeContains

指定されたセレクターに一致する要素に、指定された属性に指定された値が含まれていることをアサートします。

```php
$browser->assertAttributeContains($selector, $attribute, $value);
```

<a name="assert-attribute-doesnt-contain"></a>
#### assertAttributeDoesntContain

指定されたセレクターに一致する要素に、指定された属性に指定された値が含まれていないことをアサートします。

```php
$browser->assertAttributeDoesntContain($selector, $attribute, $value);
```

<a name="assert-aria-attribute"></a>
#### アサートアリア属性

指定されたセレクターに一致する要素が、指定された aria 属性に指定された値を持つことをアサートします。

```php
$browser->assertAriaAttribute($selector, $attribute, $value);
```

たとえば、マークアップ `<button aria-label="Add"></button>` がある場合、次のように `aria-label` 属性に対してアサートできます。

```php
$browser->assertAriaAttribute('button', 'label', 'Add')
```

<a name="assert-data-attribute"></a>
#### アサートデータ属性

指定されたセレクターに一致する要素が、指定されたデータ属性に指定された値を持つことをアサートします。

```php
$browser->assertDataAttribute($selector, $attribute, $value);
```

たとえば、マークアップ `<tr id="row-1" data-content="attendees"></tr>` がある場合、次のように `data-content` 属性に対してアサートできます。

```php
$browser->assertDataAttribute('#row-1', 'content', 'attendees')
```

<a name="assert-visible"></a>
#### アサート可視

指定されたセレクターに一致する要素が表示されていることをアサートします。

```php
$browser->assertVisible($selector);
```

<a name="assert-present"></a>
#### アサート現在

指定されたセレクターに一致する要素がソース内に存在することをアサートします。

```php
$browser->assertPresent($selector);
```

<a name="assert-not-present"></a>
#### アサートされていません

指定されたセレクターに一致する要素がソースに存在しないことをアサートします。

```php
$browser->assertNotPresent($selector);
```

<a name="assert-missing"></a>
#### アサート欠落しています

指定されたセレクターに一致する要素が表示されていないことをアサートします。

```php
$browser->assertMissing($selector);
```

<a name="assert-input-present"></a>
#### アサート入力現在

指定された名前の入力が存在することをアサートします。

```php
$browser->assertInputPresent($name);
```

<a name="assert-input-missing"></a>
#### アサート入力がありません

指定された名前の入力がソースに存在しないことをアサートします。

```php
$browser->assertInputMissing($name);
```

<a name="assert-dialog-opened"></a>
#### アサートダイアログが開きました

指定されたメッセージを含む JavaScript ダイアログが開いたことをアサートします。

```php
$browser->assertDialogOpened($message);
```

<a name="assert-enabled"></a>
#### アサート有効

指定されたフィールドが有効であることをアサートします。

```php
$browser->assertEnabled($field);
```

<a name="assert-disabled"></a>
#### アサート無効

指定されたフィールドが無効であることをアサートします。

```php
$browser->assertDisabled($field);
```

<a name="assert-button-enabled"></a>
#### アサートボタン有効

指定されたボタンが有効であることをアサートします。

```php
$browser->assertButtonEnabled($button);
```

<a name="assert-button-disabled"></a>
#### アサートボタン無効

指定されたボタンが無効になっていることをアサートします。

```php
$browser->assertButtonDisabled($button);
```

<a name="assert-focused"></a>
#### アサートフォーカス

指定されたフィールドがフォーカスされていることをアサートします。

```php
$browser->assertFocused($field);
```

<a name="assert-not-focused"></a>
#### アサートノットフォーカス

指定されたフィールドがフォーカスされていないことをアサートします。

```php
$browser->assertNotFocused($field);
```

<a name="assert-authenticated"></a>
#### 認証済み

ユーザーが認証されていることをアサートします。

```php
$browser->assertAuthenticated();
```

<a name="assert-guest"></a>
#### アサートゲスト

ユーザーが認証されていないことをアサートします。

```php
$browser->assertGuest();
```

<a name="assert-authenticated-as"></a>
#### 認証済みとしてアサート

ユーザーが指定されたユーザーとして認証されていることをアサートします。

```php
$browser->assertAuthenticatedAs($user);
```

<a name="assert-vue"></a>
#### アサートVue

Dusk では、[Vue コンポーネント](https://vuejs.org) データの状態についてアサーションを行うこともできます。たとえば、アプリケーションに次の Vue コンポーネントが含まれていると想像してください。

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

次のように Vue コンポーネントの状態をアサートできます。

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
#### アサートVueがありません

指定された Vue コンポーネント データ プロパティが指定された値と一致しないことをアサートします。

```php
$browser->assertVueIsNot($property, $value, $componentSelector = null);
```

<a name="assert-vue-contains"></a>
#### アサートVueが含まれている

指定された Vue コンポーネント データ プロパティが配列であり、指定された値が含まれていることをアサートします。

```php
$browser->assertVueContains($property, $value, $componentSelector = null);
```

<a name="assert-vue-doesnt-contain"></a>
#### assertVueDoesntContain

指定された Vue コンポーネント データ プロパティが配列であり、指定された値が含まれていないことをアサートします。

```php
$browser->assertVueDoesntContain($property, $value, $componentSelector = null);
```

<a name="pages"></a>
## ページ (Pages)

場合によっては、テストではいくつかの複雑なアクションを順番に実行する必要があります。これにより、テストが読みにくくなり、理解しにくくなる可能性があります。 Dusk Pages を使用すると、単一のメソッドを介して特定のページで実行できる表現アクションを定義できます。ページを使用すると、アプリケーションまたは単一ページの共通セレクターへのショートカットを定義することもできます。

<a name="generating-pages"></a>
### ページの生成

ページ オブジェクトを生成するには、`dusk:page` Artisan コマンドを実行します。すべてのページ オブジェクトは、アプリケーションの `tests/Browser/Pages` ディレクトリに配置されます。

```shell
php artisan dusk:page Login
```

<a name="configuring-pages"></a>
### ページの構成

デフォルトでは、ページには `url`、`assert`、および `elements` の 3 つのメソッドがあります。ここでは、`url` メソッドと `assert` メソッドについて説明します。 `elements` メソッドは [以下で詳しく説明します](#shorthand-selectors) になります。

<a name="the-url-method"></a>
#### `url` メソッド

`url` メソッドは、ページを表す URL のパスを返す必要があります。 Dusk はブラウザでページに移動するときにこの URL を使用します。

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
#### `assert` メソッド

`assert` メソッドは、ブラウザーが実際に指定されたページに存在することを確認するために必要なアサーションを行うことができます。実際には、このメソッド内に何も配置する必要はありません。ただし、必要に応じてこれらの主張を自由に行うことができます。これらのアサーションは、ページに移動すると自動的に実行されます。

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
### ページへの移動

ページが定義されたら、`visit` メソッドを使用してそのページに移動できます。

```php
use Tests\Browser\Pages\Login;

$browser->visit(new Login);
```

場合によっては、すでに特定のページにいて、そのページのセレクターとメソッドを現在のテスト コンテキストに「ロード」する必要がある場合があります。これは、ボタンを押すと、明示的に移動せずに特定のページにリダイレクトされる場合によく発生します。この状況では、`on` メソッドを使用してページをロードできます。

```php
use Tests\Browser\Pages\CreatePlaylist;

$browser->visit('/dashboard')
    ->clickLink('Create Playlist')
    ->on(new CreatePlaylist)
    ->assertSee('@create');
```

<a name="shorthand-selectors"></a>
### 短縮表記セレクター

ページ クラス内の `elements` メソッドを使用すると、ページ上の CSS セレクターにすばやく覚えやすいショートカットを定義できます。たとえば、アプリケーションのログイン ページの「電子メール」入力フィールドのショートカットを定義してみましょう。

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

ショートカットが定義されたら、通常は完全な CSS セレクターを使用する場所であればどこでも短縮セレクターを使用できます。

```php
$browser->type('@email', 'taylor@laravel.com');
```

<a name="global-shorthand-selectors"></a>
#### グローバル短縮表記セレクター

Dusk をインストールすると、基本 `Page` クラスが `tests/Browser/Pages` ディレクトリに配置されます。このクラスには、アプリケーション全体のすべてのページで使用できるグローバル短縮セレクターを定義するために使用できる `siteElements` メソッドが含まれています。

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
### ページメソッド

ページで定義されているデフォルトのメソッドに加えて、テスト全体で使用できる追加のメソッドを定義できます。たとえば、音楽管理アプリケーションを構築していると想像してみましょう。アプリケーションの 1 ページに対する一般的なアクションは、プレイリストの作成です。各テストでプレイリストを作成するロジックを書き直す代わりに、ページ クラスで `createPlaylist` メソッドを定義できます。

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

メソッドを定義したら、そのページを利用するテスト内でそのメソッドを使用できます。ブラウザー インスタンスは、カスタム ページ メソッドの最初の引数として自動的に渡されます。

```php
use Tests\Browser\Pages\Dashboard;

$browser->visit(new Dashboard)
    ->createPlaylist('My Playlist')
    ->assertSee('My Playlist');
```

<a name="components"></a>
## コンポーネント (Components)

コンポーネントは Dusk の「ページ オブジェクト」に似ていますが、ナビゲーション バーや通知ウィンドウなど、アプリケーション全体で再利用される UI や機能の一部を対象としています。そのため、コンポーネントは特定の URL にバインドされません。

<a name="generating-components"></a>
### コンポーネントの生成

コンポーネントを生成するには、`dusk:component` Artisan コマンドを実行します。新しいコンポーネントは `tests/Browser/Components` ディレクトリに配置されます。

```shell
php artisan dusk:component DatePicker
```

上に示したように、「日付ピッカー」は、アプリケーション全体のさまざまなページに存在する可能性があるコンポーネントの例です。テスト スイート全体の数十のテストで日付を選択するためにブラウザ自動化ロジックを手動で記述するのは面倒になる場合があります。代わりに、日付ピッカーを表す Dusk コンポーネントを定義して、そのロジックをコンポーネント内にカプセル化できます。

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
### コンポーネントの使用

コンポーネントが定義されたら、任意のテストから日付ピッカー内の日付を簡単に選択できます。また、日付の選択に必要なロジックが変更された場合は、コンポーネントを更新するだけで済みます。

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

`component` メソッドは、指定されたコンポーネントをスコープとするブラウザー インスタンスを取得するために使用できます。

```php
$datePicker = $browser->component(new DatePickerComponent);

$datePicker->selectDate(2019, 1, 30);

$datePicker->assertSee('January');
```

<a name="continuous-integration"></a>
## 継続的インテグレーション (Continuous Integration)

> [!WARNING]
> ほとんどの Dusk 継続的統合構成では、Laravel アプリケーションがポート 8000 の組み込み PHP 開発サーバーを使用して提供されることを想定しています。 したがって、続行する前に、継続的統合環境の `APP_URL` 環境変数値が `http://127.0.0.1:8000` であることを確認する必要があります。

<a name="running-tests-on-heroku-ci"></a>
### Heroku CI

[Heroku CI](https://www.heroku.com/continuous-integration) で Dusk テストを実行するには、次の Google Chrome ビルドパックとスクリプトを Heroku `app.json` ファイルに追加します。

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
### トラヴィスCI

[トラヴィスCI](https://travis-ci.org) で Dusk テストを実行するには、次の `.travis.yml` 構成を使用します。 Travis CI はグラフィカル環境ではないため、Chrome ブラウザを起動するには追加の手順を実行する必要があります。さらに、`php artisan serve` を使用して、PHP の組み込み Web サーバーを起動します。

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
### GitHub アクション

[GitHub アクション](https://github.com/features/actions) を使用して Dusk テストを実行している場合は、開始点として次の構成ファイルを使用できます。 TravisCI と同様に、`php artisan serve` コマンドを使用して、PHP の組み込み Web サーバーを起動します。

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
### チッパーCI

[チッパーCI](https://chipperci.com) を使用して Dusk テストを実行している場合は、開始点として次の構成ファイルを使用できます。 PHP の組み込みサーバーを使用して Laravel を実行し、リクエストをリッスンできるようにします。

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

データベースの使用方法など、Chipper CI での Dusk テストの実行の詳細については、[公式 Chipper CI ドキュメント](https://chipperci.com/docs/testing/laravel-dusk-new/) を参照してください。

