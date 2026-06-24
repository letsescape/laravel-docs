<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 9](#laravel-9)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~February), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel とその他のファーストパーティ パッケージは [Semantic Versioning](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~2 月) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^9.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^9.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/9.x/database#introduction). -->
すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [supported by Laravel](/docs/9.x/database#introduction) を確認してください。

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2～8.0 | 2019年9月3日 | 2022 年 1 月 25 日 | 2022 年 9 月 6 日 |
| 7 | 7.2～8.0 | 2020年3月3日 | 2020年10月6日 | 2021年3月3日 |
| 8 | 7.3 - 8.1 | 2020年9月8日 | 2022 年 7 月 26 日 | 2023 年 1 月 24 日 |
| 9 | 8.0～8.2 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |

<!--
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
-->
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

<!-- (*) Supported PHP versions -->
(*) サポートされている PHP バージョン

<a name="laravel-9"></a>
<!-- ## Laravel 9 -->
## Laravel 9

<!-- As you may know, Laravel transitioned to yearly releases with the release of Laravel 8. Previously, major versions were released every 6 months. This transition is intended to ease the maintenance burden on the community and challenge our development team to ship amazing, powerful new features without introducing breaking changes. Therefore, we have shipped a variety of robust features to Laravel 8 without breaking backwards compatibility, such as parallel testing support, improved Breeze starter kits, HTTP client improvements, and even new Eloquent relationship types such as "has one of many". -->
ご存知かもしれませんが、Laravel 8 のリリースにより、Laravel は年次リリースに移行しました。以前は、メジャー バージョンは 6 か月ごとにリリースされていました。この移行は、コミュニティのメンテナンスの負担を軽減し、開発チームが重大な変更を導入することなく、驚くべき強力な新機能をリリースできるようにすることを目的としています。したがって、私たちは下位互換性を損なうことなく、並列テストのサポート、改良された Breeze スターター キット、HTTP クライアントの改善、さらには「多くのうちの 1 つを持っている」などの新しい Eloquent 関係タイプなど、さまざまな堅牢な機能を Laravel 8 に出荷しました。

<!-- Therefore, this commitment to ship great new features during the current release will likely lead to future "major" releases being primarily used for "maintenance" tasks such as upgrading upstream dependencies, which can be seen in these release notes. -->
したがって、現在のリリース中に優れた新機能をリリースするというこの取り組みにより、将来の「メジャー」リリースは主に上流の依存関係のアップグレードなどの「メンテナンス」タスクに使用されることになる可能性が高く、これはこれらのリリース ノートで確認できます。

<!-- Laravel 9 continues the improvements made in Laravel 8.x by introducing support for Symfony 6.0 components, Symfony Mailer, Flysystem 3.0, improved `route:list` output, a Laravel Scout database driver, new Eloquent accessor / mutator syntax, implicit route bindings via Enums, and a variety of other bug fixes and usability improvements. -->
Laravel 9は、Symfony 6.0コンポーネント、Symfony Mailer、Flysystem 3.0のサポート、改良された`route:list`出力、Laravel Scoutデータベースドライバ、新しいEloquentaccessor/mutator構文、Enumsによる暗黙的なルートバインディング、その他のさまざまなバグ修正と使いやすさの向上により、Laravel 8.xで行われた改良を継続しています。

<a name="php-8"></a>
<!-- ### PHP 8.0 -->
### PHP 8.0

<!-- Laravel 9.x requires a minimum PHP version of 8.0. -->
Laravel 9.x には、最小 PHP バージョン 8.0 が必要です。

<a name="symfony-mailer"></a>
<!-- ### Symfony Mailer -->
### Symfony Mailer

<!-- _Symfony Mailer support was contributed by [Dries Vints](https://github.com/driesvints)_, [James Brooks](https://github.com/jbrooksuk), and [Julius Kiekbusch](https://github.com/Jubeki). -->
_Symfony Mailer のサポートは、[Dries Vints](https://github.com/driesvints)_、[James Brooks](https://github.com/jbrooksuk)、および [Julius Kiekbusch](https://github.com/Jubeki) によって提供されました。

<!-- Previous releases of Laravel utilized the [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html) library to send outgoing email. However, that library is no longer maintained and has been succeeded by Symfony Mailer. -->
Laravel の以前のリリースでは、送信電子メールの送信に [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html) ライブラリを利用していました。ただし、そのライブラリは現在は保守されておらず、Symfony Mailer に引き継がれています。

<!-- Please review the [upgrade guide](/docs/9.x/upgrade#symfony-mailer) to learn more about ensuring your application is compatible with Symfony Mailer. -->
アプリケーションが Symfony Mailer と互換性があることを確認する方法の詳細については、[upgrade guide](/docs/9.x/upgrade#symfony-mailer) を参照してください。

<a name="flysystem-3"></a>
<!-- ### Flysystem 3.x -->
### Flysystem 3.x

<!-- _Flysystem 3.x support was contributed by [Dries Vints](https://github.com/driesvints)_. -->
_Flysystem 3.x のサポートは、[Dries Vints](https://github.com/driesvints)_ によって提供されました。

<!-- Laravel 9.x upgrades our upstream Flysystem dependency to Flysystem 3.x. Flysystem powers all of filesystem interactions offered by the `Storage` facade. -->
Laravel 9.x は、アップストリームの Flysystem 依存関係を Flysystem 3.x にアップグレードします。 Flysystem は、`Storage` ファサードによって提供されるすべてのファイルシステム対話を強化します。

<!-- Please review the [upgrade guide](/docs/9.x/upgrade#flysystem-3) to learn more about ensuring your application is compatible with Flysystem 3.x. -->
アプリケーションが Flysystem 3.x と互換性があることを確認する方法の詳細については、[upgrade guide](/docs/9.x/upgrade#flysystem-3) を参照してください。

<a name="eloquent-accessors-and-mutators"></a>
<!-- ### Improved Eloquent Accessors / Mutators -->
### Improved Eloquent Accessors / Mutators

<!-- _Improved Eloquent accessors / mutators was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_改善された Eloquent accessor / mutatorは、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Laravel 9.x offers a new way to define Eloquent [accessors and mutators](/docs/9.x/eloquent-mutators#accessors-and-mutators). In previous releases of Laravel, the only way to define accessors and mutators was by defining prefixed methods on your model like so: -->
Laravel 9.x は、Eloquent [accessors and mutators](/docs/9.x/eloquent-mutators#accessors-and-mutators) を定義する新しい方法を提供します。 Laravel の以前のリリースでは、accessorとmutatorを定義する唯一の方法は、次のようにモデル上でプレフィックス付きメソッドを定義することでした。

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

<!-- However, in Laravel 9.x you may define an accessor and mutator using a single, non-prefixed method by type-hinting a return type of `Illuminate\Database\Eloquent\Casts\Attribute`: -->
ただし、Laravel 9.x では、`Illuminate\Database\Eloquent\Casts\Attribute` の戻り値の型をタイプヒントすることで、単一のプレフィックスのないメソッドを使用してaccessorとmutatorを定義できます。

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

<!-- In addition, this new approach to defining accessors will cache object values that are returned by the attribute, just like [custom cast classes](/docs/9.x/eloquent-mutators#custom-casts): -->
さらに、accessorを定義するこの新しいアプローチは、[custom cast classes](/docs/9.x/eloquent-mutators#custom-casts) と同様に、属性によって返されるオブジェクト値をキャッシュします。

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
<!-- ### Enum Eloquent Attribute Casting -->
### Enum Eloquent Attribute Casting

> [!WARNING]
> Enum castは PHP 8.1 以降でのみ使用できます。

<!-- _Enum casting was contributed by [Mohamed Said](https://github.com/themsaid)_. -->
_Enum castは [Mohamed Said](https://github.com/themsaid)_ によって提供されました。

<!-- Eloquent now allows you to cast your attribute values to PHP ["backed" Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `$casts` property array: -->
Eloquent では、属性値を PHP ["backed" Enums](https://www.php.net/manual/en/language.enumerations.backed.php) にcastできるようになりました。これを実現するには、モデルの `$casts` プロパティ配列にcastする属性と列挙型を指定します。

```
use App\Enums\ServerStatus;

/**
 * The attributes that should be cast.
 *
 * @var array
 */
protected $casts = [
    'status' => ServerStatus::class,
];
```

<!-- Once you have defined the cast on your model, the specified attribute will be automatically cast to and from an enum when you interact with the attribute: -->
モデルでcastを定義すると、指定した属性は、属性を操作するときに列挙型との間で自動的にcastされます。

```
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```

<a name="implicit-route-bindings-with-enums"></a>
<!-- ### Implicit Route Bindings With Enums -->
### Implicit Route Bindings With Enums

<!-- _Implicit Enum bindings was contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_Implicit Enum バインディングは [Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- PHP 8.1 introduces support for [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). Laravel 9.x introduces the ability to type-hint an Enum on your route definition and Laravel will only invoke the route if that route segment is a valid Enum value in the URI. Otherwise, an HTTP 404 response will be returned automatically. For example, given the following Enum: -->
PHP 8.1 では、[Enums](https://www.php.net/manual/en/language.enumerations.backed.php) のサポートが導入されています。 Laravel 9.x では、ルート定義で Enum をタイプヒントする機能が導入されており、Laravel は、そのルートセグメントが URI 内の有効な Enum 値である場合にのみルートを呼び出します。それ以外の場合は、HTTP 404 応答が自動的に返されます。たとえば、次の列挙型があるとします。

```php
enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

<!-- You may define a route that will only be invoked if the `{category}` route segment is `fruits` or `people`. Otherwise, an HTTP 404 response will be returned: -->
`{category}` ルート セグメントが `fruits` または `people` の場合にのみ呼び出されるルートを定義できます。それ以外の場合は、HTTP 404 応答が返されます。

```php
Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="forced-scoping-of-route-bindings"></a>
<!-- ### Forced Scoping Of Route Bindings -->
### Forced Scoping Of Route Bindings

<!-- _Forced scoped bindings was contributed by [Claudio Dekker](https://github.com/claudiodekker)_. -->
_強制スコープ バインディングは [Claudio Dekker](https://github.com/claudiodekker)_ によって提供されました。

<!-- In previous releases of Laravel, you may wish to scope the second Eloquent model in a route definition such that it must be a child of the previous Eloquent model. For example, consider this route definition that retrieves a blog post by slug for a specific user: -->
Laravel の以前のリリースでは、ルート定義で 2 番目の Eloquent モデルのスコープを設定し、それが以前の Eloquent モデルの子である必要がある場合があります。たとえば、特定のユーザーのスラッグによってブログ投稿を取得する次のルート定義について考えてみましょう。

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. However, this behavior was only previously supported by Laravel when a custom key was used for the child route binding. -->
カスタムのキー付き暗黙的バインディングをネストされたルートパラメーターとして使用する場合、Laravel は、親の関係名を推測する規則を使用して、親によってネストされたモデルを取得するためにクエリのスコープを自動的に設定します。ただし、この動作は、以前は子ルート バインディングにカスタム キーが使用されていた場合にのみ Laravel でサポートされていました。

<!-- However, in Laravel 9.x, you may now instruct Laravel to scope "child" bindings even when a custom key is not provided. To do so, you may invoke the `scopeBindings` method when defining your route: -->
ただし、Laravel 9.x では、カスタムキーが提供されていない場合でも、「子」バインディングをスコープするように Laravel に指示できるようになりました。これを行うには、ルートを定義するときに `scopeBindings` メソッドを呼び出します。

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

<!-- Or, you may instruct an entire group of route definitions to use scoped bindings: -->
または、ルート定義のグループ全体にスコープ付きバインディングを使用するように指示することもできます。

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

<a name="controller-route-groups"></a>
<!-- ### Controller Route Groups -->
### Controller Route Groups

<!-- _Route group improvements were contributed by [Luke Downing](https://github.com/lukeraymonddowning)_. -->
_ルート グループの改善は、[Luke Downing](https://github.com/lukeraymonddowning)_ によって提供されました。

<!-- You may now use the `controller` method to define the common controller for all of the routes within the group. Then, when defining the routes, you only need to provide the controller method that they invoke: -->
これで、`controller` メソッドを使用して、グループ内のすべてのルートに共通のコントローラを定義できるようになりました。次に、ルートを定義するときに、ルートが呼び出すコントローラ メソッドを指定するだけで済みます。

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="full-text"></a>
<!-- ### Full Text Indexes / Where Clauses -->
### Full Text Indexes / Where Clauses

<!-- _Full text indexes and "where" clauses were contributed by [Taylor Otwell](https://github.com/taylorotwell) and [Dries Vints](https://github.com/driesvints)_. -->
_全文インデックスと「where」句は、[Taylor Otwell](https://github.com/taylorotwell) および [Dries Vints](https://github.com/driesvints)_ によって提供されました。

<!-- When using MySQL or PostgreSQL, the `fullText` method may now be added to column definitions to generate full text indexes: -->
MySQL または PostgreSQL を使用する場合、`fullText` メソッドを列定義に追加して、フルテキスト インデックスを生成できるようになりました。

```
$table->text('bio')->fullText();
```

<!-- In addition, the `whereFullText` and `orWhereFullText` methods may be used to add full text "where" clauses to a query for columns that have [full text indexes](/docs/9.x/migrations#available-index-types). These methods will be transformed into the appropriate SQL for the underlying database system by Laravel. For example, a `MATCH AGAINST` clause will be generated for applications utilizing MySQL: -->
さらに、`whereFullText` メソッドと `orWhereFullText` メソッドを使用して、[full text indexes](/docs/9.x/migrations#available-index-types) を持つ列のクエリにフルテキストの "where" 句を追加することもできます。これらのメソッドは、Laravel によって基礎となるデータベース システムに適した SQL に変換されます。たとえば、MySQL を利用するアプリケーションに対して `MATCH AGAINST` 句が生成されます。

```
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="laravel-scout-database-engine"></a>
<!-- ### Laravel Scout Database Engine -->
### Laravel Scout Database Engine

<!-- _The Laravel Scout database engine was contributed by [Taylor Otwell](https://github.com/taylorotwell) and [Dries Vints](https://github.com/driesvints)_. -->
_Laravel Scout データベース エンジンは、[Taylor Otwell](https://github.com/taylorotwell) および [Dries Vints](https://github.com/driesvints)_ によって提供されました。

<!-- If your application interacts with small to medium sized databases or has a light workload, you may now use Scout's "database" engine instead of a dedicated search service such as Algolia or MeiliSearch. The database engine will use "where like" clauses and full text indexes when filtering results from your existing database to determine the applicable search results for your query. -->
アプリケーションが小規模から中規模のデータベースとやり取りする場合、またはワークロードが軽い場合は、Algolia や Meil​​iSearch などの専用の検索サービスの代わりに Scout の「データベース」エンジンを使用できるようになります。データベース エンジンは、既存のデータベースからの結果をフィルタリングするときに「where like」句と全文インデックスを使用して、クエリに該当する検索結果を決定します。

<!-- To learn more about the Scout database engine, consult the [Scout documentation](/docs/9.x/scout). -->
Scout データベース エンジンの詳細については、[Scout documentation](/docs/9.x/scout) を参照してください。

<a name="rendering-inline-blade-templates"></a>
<!-- ### Rendering Inline Blade Templates -->
### Rendering Inline Blade Templates

<!-- _Rendering inline Blade templates was contributed by [Jason Beggs](https://github.com/jasonlbeggs). Rendering inline Blade components was contributed by [Toby Zerner](https://github.com/tobyzerner)_. -->
_インライン Blade テンプレートのレンダリングは、[Jason Beggs](https://github.com/jasonlbeggs) によって提供されました。インライン Blade コンポーネントのレンダリングは、[Toby Zerner](https://github.com/tobyzerner)_ によって提供されました。

<!-- Sometimes you may need to transform a raw Blade template string into valid HTML. You may accomplish this using the `render` method provided by the `Blade` facade. The `render` method accepts the Blade template string and an optional array of data to provide to the template: -->
場合によっては、生の Blade テンプレート文字列を有効な HTML に変換する必要があるかもしれません。これは、`Blade` ファサードによって提供される `render` メソッドを使用して実行できます。 `render` メソッドは、Blade テンプレート文字列と、テンプレートに提供するオプションのデータ配列を受け入れます。

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

<!-- Similarly, the `renderComponent` method may be used to render a given class component by passing the component instance to the method: -->
同様に、`renderComponent` メソッドを使用して、コンポーネント インスタンスをメソッドに渡すことで、特定のクラス コンポーネントをレンダリングできます。

```php
use App\View\Components\HelloComponent;

return Blade::renderComponent(new HelloComponent('Julian Bashir'));
```

<a name="slot-name-shortcut"></a>
<!-- ### Slot Name Shortcut -->
### Slot Name Shortcut

<!-- _Slot name shortcuts were contributed by [Caleb Porzio](https://github.com/calebporzio)._ -->
_スロット名のショートカットは [Caleb Porzio](https://github.com/calebporzio) によって提供されました。_

<!-- In previous releases of Laravel, slot names were provided using a `name` attribute on the `x-slot` tag: -->
Laravel の以前のリリースでは、スロット名は `x-slot` タグの `name` 属性を使用して提供されていました。

```blade
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- However, beginning in Laravel 9.x, you may specify the slot's name using a convenient, shorter syntax: -->
ただし、Laravel 9.x 以降では、便利で短い構文を使用してスロット名を指定できるようになりました。

```xml
<x-slot:title>
    Server Error
</x-slot>
```

<a name="checked-selected-blade-directives"></a>
<!-- ### Checked / Selected Blade Directives -->
### Checked / Selected Blade Directives

<!-- _Checked and selected Blade directives were contributed by [Ash Allen](https://github.com/ash-jc-allen) and [Taylor Otwell](https://github.com/taylorotwell)_. -->
_チェックおよび選択された Blade ディレクティブは、[Ash Allen](https://github.com/ash-jc-allen) および [Taylor Otwell](https://github.com/taylorotwell)_ によって寄稿されました。

<!-- For convenience, you may now use the `@checked` directive to easily indicate if a given HTML checkbox input is "checked". This directive will echo `checked` if the provided condition evaluates to `true`: -->
便宜上、`@checked` ディレクティブを使用して、特定の HTML チェックボックス入力が「チェックされている」かどうかを簡単に示すことができるようになりました。このディレクティブは、指定された条件が `true` と評価される場合、`checked` をエコーし​​ます。

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

<!-- Likewise, the `@selected` directive may be used to indicate if a given select option should be "selected": -->
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
<!-- ### Bootstrap 5 Pagination Views -->
### Bootstrap 5 Pagination Views

<!-- _Bootstrap 5 pagination views were contributed by [Jared Lewis](https://github.com/jrd-lewis)_. -->
_Bootstrap 5 ページネーション ビューは、[Jared Lewis](https://github.com/jrd-lewis)_ によって寄稿されました。

<!-- Laravel now includes pagination views built using [Bootstrap 5](https://getbootstrap.com/). To use these views instead of the default Tailwind views, you may call the paginator's `useBootstrapFive` method within the `boot` method of your `App\Providers\AppServiceProvider` class: -->
Laravel には、[Bootstrap 5](https://getbootstrap.com/) を使用して構築されたページ分割ビューが含まれるようになりました。デフォルトの Tailwind ビューの代わりにこれらのビューを使用するには、`App\Providers\AppServiceProvider` クラスの `boot` メソッド内でページネータの `useBootstrapFive` メソッドを呼び出すことができます。

```
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
```

<a name="improved-validation-of-nested-array-data"></a>
<!-- ### Improved Validation Of Nested Array Data -->
### Improved Validation Of Nested Array Data

<!-- _Improved validation of nested array inputs was contributed by [Steve Bauman](https://github.com/stevebauman)_. -->
_ネストされた配列入力の検証の改善は、[Steve Bauman](https://github.com/stevebauman)_ によって提供されました。

<!-- Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may now accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element: -->
属性に検証ルールを割り当てるときに、特定のネストされた配列要素の値にアクセスする必要がある場合があります。 `Rule::forEach` メソッドを使用してこれを実行できるようになりました。 `forEach` メソッドは、検証中の配列属性の反復ごとに呼び出されるクロージャを受け入れ、属性の値と明示的な完全に展開された属性名を受け取ります。クロージャは、配列要素に割り当てるルールの配列を返す必要があります。

```
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
```

<a name="laravel-breeze-api"></a>
<!-- ### Laravel Breeze API & Next.js -->
### Laravel Breeze API & Next.js

<!-- _The Laravel Breeze API scaffolding and Next.js starter kit was contributed by [Taylor Otwell](https://github.com/taylorotwell) and [Miguel Piedrafita](https://twitter.com/m1guelpf)_. -->
_Laravel Breeze API スキャフォールディングと Next.js スターター キットは、[Taylor Otwell](https://github.com/taylorotwell) および [Miguel Piedrafita](https://twitter.com/m1guelpf)_ によって提供されました。

<!-- The [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-next) starter kit has received an "API" scaffolding mode and complimentary [Next.js](https://nextjs.org) [frontend implementation](https://github.com/laravel/breeze-next). This starter kit scaffolding may be used to jump start your Laravel applications that are serving as a backend, Laravel Sanctum authenticated API for a JavaScript frontend. -->
[Laravel Breeze](/docs/9.x/starter-kits#breeze-and-next) スターター キットには、「API」スキャフォールディング モードと無料の [Next.js](https://nextjs.org) [frontend implementation](https://github.com/laravel/breeze-next) が含まれています。このスターター キット スキャフォールディングは、バックエンドとして機能する Laravel アプリケーション (JavaScript フロントエンド用の Laravel Sanctum 認証済み API) をすぐに開始するために使用できます。

<a name="exception-page"></a>
<!-- ### Improved Ignition Exception Page -->
### Improved Ignition Exception Page

<!-- _Ignition is developed by [Spatie](https://spatie.be/)._ -->
_Ignition は [Spatie](https://spatie.be/) によって開発されました。_

<!-- Ignition, the open source exception debug page created by Spatie, has been redesigned from the ground up. The new, improved Ignition ships with Laravel 9.x and includes light / dark themes, customizable "open in editor" functionality, and more. -->
Spatie が作成したオープンソースの例外デバッグ ページである Ignition は、根本から再設計されました。新しく改良された Ignition は Laravel 9.x に同梱されており、ライト/ダーク テーマ、カスタマイズ可能な「エディタで開く」機能などが含まれています。

<!--
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/483853/149235404-f7caba56-ebdf-499e-9883-cac5d5610369.png"/>
</p>
-->
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/483853/149235404-f7caba56-ebdf-499e-9883-cac5d5610369.png"/>
</p>

<a name="improved-route-list"></a>
<!-- ### Improved `route:list` CLI Output -->
### Improved `route:list` CLI Output

<!-- _Improved `route:list` CLI output was contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_改良された `route:list` CLI 出力は、[Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- The `route:list` CLI output has been significantly improved for the Laravel 9.x release, offering a beautiful new experience when exploring your route definitions. -->
`route:list` CLI 出力は Laravel 9.x リリースで大幅に改善され、ルート定義を探索するときに美しく新しいエクスペリエンスを提供します。

<!--
<p align="center">
<img src="https://user-images.githubusercontent.com/5457236/148321982-38c8b869-f188-4f42-a3cc-a03451d5216c.png"/>
</p>
-->
<p align="center">
<img src="https://user-images.githubusercontent.com/5457236/148321982-38c8b869-f188-4f42-a3cc-a03451d5216c.png"/>
</p>

<a name="test-coverage-support-on-artisan-test-Command"></a>
<!-- ### Test Coverage Using Artisan `test` Command -->
### Test Coverage Using Artisan `test` Command

<!-- _Test coverage when using the Artisan `test` command was contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_Artisan `test` コマンド使用時のテスト カバレッジは、[Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- The Artisan `test` command has received a new `--coverage` option that you may use to explore the amount of code coverage your tests are providing to your application: -->
Artisan `test` コマンドに、テストがアプリケーションに提供するコード カバレッジの量を調査するために使用できる新しい `--coverage` オプションが追加されました。

```shell
php artisan test --coverage
```

<!-- The test coverage results will be displayed directly within the CLI output. -->
テスト カバレッジの結果は、CLI 出力内に直接表示されます。

<!--
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>
-->
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>

<!-- In addition, if you would like to specify a minimum threshold that your test coverage percentage must meet, you may use the `--min` option. The test suite will fail if the given minimum threshold is not met: -->
さらに、テスト カバレッジ パーセンテージが満たさなければならない最小しきい値を指定したい場合は、`--min` オプションを使用できます。指定された最小しきい値が満たされていない場合、テスト スイートは失敗します。

```shell
php artisan test --coverage --min=80.3
```

<!--
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/149989853-a29a7629-2bfa-4bf3-bbf7-cdba339ec157.png"/>
</p>
-->
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/149989853-a29a7629-2bfa-4bf3-bbf7-cdba339ec157.png"/>
</p>

<a name="soketi-echo-server"></a>
<!-- ### Soketi Echo Server -->
### Soketi Echo Server

<!-- _The Soketi Echo server was developed by [Alex Renoki](https://github.com/rennokki)_. -->
_Soketi Echo サーバーは [Alex Renoki](https://github.com/rennokki)_ によって開発されました。

<!-- Although not exclusive to Laravel 9.x, Laravel has recently assisted with the documentation of Soketi, a [Laravel Echo](/docs/9.x/broadcasting) compatible Web Socket server written for Node.js. Soketi provides a great, open source alternative to Pusher and Ably for those applications that prefer to manage their own Web Socket server. -->
Laravel 9.x に限定されたものではありませんが、Laravel は最近、Node.js 用に作成された [Laravel Echo](/docs/9.x/broadcasting) 互換の Web ソケット サーバーである Soketi のドキュメントを支援しました。 Soketi は、独自の Web Socket サーバーを管理することを好むアプリケーション向けに、Pusher や Ably に代わる優れたオープンソースの代替手段を提供します。

<!-- For more information on using Soketi, please consult the [broadcasting documentation](/docs/9.x/broadcasting) and [Soketi documentation](https://docs.soketi.app/). -->
Soketi の使用方法の詳細については、[broadcasting documentation](/docs/9.x/broadcasting) および [Soketi documentation](https://docs.soketi.app/) を参照してください。

<a name="improved-collections-ide-support"></a>
<!-- ### Improved Collections IDE Support -->
### Improved Collections IDE Support

<!-- _Improved collections IDE support was contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_コレクション IDE サポートの改善は、[Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- Laravel 9.x adds improved, "generic" style type definitions to the collections component, improving IDE and static analysis support. IDEs such as [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections) or static analysis tools such as [PHPStan](https://phpstan.org) will now better understand Laravel collections natively. -->
Laravel 9.x では、改良された「汎用」スタイル型定義がコレクションコンポーネントに追加され、IDE と静的分析のサポートが改善されています。 [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections) などの IDE や [PHPStan](https://phpstan.org) などの静的分析ツールは、Laravel コレクションをネイティブに理解できるようになりました。

<!--
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/151783350-ed301660-1e09-44c1-b549-85c6db3f078d.gif"/>
</p>
-->
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/151783350-ed301660-1e09-44c1-b549-85c6db3f078d.gif"/>
</p>

<a name="new-helpers"></a>
<!-- ### New Helpers -->
### New Helpers

<!-- Laravel 9.x introduces two new, convenient helper functions that you may use in your own application. -->
Laravel 9.x では、独自のアプリケーションで使用できる 2 つの新しい便利なヘルパ関数が導入されています。

<a name="new-helpers-str"></a>
<!-- #### `str` -->
#### `str`

<!-- The `str` function returns a new `Illuminate\Support\Stringable` instance for the given string. This function is equivalent to the `Str::of` method: -->
`str` 関数は、指定された文字列の新しい `Illuminate\Support\Stringable` インスタンスを返します。この関数は、`Str::of` メソッドと同等です。

```
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<!-- If no argument is provided to the `str` function, the function returns an instance of `Illuminate\Support\Str`: -->
`str` 関数に引数が指定されていない場合、関数は `Illuminate\Support\Str` のインスタンスを返します。

```
$snake = str()->snake('LaravelFramework');

// 'laravel_framework'
```

<a name="new-helpers-to-route"></a>
<!-- #### `to_route` -->
#### `to_route`

<!-- The `to_route` function generates a redirect HTTP response for a given named route, providing an expressive way to redirect to named routes from your routes and controllers: -->
`to_route` 関数は、指定された名前付きルートのリダイレクト HTTP 応答を生成し、ルートとコントローラから名前付きルートにリダイレクトする表現力豊かな方法を提供します。

```
return to_route('users.show', ['user' => 1]);
```

<!-- If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the to_route method: -->
必要に応じて、リダイレクトに割り当てる HTTP ステータス コードと追加の応答ヘッダーを、to_route メソッドの 3 番目と 4 番目の引数として渡すことができます。

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

