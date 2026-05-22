# リリースノート (Release Notes)

- [バージョン管理スキーム](#versioning-scheme)
- [サポートポリシー](#support-policy)
- [Laravel9](#laravel-9)

<a name="versioning-scheme"></a>
## バージョン管理スキーム (Versioning Scheme)

Laravel とその他のファーストパーティ パッケージは [セマンティック バージョニング](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~2 月) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^9.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
#### 名前付き引数

[名前付き引数](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
## サポートポリシー (Support Policy)

すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [Laravelによってサポートされています](/docs/{{version}}/database#introduction) を確認してください。

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2～8.0 | 2019年9月3日 | 2022 年 1 月 25 日 | 2022 年 9 月 6 日 |
| 7 | 7.2～8.0 | 2020年3月3日 | 2020年10月6日 | 2021年3月3日 |
| 8 | 7.3 - 8.1 | 2020年9月8日 | 2022 年 7 月 26 日 | 2023 年 1 月 24 日 |
| 9 | 8.0～8.2 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |

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

<a name="laravel-9"></a>
## Laravel9 (Laravel 9)

ご存知かもしれませんが、Laravel 8 のリリースにより、Laravel は年次リリースに移行しました。以前は、メジャー バージョンは 6 か月ごとにリリースされていました。この移行は、コミュニティのメンテナンスの負担を軽減し、開発チームが重大な変更を導入することなく、驚くべき強力な新機能をリリースできるようにすることを目的としています。したがって、私たちは下位互換性を損なうことなく、並列テストのサポート、改良された Breeze スターター キット、HTTP クライアントの改善、さらには「多くのうちの 1 つを持っている」などの新しい Eloquent 関係タイプなど、さまざまな堅牢な機能を Laravel 8 に出荷しました。

したがって、現在のリリース中に優れた新機能をリリースするというこの取り組みにより、将来の「メジャー」リリースは主に上流の依存関係のアップグレードなどの「メンテナンス」タスクに使用されることになる可能性が高く、これはこれらのリリース ノートで確認できます。

Laravel 9は、Symfony 6.0コンポーネント、Symfony Mailer、Flysystem 3.0のサポート、改良された`route:list`出力、Laravel Scoutデータベースドライバ、新しいEloquentアクセサー/ミューテタ構文、Enumsによる暗黙的なルートバインディング、その他のさまざまなバグ修正と使いやすさの向上により、Laravel 8.xで行われた改良を継続しています。

<a name="php-8"></a>
### PHP8.0

Laravel 9.x には、最小 PHP バージョン 8.0 が必要です。

<a name="symfony-mailer"></a>
### Symfony Mailer

_Symfony Mailer のサポートは、[ドリス・ヴィンツ](https://github.com/driesvints)_、[ジェームズ・ブルックス](https://github.com/jbrooksuk)、および [ジュリアス・キークブッシュ](https://github.com/Jubeki) によって提供されました。

Laravel の以前のリリースでは、送信電子メールの送信に [迅速なメーラー](https://swiftmailer.symfony.com/docs/introduction.html) ライブラリを利用していました。ただし、そのライブラリは現在は保守されておらず、Symfony Mailer に引き継がれています。

アプリケーションが Symfony Mailer と互換性があることを確認する方法の詳細については、[アップグレードガイド](/docs/{{version}}/upgrade#symfony-mailer) を参照してください。

<a name="flysystem-3"></a>
### フライシステム 3.x

_Flysystem 3.x のサポートは、[ドリス・ヴィンツ](https://github.com/driesvints)_ によって提供されました。

Laravel 9.x は、アップストリームの Flysystem 依存関係を Flysystem 3.x にアップグレードします。 Flysystem は、`Storage` ファサードによって提供されるすべてのファイルシステム対話を強化します。

アプリケーションが Flysystem 3.x と互換性があることを確認する方法の詳細については、[アップグレードガイド](/docs/{{version}}/upgrade#flysystem-3) を参照してください。

<a name="eloquent-accessors-and-mutators"></a>
### 改良された Eloquent アクセサー / ミューテタ

_改善された Eloquent アクセサー / ミューテタは、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

Laravel 9.x は、Eloquent [アクセサとミューテタ](/docs/{{version}}/eloquent-mutators#accessors-and-mutators) を定義する新しい方法を提供します。 Laravel の以前のリリースでは、アクセサーとミューテタを定義する唯一の方法は、次のようにモデル上でプレフィックス付きメソッドを定義することでした。

```php
public function getNameAttribute($value)
{
    return strtoupper($value);
}

public function setNameAttribute($value)
{
    $this->attributes['name'] = $value;
}
```

ただし、Laravel 9.x では、`Illuminate\Database\Eloquent\Casts\Attribute` の戻り値の型をタイプヒントすることで、単一のプレフィックスのないメソッドを使用してアクセサーとミューテタを定義できます。

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

public function name(): Attribute
{
    return new Attribute(
        get: fn ($value) => strtoupper($value),
        set: fn ($value) => $value,
    );
}
```

さらに、アクセサーを定義するこの新しいアプローチは、[カスタムキャストクラス](/docs/{{version}}/eloquent-mutators#custom-casts) と同様に、属性によって返されるオブジェクト値をキャッシュします。

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

public function address(): Attribute
{
    return new Attribute(
        get: fn ($value, $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```

<a name="enum-casting"></a>
### Enum Eloquent 属性のキャスト

> **警告**
> Enum キャストは PHP 8.1 以降でのみ使用できます。

_Enum キャストは [モハメド・サイード](https://github.com/themsaid)_ によって提供されました。

Eloquent では、属性値を PHP [「バックアップされた」列挙型](https://www.php.net/manual/en/language.enumerations.backed.php) にキャストできるようになりました。これを実現するには、モデルの `$casts` プロパティ配列にキャストする属性と列挙型を指定します。

    use App\Enums\ServerStatus;

    /**
     * The attributes that should be cast.
     *
     * @var array
     */
    protected $casts = [
        'status' => ServerStatus::class,
    ];

モデルでキャストを定義すると、指定した属性は、属性を操作するときに列挙型との間で自動的にキャストされます。

    if ($server->status == ServerStatus::Provisioned) {
        $server->status = ServerStatus::Ready;

        $server->save();
    }

<a name="implicit-route-bindings-with-enums"></a>
### 列挙型を使用した暗黙的なルート バインディング

_Implicit Enum バインディングは [ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

PHP 8.1 では、[Enums](https://www.php.net/manual/en/language.enumerations.backed.php) のサポートが導入されています。 Laravel 9.x では、ルート定義で Enum をタイプヒントする機能が導入されており、Laravel は、そのルートセグメントが URI 内の有効な Enum 値である場合にのみルートを呼び出します。それ以外の場合は、HTTP 404 応答が自動的に返されます。たとえば、次の列挙型があるとします。

```php
enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

`{category}` ルート セグメントが `fruits` または `people` の場合にのみ呼び出されるルートを定義できます。それ以外の場合は、HTTP 404 応答が返されます。

```php
Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="forced-scoping-of-route-bindings"></a>
### ルートバインディングの強制スコープ設定

_強制スコープ バインディングは [クラウディオ・デッカー](https://github.com/claudiodekker)_ によって提供されました。

Laravel の以前のリリースでは、ルート定義で 2 番目の Eloquent モデルのスコープを設定し、それが以前の Eloquent モデルの子である必要がある場合があります。たとえば、特定のユーザーのスラッグによってブログ投稿を取得する次のルート定義について考えてみましょう。

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
        return $post;
    });

カスタムのキー付き暗黙的バインディングをネストされたルートパラメーターとして使用する場合、Laravel は、親の関係名を推測する規則を使用して、親によってネストされたモデルを取得するためにクエリのスコープを自動的に設定します。ただし、この動作は、以前は子ルート バインディングにカスタム キーが使用されていた場合にのみ Laravel でサポートされていました。

ただし、Laravel 9.x では、カスタムキーが提供されていない場合でも、「子」バインディングをスコープするように Laravel に指示できるようになりました。これを行うには、ルートを定義するときに `scopeBindings` メソッドを呼び出します。

    use App\Models\Post;
    use App\Models\User;

    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    })->scopeBindings();

または、ルート定義のグループ全体にスコープ付きバインディングを使用するように指示することもできます。

    Route::scopeBindings()->group(function () {
        Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
            return $post;
        });
    });

<a name="controller-route-groups"></a>
### コントローラルートグループ

_ルート グループの改善は、[ルーク・ダウニング](https://github.com/lukeraymonddowning)_ によって提供されました。

これで、`controller` メソッドを使用して、グループ内のすべてのルートに共通のコントローラを定義できるようになりました。次に、ルートを定義するときに、ルートが呼び出すコントローラ メソッドを指定するだけで済みます。

    use App\Http\Controllers\OrderController;

    Route::controller(OrderController::class)->group(function () {
        Route::get('/orders/{id}', 'show');
        Route::post('/orders', 'store');
    });

<a name="full-text"></a>
### 全文インデックス / Where 句

_全文インデックスと「where」句は、[テイラー・オトウェル](https://github.com/taylorotwell) および [ドリス・ヴィンツ](https://github.com/driesvints)_ によって提供されました。

MySQL または PostgreSQL を使用する場合、`fullText` メソッドを列定義に追加して、フルテキスト インデックスを生成できるようになりました。

    $table->text('bio')->fullText();

さらに、`whereFullText` メソッドと `orWhereFullText` メソッドを使用して、[全文インデックス](/docs/{{version}}/migrations#available-index-types) を持つ列のクエリにフルテキストの "where" 句を追加することもできます。これらのメソッドは、Laravel によって基礎となるデータベース システムに適した SQL に変換されます。たとえば、MySQL を利用するアプリケーションに対して `MATCH AGAINST` 句が生成されます。

    $users = DB::table('users')
               ->whereFullText('bio', 'web developer')
               ->get();

<a name="laravel-scout-database-engine"></a>
### Laravel Scout データベース エンジン

_Laravel Scout データベース エンジンは、[テイラー・オトウェル](https://github.com/taylorotwell) および [ドリス・ヴィンツ](https://github.com/driesvints)_ によって提供されました。

アプリケーションが小規模から中規模のデータベースとやり取りする場合、またはワークロードが軽い場合は、Algolia や Meil​​iSearch などの専用の検索サービスの代わりに Scout の「データベース」エンジンを使用できるようになります。データベース エンジンは、既存のデータベースからの結果をフィルタリングするときに「where like」句と全文インデックスを使用して、クエリに該当する検索結果を決定します。

Scout データベース エンジンの詳細については、[Scoutの文書](/docs/{{version}}/scout) を参照してください。

<a name="rendering-inline-blade-templates"></a>
### インラインBlade テンプレートのレンダリング

_インライン Blade テンプレートのレンダリングは、[ジェイソン・ベッグス](https://github.com/jasonlbeggs) によって提供されました。インライン Blade コンポーネントのレンダリングは、[トビー・ゼルナー](https://github.com/tobyzerner)_ によって提供されました。

場合によっては、生の Blade テンプレート文字列を有効な HTML に変換する必要があるかもしれません。これは、`Blade` ファサードによって提供される `render` メソッドを使用して実行できます。 `render` メソッドは、Blade テンプレート文字列と、テンプレートに提供するオプションのデータ配列を受け入れます。

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

同様に、`renderComponent` メソッドを使用して、コンポーネント インスタンスをメソッドに渡すことで、特定のクラス コンポーネントをレンダリングできます。

```php
use App\View\Components\HelloComponent;

return Blade::renderComponent(new HelloComponent('Julian Bashir'));
```

<a name="slot-name-shortcut"></a>
### スロット名のショートカット

_スロット名のショートカットは [カレブ・ポルツィオ](https://github.com/calebporzio) によって提供されました。_

Laravel の以前のリリースでは、スロット名は `x-slot` タグの `name` 属性を使用して提供されていました。

```blade
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

ただし、Laravel 9.x 以降では、便利で短い構文を使用してスロット名を指定できるようになりました。

```xml
<x-slot:title>
    Server Error
</x-slot>
```

<a name="checked-selected-blade-directives"></a>
### チェック/選択されたBlade ディレクティブ

_チェックおよび選択された Blade ディレクティブは、[アッシュ・アレン](https://github.com/ash-jc-allen) および [テイラー・オトウェル](https://github.com/taylorotwell)_ によって寄稿されました。

便宜上、`@checked` ディレクティブを使用して、特定の HTML チェックボックス入力が「チェックされている」かどうかを簡単に示すことができるようになりました。このディレクティブは、指定された条件が `true` と評価される場合、`checked` をエコーし​​ます。

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

同様に、`@selected` ディレクティブを使用して、特定の選択オプションを「選択」する必要があるかどうかを示すことができます。

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

<a name="bootstrap-5-pagination-views"></a>
### ブートストラップ 5 ページネーション ビュー

_Bootstrap 5 ページネーション ビューは、[ジャレッド・ルイス](https://github.com/jrd-lewis)_ によって寄稿されました。

Laravel には、[ブートストラップ 5](https://getbootstrap.com/) を使用して構築されたページ分割ビューが含まれるようになりました。デフォルトの Tailwind ビューの代わりにこれらのビューを使用するには、`App\Providers\AppServiceProvider` クラスの `boot` メソッド内でページネータの `useBootstrapFive` メソッドを呼び出すことができます。

    use Illuminate\Pagination\Paginator;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Paginator::useBootstrapFive();
    }

<a name="improved-validation-of-nested-array-data"></a>
### ネストされた配列データの検証の改善

_ネストされた配列入力の検証の改善は、[スティーブ・バウマン](https://github.com/stevebauman)_ によって提供されました。

属性に検証ルールを割り当てるときに、特定のネストされた配列要素の値にアクセスする必要がある場合があります。 `Rule::forEach` メソッドを使用してこれを実行できるようになりました。 `forEach` メソッドは、検証中の配列属性の反復ごとに呼び出されるクロージャを受け入れ、属性の値と明示的な完全に展開された属性名を受け取ります。クロージャは、配列要素に割り当てるルールの配列を返す必要があります。

    use App\Rules\HasPermission;
    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    $validator = Validator::make($request->all(), [
        'companies.*.id' => Rule::forEach(function ($value, $attribute) {
            return [
                Rule::exists(Company::class, 'id'),
                new HasPermission('manage-company', $value),
            ];
        }),
    ]);

<a name="laravel-breeze-api"></a>
### Laravel Breeze API と Next.js

_Laravel Breeze API スキャフォールディングと Next.js スターター キットは、[テイラー・オトウェル](https://github.com/taylorotwell) および [ミゲル・ピエドラフィタ](https://twitter.com/m1guelpf)_ によって提供されました。

[Laravel Breeze](/docs/{{version}}/starter-kits#breeze-and-next) スターター キットには、「API」スキャフォールディング モードと無料の [Next.js](https://nextjs.org) [フロントエンドの実装](https://github.com/laravel/breeze-next) が含まれています。このスターター キット スキャフォールディングは、バックエンドとして機能する Laravel アプリケーション (JavaScript フロントエンド用の Laravel Sanctum 認証済み API) をすぐに開始するために使用できます。

<a name="exception-page"></a>
### 点火例外ページの改善

_Ignition は [Spatie](https://spatie.be/) によって開発されました。_

Spatie が作成したオープンソースの例外デバッグ ページである Ignition は、根本から再設計されました。新しく改良された Ignition は Laravel 9.x に同梱されており、ライト/ダーク テーマ、カスタマイズ可能な「エディタで開く」機能などが含まれています。

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/483853/149235404-f7caba56-ebdf-499e-9883-cac5d5610369.png"/>
</p>

<a name="improved-route-list"></a>
### `route:list` CLI 出力の改善

_改良された `route:list` CLI 出力は、[ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

`route:list` CLI 出力は Laravel 9.x リリースで大幅に改善され、ルート定義を探索するときに美しく新しいエクスペリエンスを提供します。

<p align="center">
<img src="https://user-images.githubusercontent.com/5457236/148321982-38c8b869-f188-4f42-a3cc-a03451d5216c.png"/>
</p>

<a name="test-coverage-support-on-artisan-test-Command"></a>
### Artisan `test` コマンドを使用したカバレッジのテスト

_Artisan `test` コマンド使用時のテスト カバレッジは、[ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

Artisan `test` コマンドに、テストがアプリケーションに提供するコード カバレッジの量を調査するために使用できる新しい `--coverage` オプションが追加されました。

```shell
php artisan test --coverage
```

テスト カバレッジの結果は、CLI 出力内に直接表示されます。

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>

さらに、テスト カバレッジ パーセンテージが満たさなければならない最小しきい値を指定したい場合は、`--min` オプションを使用できます。指定された最小しきい値が満たされていない場合、テスト スイートは失敗します。

```shell
php artisan test --coverage --min=80.3
```

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/149989853-a29a7629-2bfa-4bf3-bbf7-cdba339ec157.png"/>
</p>

<a name="soketi-echo-server"></a>
### Soketi Echo サーバー

_Soketi Echo サーバーは [アレックス・レノキ](https://github.com/rennokki)_ によって開発されました。

Laravel 9.x に限定されたものではありませんが、Laravel は最近、Node.js 用に作成された [Laravel Echo](/docs/{{version}}/broadcasting) 互換の Web ソケット サーバーである Soketi のドキュメントを支援しました。 Soketi は、独自の Web Socket サーバーを管理することを好むアプリケーション向けに、Pusher や Ably に代わる優れたオープンソースの代替手段を提供します。

Soketi の使用方法の詳細については、[放送ドキュメント](/docs/{{version}}/broadcasting) および [ソケティのドキュメント](https://docs.soketi.app/) を参照してください。

<a name="improved-collections-ide-support"></a>
### コレクション IDE サポートの改善

_コレクション IDE サポートの改善は、[ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

Laravel 9.x では、改良された「汎用」スタイル型定義がコレクションコンポーネントに追加され、IDE と静的分析のサポートが改善されています。 [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections) などの IDE や [PHPStan](https://phpstan.org) などの静的分析ツールは、Laravel コレクションをネイティブに理解できるようになりました。

<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/151783350-ed301660-1e09-44c1-b549-85c6db3f078d.gif"/>
</p>

<a name="new-helpers"></a>
### 新しいヘルパ

Laravel 9.x では、独自のアプリケーションで使用できる 2 つの新しい便利なヘルパ関数が導入されています。

<a name="new-helpers-str"></a>
#### `str`

`str` 関数は、指定された文字列の新しい `Illuminate\Support\Stringable` インスタンスを返します。この関数は、`Str::of` メソッドと同等です。

    $string = str('Taylor')->append(' Otwell');

    // 'Taylor Otwell'

`str` 関数に引数が指定されていない場合、関数は `Illuminate\Support\Str` のインスタンスを返します。

    $snake = str()->snake('LaravelFramework');

    // 'laravel_framework'

<a name="new-helpers-to-route"></a>
#### `to_route`

`to_route` 関数は、指定された名前付きルートのリダイレクト HTTP 応答を生成し、ルートとコントローラから名前付きルートにリダイレクトする表現力豊かな方法を提供します。

    return to_route('users.show', ['user' => 1]);

必要に応じて、リダイレクトに割り当てる HTTP ステータス コードと追加の応答ヘッダーを、to_route メソッドの 3 番目と 4 番目の引数として渡すことができます。

    return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);

