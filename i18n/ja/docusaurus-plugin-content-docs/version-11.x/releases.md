# リリースノート (Release Notes)

- [バージョン管理スキーム](#versioning-scheme)
- [サポートポリシー](#support-policy)
- [Laravel11](#laravel-11)

<a name="versioning-scheme"></a>
## バージョン管理スキーム (Versioning Scheme)

Laravel とその他のファーストパーティ パッケージは [セマンティック バージョニング](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^11.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
#### 名前付き引数

[名前付き引数](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
## サポートポリシー (Support Policy)

すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [Laravelによってサポートされています](/docs/{{version}}/database#introduction) を確認してください。

<div class="overflow-auto">

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 9 | 8.0～8.2 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |
| 11 | 8.2～8.4 | 2024 年 3 月 12 日 | 2025 年 9 月 3 日 | 2026 年 3 月 12 日 |
| 12 | 8.2～8.4 | 2025 年 2 月 24 日 | 2026 年 8 月 13 日 | 2027 年 2 月 24 日 |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

(*) サポートされている PHP バージョン

<a name="laravel-11"></a>
## Laravel11 (Laravel 11)

Laravel 11は、合理化されたアプリケーション構造、1秒あたりのレート制限、ヘルスルーティング、適切な暗号化キーローテーション、キューテストの改善、[Resend](https://resend.com)メールトランスポート、プロンプトバリデーターの統合、新しいArtisan コマンドなどを導入することにより、Laravel 10.xで行われた改善を継続しています。さらに、アプリケーションに堅牢なリアルタイム機能を提供するために、ファーストパーティのスケーラブルな WebSocket サーバーである Laravel Reverb が導入されました。

<a name="php-8"></a>
### PHP8.2

Laravel 11.x には、最小 PHP バージョン 8.2 が必要です。

<a name="structure"></a>
### 合理化されたアプリケーション構造

_Laravel の合理化されたアプリケーション構造は、[テイラー・オトウェル](https://github.com/taylorotwell) および [ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって開発されました。

Laravel 11 では、既存のアプリケーションを変更する必要がなく、**新しい** Laravel アプリケーション用に合理化されたアプリケーション構造が導入されています。新しいアプリケーション構造は、Laravel 開発者がすでによく知っている概念の多くを保持しながら、より無駄がなく、より現代的なエクスペリエンスを提供することを目的としています。以下では、Laravel の新しいアプリケーション構造のハイライトについて説明します。

#### アプリケーションのブートストラップ ファイル

`bootstrap/app.php` ファイルは、コードファーストのアプリケーション構成ファイルとして復活しました。このファイルから、アプリケーションのルーティング、ミドルウェア、サービスプロバイダ、例外処理などをカスタマイズできます。このファイルは、以前はアプリケーションのファイル構造全体に散在していたさまざまな高レベルのアプリケーション動作設定を統合します。

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        //
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

<a name="service-providers"></a>
#### サービスプロバイダ

デフォルトの Laravel アプリケーション構造には 5 つのサービスプロバイダが含まれていますが、Laravel 11 には `AppServiceProvider` が 1 つだけ含まれています。以前のサービスプロバイダの機能は `bootstrap/app.php` に組み込まれており、フレームワークによって自動的に処理されるか、アプリケーションの `AppServiceProvider` に配置される場合があります。

たとえば、イベント検出がデフォルトで有効になり、イベントとそのリスナを手動で登録する必要がほとんどなくなりました。ただし、イベントを手動で登録する必要がある場合は、`AppServiceProvider` で簡単に登録できます。同様に、以前に `AuthServiceProvider` に登録したルート モデル バインディングまたは認証ゲートも、`AppServiceProvider` に登録される可能性があります。

<a name="opt-in-routing"></a>
#### オプトイン API とブロードキャスト ルーティング

`api.php` および `channels.php` ルート ファイルは、多くのアプリケーションでこれらのファイルが必要ないため、デフォルトでは存在しません。代わりに、単純な Artisan コマンドを使用して作成することもできます。

```shell
php artisan install:api

php artisan install:broadcasting
```

<a name="middleware"></a>
#### ミドルウェア

以前は、新しい Laravel アプリケーションには 9 つのミドルウェアが含まれていました。これらのミドルウェアは、リクエストの認証、入力文字列のトリミング、CSRF トークンの検証などのさまざまなタスクを実行しました。

Laravel 11 では、これらのミドルウェアはフレームワーク自体に移動されているため、アプリケーションの構造がかさばることはありません。これらのミドルウェアの動作をカスタマイズするための新しいメソッドがフレームワークに追加されており、アプリケーションの `bootstrap/app.php` ファイルから呼び出すことができます。

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(
        except: ['stripe/*']
    );

    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ])
})
```

すべてのミドルウェアはアプリケーションの `bootstrap/app.php` を介して簡単にカスタマイズできるため、別個の HTTP "カーネル" クラスの必要性がなくなりました。

<a name="scheduling"></a>
#### スケジュール設定

新しい `Schedule` ファサードを使用すると、スケジュールされたタスクをアプリケーションの `routes/console.php` ファイルで直接定義できるようになり、別個のコンソール「カーネル」クラスが不要になります。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->daily();
```

<a name="exception-handling"></a>
#### 例外処理

ルーティングやミドルウェアと同様に、例外処理を個別の例外ハンドラー クラスではなくアプリケーションの `bootstrap/app.php` ファイルからカスタマイズできるようになり、新しい Laravel アプリケーションに含まれるファイル全体の数が削減されます。

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport(MissedFlightException::class);

    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

<a name="base-controller-class"></a>
#### 基本 `Controller` クラス

新しい Laravel アプリケーションに含まれるベース コントローラが簡素化されました。 Laravel の内部 `Controller` クラスは拡張されなくなり、必要に応じてアプリケーションの個々のコントローラに含めることができるため、`AuthorizesRequests` および `ValidatesRequests` トレイトは削除されました。

    <?php

    namespace App\Http\Controllers;

    abstract class Controller
    {
        //
    }

<a name="application-defaults"></a>
#### アプリケーションのデフォルト

デフォルトでは、新しい Laravel アプリケーションはデータベース ストレージに SQLite を使用するほか、Laravel のセッション、キャッシュ、キューに `database` ドライバを使用します。これにより、追加のソフトウェアをインストールしたり、追加のデータベース移行を作成したりすることなく、新しい Laravel アプリケーションを作成した後すぐにアプリケーションの構築を開始できます。

さらに、時間の経過とともに、これらの Laravel サービスの `database` ドライバは、多くのアプリケーション コンテキストで実稼働環境で使用できるほど十分に堅牢になりました。したがって、ローカル アプリケーションと運用アプリケーションの両方に賢明で統一された選択肢を提供します。

<a name="reverb"></a>
### Laravel Reverb

_Laravel Reverb は [ジョー・ディクソン](https://github.com/joedixon)_ によって開発されました。

[Laravel Reverb](https://reverb.laravel.com) は、超高速でスケーラブルなリアルタイム WebSocket 通信を Laravel アプリケーションに直接もたらし、Laravel Echo などの Laravel の既存のイベント ブロードキャスト ツール スイートとのシームレスな統合を提供します。

```shell
php artisan reverb:start
```

さらに、Reverb は Redis のパブリッシュ/サブスクライブ機能を介した水平スケーリングをサポートしており、単一の高需要アプリケーションをサポートする複数のバックエンド Reverb サーバー全体に WebSocket トラフィックを分散できます。

Laravel Reverb の詳細については、完全な [Reverb のドキュメント](/docs/{{version}}/reverb) を参照してください。

<a name="rate-limiting"></a>
### 1 秒あたりのレート制限

_秒あたりのレート制限は、[ティム・マクドナルド](https://github.com/timacdonald)_ によって提供されました。

Laravel は、HTTP リクエストやキューに入れられたジョブのレート リミッターを含む、すべてのレート リミッターに対して「1 秒あたり」のレート制限をサポートするようになりました。以前は、Laravel のレート リミッターは「1 分あたり」の粒度に制限されていました。

```php
RateLimiter::for('invoices', function (Request $request) {
    return Limit::perSecond(1);
});
```

Laravel のレート制限の詳細については、[レート制限に関するドキュメント](/docs/{{version}}/routing#rate-limiting) を確認してください。

<a name="health"></a>
### ヘルスルーティング

_ヘルス ルーティングは [テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

新しい Laravel 11 アプリケーションには、`health` ルーティング ディレクティブが含まれています。これは、サードパーティのアプリケーション健全性監視サービスや Kubernetes などのオーケストレーション システムによって呼び出される単純な健全性チェック エンドポイントを定義するように Laravel に指示します。デフォルトでは、このルートは `/up` で提供されます。

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
)
```

このルートに対して HTTP リクエストが行われると、Laravel は `DiagnosingHealth` イベントも送出し、アプリケーションに関連する追加のヘルスチェックを実行できるようにします。

<a name="encryption"></a>
### 正常な暗号化キーのローテーション

_正常な暗号化キーのローテーションは、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

Laravel はアプリケーションのセッション Cookie を含むすべての Cookie を暗号化するため、基本的に Laravel アプリケーションへのすべてのリクエストは暗号化に依存します。ただし、このため、アプリケーションの暗号化キーをローテーションすると、すべてのユーザーがアプリケーションからログアウトされます。また、以前の暗号鍵で暗号化されたデータは復号できなくなります。

Laravel 11 では、`APP_PREVIOUS_KEYS` 環境変数を使用して、アプリケーションの以前の暗号化キーをカンマ区切りのリストとして定義できます。

値を暗号化するとき、Laravel は常に `APP_KEY` 環境変数内にある「現在の」暗号化キーを使用します。値を復号化するとき、Laravel は最初に現在のキーを試行します。現在のキーを使用した復号化が失敗した場合、Laravel はキーの 1 つで値を復号化できるまで、以前のすべてのキーを試します。

この正常な復号化のアプローチにより、暗号化キーがローテーションされた場合でも、ユーザーはアプリケーションを中断することなく使用し続けることができます。

Laravel での暗号化の詳細については、[暗号化ドキュメント](/docs/{{version}}/encryption) を確認してください。

<a name="automatic-password-rehashing"></a>
### パスワードの自動再ハッシュ

_自動パスワード再ハッシュは、[スティーブン・リース＝カーター](https://github.com/valorin)_ によって提供されました。

Laravel のデフォルトのパスワードハッシュアルゴリズムは bcrypt です。 bcrypt ハッシュの「作業係数」は、`config/hashing.php` 構成ファイルまたは `BCRYPT_ROUNDS` 環境変数を介して調整できます。

通常、CPU / GPU の処理能力が増加するにつれて、bcrypt 作業係数は時間の経過とともに増加する必要があります。アプリケーションの bcrypt 作業係数を増やすと、ユーザーがアプリケーションで認証されるときに、Laravel はユーザーのパスワードを適切かつ自動的に再ハッシュするようになります。

<a name="prompt-validation"></a>
### 即時検証

_プロンプトバリデーターの統合は、[アンドレア・マルコ・サルトーリ](https://github.com/cerbero90)_ によって提供されました。

[Laravelプロンプト](/docs/{{version}}/prompts) は、プレースホルダー テキストや検証などのブラウザーのような機能を備えた、美しくユーザーフレンドリーなフォームをコマンドライン アプリケーションに追加するための PHP パッケージです。

Laravel プロンプトは、クロージャーを介した入力検証をサポートしています。

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

ただし、多くの入力や複雑な検証シナリオを扱う場合、これは面倒になる可能性があります。したがって、Laravel 11 では、プロンプト入力を検証するときに Laravel の [validator](/docs/{{version}}/validation) の機能を最大限に活用できます。

```php
$name = text('What is your name?', validate: [
    'name' => 'required|min:3|max:255',
]);
```

<a name="queue-interaction-testing"></a>
### キュー相互作用のテスト

_キューの相互作用テストは [テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

以前は、キューに入れられたジョブが解放、削除されたか、手動で失敗したかをテストしようとするのは面倒で、カスタム キューのフェイクとスタブを定義する必要がありました。ただし、Laravel 11 では、`withFakeQueueInteractions` メソッドを使用して、これらのキューの相互作用を簡単にテストできます。

```php
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
```

キューに入れられたジョブのテストの詳細については、[キューのドキュメント](/docs/{{version}}/queues#testing) を確認してください。

<a name="new-artisan-commands"></a>
### 新しいArtisan コマンド

_クラス作成Artisan コマンドは、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

新しい Artisan コマンドが追加され、クラス、列挙型、インターフェイス、特性を迅速に作成できるようになりました。

```shell
php artisan make:class
php artisan make:enum
php artisan make:interface
php artisan make:trait
```

<a name="model-cast-improvements"></a>
### モデルキャストの改善

_モデル キャストの改善は、[ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

Laravel 11 では、プロパティの代わりにメソッドを使用したモデルのキャストの定義がサポートされています。これにより、特に引数付きのキャストを使用する場合に、合理的で流暢なキャスト定義が可能になります。

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => AsCollection::using(OptionCollection::class),
                      // AsEncryptedCollection::using(OptionCollection::class),
                      // AsEnumArrayObject::using(OptionEnum::class),
                      // AsEnumCollection::using(OptionEnum::class),
        ];
    }

属性キャストの詳細については、[Eloquent ドキュメント](/docs/{{version}}/eloquent-mutators#attribute-casting) を参照してください。

<a name="the-once-function"></a>
### `once`関数

_`once` ヘルパは、[テイラー・オトウェル](https://github.com/taylorotwell)_ および _[ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

`once` ヘルパ関数は、指定されたコールバックを実行し、リクエストの間、結果をメモリにキャッシュします。同じコールバックを使用した後続の `once` 関数の呼び出しでは、以前にキャッシュされた結果が返されます。

    function random(): int
    {
        return once(function () {
            return random_int(1, 1000);
        });
    }

    random(); // 123
    random(); // 123 (cached result)
    random(); // 123 (cached result)

`once` ヘルパの詳細については、[ヘルパのドキュメント](/docs/{{version}}/helpers#method-once) を確認してください。

<a name="database-performance"></a>
### インメモリデータベースを使用したテスト時のパフォーマンスの向上

_メモリ内データベースのテスト パフォーマンスの向上は、[アンダース・ジェンボ](https://github.com/AJenbo) によるものです_

Laravel 11 では、テスト中に `:memory:` SQLite データベースを使用すると速度が大幅に向上します。これを達成するために、Laravel は PHP の PDO オブジェクトへの参照を維持し、それを接続全体で再利用することで、多くの場合、合計テスト実行時間を半分に短縮します。

<a name="mariadb"></a>
### MariaDB のサポートの改善

_MariaDB のサポートの改善は、[ヨナス・シュタウデンマイヤー](https://github.com/staudenmeir) および [ジュリアス・キークブッシュ](https://github.com/Jubeki) によって提供されました_

Laravel 11 には、MariaDB のサポートが改善されました。以前の Laravel リリースでは、Laravel の MySQL ドライバ経由で MariaDB を使用できました。ただし、Laravel 11 には、このデータベース システムにより良いデフォルトを提供する専用の MariaDB ドライバが含まれています。

Laravel のデータベースドライバの詳細については、[データベースのドキュメント](/docs/{{version}}/database) を確認してください。

<a name="inspecting-database"></a>
### データベースの検査とスキーマ操作の改善

_スキーマ操作とデータベース検査の改善は、[ハーフェズ・ディバンダリ](https://github.com/hafezdivandari) の貢献によるものです_

Laravel 11 では、ネイティブの変更、名前変更、列の削除など、追加のデータベース スキーマ操作および検査方法が提供されます。さらに、テーブル、ビュー、列、インデックス、外部キーを操作するための高度な空間タイプ、デフォルト以外のスキーマ名、およびネイティブ スキーマ メソッドが提供されます。

    use Illuminate\Support\Facades\Schema;

    $tables = Schema::getTables();
    $views = Schema::getViews();
    $columns = Schema::getColumns('users');
    $indexes = Schema::getIndexes('users');
    $foreignKeys = Schema::getForeignKeys('users');

