<!-- # Laravel Head -->
# Laravel Head

- [Introduction](#introduction)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Resolution Precedence](#resolution-precedence)
- [Defining Metadata](#defining-metadata)
    - [Defaults](#defaults)
    - [Route Metadata](#route-metadata)
    - [Runtime Metadata](#runtime-metadata)
    - [Error Pages](#error-pages)
- [Open Graph](#open-graph)
    - [X / Twitter Cards](#twitter-cards)
- [Theme Colors](#theme-colors)
- [Application Metadata and Icons](#app-metadata-and-icons)
- [Progressive Web Apps](#progressive-web-apps)
- [Performance and Discovery](#performance-and-discovery)
- [Custom Tags](#custom-tags)
- [Schemas](#schemas)
    - [Breadcrumbs](#breadcrumbs)
    - [FAQs](#faqs)
    - [Custom Schemas](#custom-schemas)
- [Rendering](#rendering)
    - [Blade](#blade)
    - [Livewire](#livewire)
    - [Inertia](#inertia)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Head](https://github.com/laravel/head) provides a fluent API for managing your application's document `<head>` element, including title and meta tags, Open Graph metadata, canonical URLs, robots directives, performance hints, and structured data. It works with Blade, Livewire, and Inertia. -->
[Laravel Head](https://github.com/laravel/head) は、アプリケーションのドキュメント `<head>` 要素を管理するための fluent API を提供します。タイトルや meta タグ、Open Graph メタデータ、canonical URL、robots ディレクティブ、パフォーマンスヒント、構造化データなどを扱えます。Blade、Livewire、Inertia で利用できます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Laravel Head using the Composer package manager: -->
Composer パッケージマネージャを使って Laravel Head をインストールできます。

```shell
composer require laravel/head
```

<a name="quickstart"></a>
<!-- ## Quickstart -->
## Quickstart

<!-- Register site-wide defaults in a service provider: -->
サービス全体のデフォルトをサービスプロバイダに登録します。

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head
    ->title('Laravel', suffix: ' - Laravel')
    ->description('Build something great.'));
```

<!-- Set page-specific metadata at runtime: -->
ページごとのメタデータを実行時に設定します：

```php
Head::title($post->title)
    ->description($post->description);
```

<!-- Render the resolved tags in your layout: -->
レイアウトで解決済みのタグをレンダリングします。

```blade
<head>
    @head
</head>
```

<a name="resolution-precedence"></a>
<!-- ## Resolution Precedence -->
## Resolution Precedence

<!-- Page metadata resolves from five layers, listed from lowest to highest priority: -->
ページメタデータは、優先度の低いものから高いものへ、次の5つのレイヤーで解決されます。

<!-- 1. Page defaults 2. Route group metadata 3. Route metadata 4. Runtime metadata 5. Error metadata -->
1. ページのデフォルト設定
2. ルートグループのメタデータ
3. ルートのメタデータ
4. ランタイムのメタデータ
5. エラーのメタデータ

<!-- Higher layers replace lower layers field by field. For example, a runtime title replaces the route title without replacing the route description. The sections that follow describe how to set metadata at each layer. For information about rendering the resolved metadata in Blade, Livewire, and Inertia, see [Rendering](#rendering). -->
上位レイヤーは、フィールド単位で下位レイヤーを置き換えます。たとえば、実行時のタイトルを設定するとルートのタイトルは置き換わりますが、ルートの説明は置き換わりません。以降のセクションでは、各レイヤーでメタデータを設定する方法を説明します。解決されたメタデータを Blade、Livewire、Inertia でレンダリングする方法については、[Rendering](#rendering)を参照してください。

<a name="defining-metadata"></a>
<!-- ## Defining Metadata -->
## Defining Metadata

<!-- Laravel Head allows you to define metadata using site-wide defaults, route metadata, runtime calls, and error page definitions. -->
Laravel Head では、サイト全体のデフォルト値、ルートのメタデータ、実行時の呼び出し、エラーページの定義を使ってメタデータを定義できます。

<a name="defaults"></a>
<!-- ### Defaults -->
### Defaults

<!-- Register page defaults in a service provider: -->
サービスプロバイダでページのデフォルト値を登録します。

```php
use Laravel\Head\Enums\OgType;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(function (HeadBuilder $head) {
    $head
        ->title('Laravel', suffix: ' - Laravel')
        ->description('Build something great.')
        ->canonical()
        ->og(siteName: 'Laravel', type: OgType::Website)
        ->searchableByRobots()
        ->preconnect('https://fonts.example.com');
});
```

<!-- Defaults are the lowest-priority page metadata layer. If no route, runtime, or error metadata sets a title, `Laravel` renders as-is. When a higher layer sets a page title, the inherited suffix is applied, so `Head::title('About')` renders `About - Laravel`. Pass `exact: true` for titles that should ignore an inherited prefix or suffix. -->
デフォルトは、ページメタデータの中で最も優先度の低い層です。ルート、ランタイム、エラーメタデータのいずれによってもタイトルが設定されていない場合、`Laravel` はそのまま表示されます。上位の層でページタイトルを設定すると、継承されたサフィックスが適用されるため、`Head::title('About')` は `About - Laravel` として表示されます。継承されたプレフィックスまたはサフィックスを無視するタイトルには、`exact: true` を渡してください。

<!-- Calling `Head::canonical()` renders a canonical URL using the current request URL. To set an explicit URL, pass a string such as `Head::canonical('/about')`. Canonical URLs are normalized to `https` by default; pass `forceHttps: false` to preserve the request scheme. -->
`Head::canonical()` を呼び出すと、現在のリクエスト URL を使って canonical URL を生成します。明示的な URL を設定するには、`Head::canonical('/about')` のように文字列を渡します。canonical URL はデフォルトで `https` に正規化されます。リクエストのスキームを維持するには、`forceHttps: false` を渡してください。

<!-- Robots directives may be passed as a raw string, as `RobotsRule` enum cases, or as a list mixing both forms. Lists are rendered as comma-separated directives, so `Head::robots([RobotsRule::NoIndex, RobotsRule::NoFollow])` renders `noindex, nofollow`. -->
Robots ディレクティブは、文字列として直接渡すことも、`RobotsRule` の enum ケースとして渡すことも、両方を組み合わせたリストとして渡すこともできます。リストはカンマ区切りのディレクティブとして出力されるため、`Head::robots([RobotsRule::NoIndex, RobotsRule::NoFollow])` は `noindex, nofollow` として出力されます。

<!-- For convenience, the `searchableByRobots` method renders `all`, while the `hiddenFromRobots` method renders `none`. -->
便宜上、`searchableByRobots` メソッドは `all` を出力し、`hiddenFromRobots` メソッドは `none` を出力します。

<a name="route-metadata"></a>
<!-- ### Route Metadata -->
### Route Metadata

<!-- You may define metadata directly on routes, which is especially useful for semi-static pages whose metadata is known ahead of time. -->
ルート上でメタデータを直接定義できます。これは、メタデータがあらかじめわかっている準静的なページで特に便利です。

<a name="routes-and-groups"></a>
<!-- #### Routes and Groups -->
#### Routes and Groups

```php
Route::view('/contact', 'contact')
    ->name('contact')
    ->withHead(
        title: 'Contact Us',
        description: 'Get in touch.',
    );
```

<!-- Shared route metadata may be applied to a group at any position in the chain: -->
共有するルートメタデータは、チェーン内の任意の位置でグループに適用できます。

```php
Route::withHead(robots: 'noindex, nofollow')
    ->prefix('admin')
    ->name('admin.')
    ->group(function () {
        Route::get('/dashboard', DashboardController::class)
            ->name('dashboard')
            ->withHead(title: 'Dashboard');
    });
```

<!-- You may also define metadata for resource and singleton routes: -->
リソースルートとシングルトンルートのメタデータも定義できます。

```php
Route::resource('posts', PostController::class)->withHead(
    robots: 'index, follow',
);

Route::singleton('profile', ProfileController::class)->withHead(
    title: 'Your Profile',
);
```

<!-- The `withHead` method stores plain arrays through Laravel's native route metadata API. It is equivalent to calling the `metadata` method with the attributes nested under a `head` key, so the metadata remains compatible with cached routes. -->
`withHead` メソッドは、Laravel のネイティブなルートメタデータ API を通じて単純な配列を保存します。これは、属性を `head` キーの下にネストして `metadata` メソッドを呼び出すのと同じであるため、メタデータはキャッシュ済みルートとの互換性を維持します。

<!-- The named arguments are intentionally limited to Laravel Head's built-in route properties so editors and static analysis can catch misspelled names. Route attributes registered by custom tag builders may be passed through `extensions`: -->
名前付き引数は、エディタや静的解析で名前のスペルミスを検出できるよう、Laravel Head に組み込まれたルートプロパティに意図的に限定されています。カスタムタグビルダが登録したルート属性は、`extensions` を通じて渡せます。

```php
Route::get('/article', ArticleController::class)->withHead(
    title: 'Article',
    extensions: ['readingTime' => 4],
);
```

<a name="supported-properties"></a>
<!-- #### Supported Properties -->
#### Supported Properties

<!-- The supported route properties map to the same names as the fluent builder methods: -->
サポートされているルートプロパティは、フルーエントビルダーメソッドと同じ名前にマッピングされます。

<!-- | Category | Properties | | --- | --- | | Document | `title`, `description`, `canonical`, `robots` | | Application metadata | `themeColor`, `applicationName`, `colorScheme`, `referrer`, `viewport`, `appleWebAppTitle`, `webAppCapable`, `appleWebAppStatusBarStyle` | | Social | `og`, `ogImage`, `ogVideo`, `ogAudio`, `twitter`, `twitterImage` | | Performance | `preload`, `prefetch`, `preconnect`, `dnsPrefetch` | | Discovery | `alternates`, `feed`, `icon`, `favicon`, `appleTouchIcon`, `appleTouchStartupImage`, `maskIcon`, `manifest` | | Structured data | `schema` | | Custom tags | `meta`, `link` | -->
| カテゴリ | プロパティ |
| --- | --- |
| ドキュメント | `title`, `description`, `canonical`, `robots` |
| アプリケーションメタデータ | `themeColor`, `applicationName`, `colorScheme`, `referrer`, `viewport`, `appleWebAppTitle`, `webAppCapable`, `appleWebAppStatusBarStyle` |
| ソーシャル | `og`, `ogImage`, `ogVideo`, `ogAudio`, `twitter`, `twitterImage` |
| パフォーマンス | `preload`, `prefetch`, `preconnect`, `dnsPrefetch` |
| 検出 | `alternates`, `feed`, `icon`, `favicon`, `appleTouchIcon`, `appleTouchStartupImage`, `maskIcon`, `manifest` |
| 構造化データ | `schema` |
| カスタムタグ | `meta`, `link` |

<!-- Nested option names use the same `camelCase` naming as the fluent API, such as `forceHttps`, `siteName`, and `secureUrl`. -->
ネストしたオプション名には、`forceHttps`、`siteName`、`secureUrl` のように、fluent API と同じ `camelCase` 命名規則を使用します。

<!-- Repeatable properties, such as `ogImage`, `preload`, `feed`, `schema`, `icon`, and `appleTouchStartupImage`, accept either a single value or a list. -->
`ogImage`、`preload`、`feed`、`schema`、`icon`、`appleTouchStartupImage` などの複数指定可能なプロパティには、単一の値またはリストを指定できます。

<a name="runtime-metadata"></a>
<!-- ### Runtime Metadata -->
### Runtime Metadata

<!-- When a value isn't known until a request arrives, such as the title of a post being viewed, you may set it at runtime: -->
リクエストが届くまで値がわからない場合、たとえば閲覧中の投稿のタイトルなどは、実行時に設定できます。

```php
use Laravel\Head\Facades\Head;

public function __invoke(Post $post): Response
{
    Head::title($post->title);

    // ...
}
```

<!-- Runtime calls made via the `Head` facade override route metadata for request-dependent data. Controllers and actions are the most common places to make these calls: -->
`Head` ファサードを介して実行するランタイム呼び出しは、リクエストに依存するデータのルートメタデータを上書きします。こうした呼び出しを行う場所として最も一般的なのは、コントローラとアクションです。

```php
use App\Models\Post;
use Laravel\Head\Facades\Head;

public function show(Post $post)
{
    Head::title($post->title)
        ->description($post->description);

    return view('posts.show', ['post' => $post]);
}
```

<!-- Multiple runtime calls are merged in the order they run. For single-value fields such as title, description, canonical URL, and robots directives, the later call takes precedence. Repeatable fields retain multiple entries, but adding the same key again updates the earlier entry. For the `ogImage` method, the URL is the key: -->
複数のランタイム呼び出しは、実行された順序でマージされます。title、description、canonical URL、robots ディレクティブなどの単一値フィールドでは、後から実行された呼び出しが優先されます。繰り返し可能なフィールドでは複数のエントリが保持されますが、同じキーを再度追加すると、それ以前のエントリが更新されます。`ogImage` メソッドでは、URL がキーになります。

```php
Head::ogImage('/images/cover.jpg', alt: 'Draft cover')
    ->ogImage('/images/gallery.jpg', alt: 'Gallery image')
    ->ogImage('/images/cover.jpg', alt: 'Final cover', width: 1200, height: 630);
```

```html
<meta property="og:image" content="/images/cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Final cover">
<meta property="og:image" content="/images/gallery.jpg">
<meta property="og:image:alt" content="Gallery image">
```

<!-- Open Graph media inherited from your defaults acts as a fallback. When route, runtime, or error metadata defines its own media of the same type, the default media is replaced instead of merged, so a page's `og:image` takes precedence over a site-wide default image. -->
デフォルトから継承した Open Graph のメディアはフォールバックとして機能します。ルート、ランタイム、またはエラーのメタデータで同じタイプのメディアが独自に定義されている場合、デフォルトのメディアはマージされずに置き換えられるため、ページの `og:image` がサイト全体のデフォルト画像より優先されます。

<!-- You may fluently define conditional metadata using the `when` and `unless` methods: -->
条件付きメタデータは、`when` メソッドと `unless` メソッドを使って定義できます。

```php
Head::title($post->title)
    ->when($post->isDraft(), fn ($head) => $head->hiddenFromRobots());
```

<a name="error-pages"></a>
<!-- ### Error Pages -->
### Error Pages

<!-- Typically, you should register error metadata within the `boot` method of your application's `AppServiceProvider` class: -->
通常、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内でエラーメタデータを登録します。

```php
use Laravel\Head\ErrorPages;
use Laravel\Head\Facades\Head;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Head::errors(function (ErrorPages $errors) {
        $errors->defaults(robots: 'noindex, follow');

        $errors->status(
            404,
            title: 'Page Not Found',
            description: 'The page you are looking for could not be found.',
        );
    });
}
```

<!-- The `defaults` and `status` methods also accept the same fluent builder callback used by `Head::defaults()`: -->
`defaults` メソッドと `status` メソッドも、`Head::defaults()` で使用するものと同じ fluent builder のコールバックを受け取れます。

```php
use Laravel\Head\ErrorPages;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::errors(function (ErrorPages $errors) {
    $errors->status(404, fn (HeadBuilder $head) => $head
        ->title('Page Not Found')
        ->description('The page you are looking for could not be found.'));
});
```

<!-- When a response is rendered for a registered error status, that metadata takes precedence over every other layer. -->
登録済みのエラーステータスに対してレスポンスをレンダリングする場合、そのメタデータが他のすべてのレイヤーより優先されます。

<!-- Laravel automatically detects the response status when rendering an error view or executing a respond-phase hook such as Inertia's `handleExceptionsUsing()` method. If you render an error response inside an `$exceptions->render()` callback, call `Head::status(404)` before rendering so the error metadata is applied. -->
Laravel は、エラービューをレンダリングするときや、Inertia の `handleExceptionsUsing()` メソッドのようなレスポンスフェーズのフックを実行するときに、レスポンスのステータスを自動的に検出します。`$exceptions->render()` コールバック内でエラーレスポンスをレンダリングする場合は、レンダリング前に `Head::status(404)` を呼び出して、エラーのメタデータが適用されるようにしてください。

<a name="open-graph"></a>
<!-- ## Open Graph -->
## Open Graph

<!-- You may set Open Graph properties using the `og` method. Repeatable media may be added using the top-level methods, which accept named arguments directly: -->
`og` メソッドを使用して、Open Graph プロパティを設定できます。繰り返し指定できるメディアは、名前付き引数を直接受け取るトップレベルメソッドを使用して追加できます。

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\OgType;

Head::og(type: OgType::Article, title: $post->title)
    ->ogImage($post->hero_image_url)
    ->ogImage(
        $post->gallery_image_url,
        alt: $post->gallery_image_alt,
        width: 1200,
        height: 630,
        type: ImageType::Jpeg,
    );
```

<!-- The `ogImage`, `ogVideo`, and `ogAudio` methods accept a URL as their first argument, along with optional named arguments such as `alt`, `width`, `height`, `type`, and `secureUrl` where supported by the Open Graph specification. -->
`ogImage`、`ogVideo`、`ogAudio` メソッドは、最初の引数として URL を受け取ります。また、Open Graph 仕様でサポートされている場合は、`alt`、`width`、`height`、`type`、`secureUrl` などの名前付き引数も任意で指定できます。

<!-- You may pass image MIME types as `ImageType` enum cases anywhere the API accepts an image `type`, such as `ImageType::Svg`, `ImageType::Png`, `ImageType::Jpeg`, and `ImageType::Webp`. -->
API が画像の `type` を受け付ける箇所では、`ImageType::Svg`、`ImageType::Png`、`ImageType::Jpeg`、`ImageType::Webp` などの `ImageType` enum ケースとして画像の MIME タイプを渡せます。

> [!NOTE]
> ドキュメントの `title` と `description` は、不足している `og:title` と `og:description` の値を自動的に補完します。

<!-- For a single Open Graph image with no other attributes, you may pass the `image` named argument to the `og` method: -->
他の属性を指定せず、Open Graph 画像を1つだけ設定する場合は、`og` メソッドに名前付き引数 `image` を渡します。

```php
Head::og(
    type: OgType::Website,
    title: $page->title,
    description: $page->description,
    image: $page->og_image_url,
);
```

<!-- The `og(image: ...)` and `ogImage(...)` calls write to the same underlying image list, so you may use whichever is more expressive at the call site. You may use the [`meta`](#custom-tags) method for custom Open Graph extensions such as product or article properties. -->
`og(image: ...)` と `ogImage(...)` の呼び出しは同じ内部の画像リストに書き込むため、呼び出し箇所でより表現力の高い方を使用できます。商品や記事のプロパティなど、カスタムの Open Graph 拡張には [`meta`](#custom-tags) メソッドを使用できます。

<a name="twitter-cards"></a>
<!-- ### X / Twitter Cards -->
### X / Twitter Cards

<!-- To render X / Twitter cards from the same title, description, and image used by Open Graph, register `twitter()` in your defaults: -->
Open Graph で使用するタイトル、説明、画像と同じ内容で X / Twitter カードを表示するには、デフォルト設定に `twitter()` を登録します。

```php
use Laravel\Head\Enums\TwitterCard;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head->twitter(
    card: TwitterCard::SummaryWithLargeImage,
));
```

<!-- Then set page-level metadata: -->
次に、ページレベルのメタデータを設定します。

```php
Head::title('Introducing Laravel Head')
    ->description('A fluent API for Laravel document head metadata.')
    ->ogImage('https://example.com/social.jpg', alt: 'Introducing Laravel Head');
```

<!-- This renders matching Twitter tags: -->
これは一致する Twitter タグをレンダリングします。

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Introducing Laravel Head">
<meta name="twitter:description" content="A fluent API for Laravel document head metadata.">
<meta name="twitter:image" content="https://example.com/social.jpg">
<meta name="twitter:image:alt" content="Introducing Laravel Head">
```

<!-- You may customize individual pages with explicit Twitter values: -->
Twitter の値を明示的に指定して、個別のページをカスタマイズできます。

```php
Head::twitter(title: $post->social_title)
    ->twitterImage($post->social_image_url, alt: $post->title);
```

<!-- Route metadata accepts `twitter` and `twitterImage`. -->
ルートメタデータは `twitter` と `twitterImage` を受け付けます。

<a name="theme-colors"></a>
<!-- ## Theme Colors -->
## Theme Colors

<!-- You may set theme colors globally, per route, or at runtime: -->
テーマカラーは、グローバル、ルートごと、または実行時に設定できます。

```php
Head::themeColor('#0f172a');
```

<!-- This renders a `<meta name="theme-color">` tag. For media-specific theme colors, you may use the `Media` enum: -->
これにより、`<meta name="theme-color">` タグがレンダリングされます。メディアに応じたテーマカラーには、`Media` enum を使用できます。

```php
use Laravel\Head\Enums\Media;

Head::themeColor('#ffffff', media: Media::Light)
    ->themeColor('#111827', media: Media::Dark);
```

<!-- The `Media` enum also includes `Portrait` and `Landscape`. The `media` argument also accepts a custom media query string. -->
`Media` enumには `Portrait` と `Landscape` も含まれます。`media` 引数にはカスタムメディアクエリ文字列も渡せます。

<!-- Route metadata supports a single theme color through the same `camelCase` key: -->
ルートメタデータでは、同じ `camelCase` キーを使って単一のテーマカラーを指定できます。

```php
Route::view('/dashboard', 'dashboard')->withHead(
    themeColor: '#0f172a',
);
```

<a name="app-metadata-and-icons"></a>
<!-- ## Application Metadata and Icons -->
## Application Metadata and Icons

<!-- Laravel Head includes methods for common browser and application metadata: -->
Laravel Headには、一般的なブラウザおよびアプリケーションのメタデータを扱うメソッドが用意されています。

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\Media;

Head::applicationName('Laravel')
    ->colorScheme('light dark')
    ->referrer('strict-origin-when-cross-origin')
    ->viewport('width=device-width, initial-scale=1')
    ->appleWebAppTitle('Laravel')
    ->webAppCapable()
    ->appleWebAppStatusBarStyle('black')
    ->favicon('/favicon.svg', type: ImageType::Svg)
    ->icon('/favicon-32x32.png', type: ImageType::Png, sizes: '32x32')
    ->appleTouchIcon('/apple-touch-icon.png', sizes: '180x180')
    ->appleTouchStartupImage('/launch.png', media: Media::Portrait)
    ->maskIcon('/safari-pinned-tab.svg', color: '#111827')
    ->manifest('/site.webmanifest');
```

<!-- The `favicon` method is an alias for the `icon` method and accepts the same `type`, `sizes`, and `media` arguments. -->
`favicon` メソッドは `icon` メソッドのエイリアスであり、同じ `type`、`sizes`、`media` 引数を受け取ります。

<!-- Route metadata uses the same names: -->
ルートのメタデータでも同じ名前を使用します：

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\Media;

Route::view('/dashboard', 'dashboard')->withHead(
    applicationName: 'Laravel',
    colorScheme: 'light dark',
    appleWebAppTitle: 'Laravel',
    webAppCapable: true,
    appleWebAppStatusBarStyle: 'black',
    favicon: [
        ['href' => '/favicon.svg', 'type' => ImageType::Svg],
        ['href' => '/favicon-32x32.png', 'type' => ImageType::Png, 'sizes' => '32x32'],
    ],
    appleTouchIcon: ['href' => '/apple-touch-icon.png', 'sizes' => '180x180'],
    appleTouchStartupImage: ['href' => '/launch.png', 'media' => Media::Portrait],
    manifest: '/site.webmanifest',
);
```

<a name="progressive-web-apps"></a>
<!-- ## Progressive Web Apps -->
## Progressive Web Apps

<!-- The `pwa` method configures the common document `<head>` tags needed for an installable web app: -->
`pwa` メソッドは、インストール可能な Web アプリに必要なドキュメントの共通の `<head>` タグを設定します。

```php
Head::pwa(
    name: 'Laravel',
    manifest: '/site.webmanifest',
    themeColor: '#0f172a',
    appleTouchIcon: '/apple-touch-icon.png',
    appleWebAppStatusBarStyle: 'black',
);
```

<!-- This renders the application name, web application manifest link, and iOS standalone metadata. If provided, the theme color, Apple status bar style, and Apple touch icon are also rendered. Creating the web application manifest and registering a service worker remain your application's responsibility. -->
これにより、アプリケーション名、Webアプリケーションマニフェストへのリンク、iOSのスタンドアロンメタデータが出力されます。指定されている場合は、テーマカラー、Appleのステータスバーのスタイル、Apple Touch Iconも出力されます。Webアプリケーションマニフェストの作成とサービスワーカーの登録は、アプリケーション側で行う必要があります。

<!-- You may use the `pwa` method in defaults or runtime metadata. Route metadata supports the individual properties shown above. -->
defaults またはランタイムメタデータで `pwa` メソッドを使用できます。ルートメタデータでは、上記に示した個別のプロパティがサポートされます。

<a name="performance-and-discovery"></a>
<!-- ## Performance and Discovery -->
## Performance and Discovery

<!-- Laravel Head renders performance hints, pagination links, locale alternates, and feed discovery: -->
Laravel Head は、パフォーマンスヒント、ページネーションリンク、ロケールの alternate リンク、フィード検出を生成します。

```php
Head::preload(asset('fonts/inter.woff2'), as: 'font', crossorigin: true)
    ->prefetch(asset('images/next.webp'))
    ->preconnect('https://cdn.example.com')
    ->dnsPrefetch('https://analytics.example.com')
    ->paginate($posts)
    ->alternates([
        'en' => 'https://example.com/en/about',
        'fr' => 'https://example.com/fr/about',
        'x-default' => 'https://example.com/about',
    ])
    ->feed('/feed', title: 'Laravel RSS')
    ->feed('/feed.atom', type: 'atom', title: 'Laravel Atom');
```

<!-- For local assets, `preloadAsset()` and `prefetchAsset()` resolve the URL through the `asset()` helper and detect the `as` attribute from the file extension. Font preloads automatically include `crossorigin`, which the preload specification requires even for same-origin fonts: -->
ローカルアセットの場合、`preloadAsset()` と `prefetchAsset()` は `asset()` ヘルパを通じて URL を解決し、ファイル拡張子から `as` 属性を判定します。フォントのプリロードには `crossorigin` が自動的に含まれます。これは、同一オリジンのフォントであってもプリロード仕様で必要とされるためです。

```php
Head::preloadAsset('fonts/inter.woff2')
    ->prefetchAsset('images/next.webp');
```

```html
<link rel="preload" href="https://example.com/fonts/inter.woff2" as="font" crossorigin>
<link rel="prefetch" href="https://example.com/images/next.webp" as="image">
```

<!-- You may pass `as` explicitly to override detection. The `preloadAsset` method will throw an exception when the `as` attribute cannot be detected from the extension because browsers ignore preloads without this attribute; the `prefetchAsset` method will simply omit it. -->
`as` を明示的に渡して検出を上書きできます。ブラウザはこの属性のない preload を無視するため、拡張子から `as` 属性を検出できない場合、`preloadAsset` メソッドは例外をスローします。`prefetchAsset` メソッドでは、この属性を単に省略します。

<a name="custom-tags"></a>
<!-- ## Custom Tags -->
## Custom Tags

<!-- For tags without a dedicated method, use `meta()` and `link()`: -->
専用のメソッドがないタグには、`meta()` と `link()` を使用します。

```php
Head::meta('format-detection', 'telephone=no')
    ->meta('article:author', $post->author->name)
    ->link('search', '/opensearch.xml', [
        'type' => 'application/opensearchdescription+xml',
        'title' => 'Laravel Search',
    ])
    ->link('me', 'https://social.example.com/@laravel');
```

<!-- You may include a media query on a meta tag when the browser should only apply the tag under matching conditions: -->
ブラウザが一致する条件下でのみタグを適用するようにする場合は、meta タグにメディアクエリを指定できます。

```php
use Laravel\Head\Enums\Media;

Head::meta('theme-color', '#ffffff', media: Media::Light)
    ->meta('theme-color', '#111827', media: Media::Dark);
```

<!-- The `meta` method uses the `name` attribute for regular meta tags. For keys that typically use the `property` attribute, such as Open Graph (`og:`) or article metadata (`article:`), the method switches automatically: -->
`meta` メソッドは、通常の meta タグに `name` 属性を使用します。Open Graph（`og:`）や記事メタデータ（`article:`）のように、通常 `property` 属性を使用するキーの場合、メソッドが自動的に切り替えます。

```php
Head::meta('description', 'About Laravel')
    ->meta('og:title', 'About Laravel');
```

```html
<meta name="description" content="About Laravel">
<meta property="og:title" content="About Laravel">
```

<!-- You may pass `property: true` or `property: false` to explicitly select either attribute. -->
`property: true` または `property: false` を渡して、どちらの属性を選択するか明示的に指定できます。

<a name="schemas"></a>
<!-- ## Schemas -->
## Schemas

<!-- Built-in schema builders cover the common JSON-LD types: -->
組み込みのスキーマビルダは、一般的な JSON-LD の型に対応しています。

```php
use Laravel\Head\Enums\OfferAvailability;
use Laravel\Head\Facades\Schema;

Head::schema(
    Schema::product()
        ->name($product->name)
        ->offers(
            Schema::offer()
                ->price($product->price)
                ->currency('USD')
                ->availability(OfferAvailability::InStock)
        )
);
```

<!-- The built-in factory methods are `article`, `blogPosting`, `product`, `offer`, `brand`, `breadcrumbs`, `faq`, `organization`, `person`, `webPage`, and `webSite`. Unknown factory methods create a generic schema object, so you can still express custom schema.org types. -->
組み込みのファクトリメソッドは、`article`、`blogPosting`、`product`、`offer`、`brand`、`breadcrumbs`、`faq`、`organization`、`person`、`webPage`、`webSite` です。未知のファクトリメソッドを使うと汎用のスキーマオブジェクトが作成されるため、カスタムの schema.org タイプも表現できます。

<!-- When JSON-LD schema data is invalid, Laravel Head throws an exception in non-production environments and logs a warning in production. -->
JSON-LD スキーマデータが無効な場合、Laravel Head は非本番環境では例外をスローし、本番環境では警告をログに記録します。

<a name="breadcrumbs"></a>
<!-- ### Breadcrumbs -->
### Breadcrumbs

<!-- Breadcrumb items may be added one at a time or in bulk. Positions are assigned automatically in the order the items are added: -->
パンくず項目は1つずつ追加することも、一括で追加することもできます。位置は、項目を追加した順に自動的に割り当てられます。

```php
Head::schema(
    Schema::breadcrumbs()->items([
        'Home' => route('home'),
        'Shop' => route('shop.index'),
        'Shoes' => route('shop.category', 'shoes'),
    ])
);
```

<!-- You may use the `item` method to append a single breadcrumb item: -->
`item` メソッドを使用して、単一のパンくず項目を追加できます。

```php
Schema::breadcrumbs()
    ->item('Home', route('home'))
    ->item('Shop', route('shop.index'));
```

<a name="faqs"></a>
<!-- ### FAQs -->
### FAQs

<!-- FAQ entries follow the same pattern. You may add them one at a time using the `question` method or in bulk using the `questions` method: -->
FAQの項目も同じパターンに従います。`question` メソッドを使って1つずつ追加することも、`questions` メソッドを使ってまとめて追加することもできます。

```php
Head::schema(
    Schema::faq()->questions([
        'What is Laravel Head?' => 'A fluent API for managing the document head.',
        'Is it free?' => 'Yes, it is open source.',
    ])
);
```

<a name="custom-schemas"></a>
<!-- ### Custom Schemas -->
### Custom Schemas

<!-- You may explicitly register custom schema types: -->
カスタムスキーマ型を明示的に登録できます。

```php
use DateTimeInterface;
use Laravel\Head\Facades\Schema;
use Laravel\Head\Schema\SchemaObject;
use Laravel\Head\SchemaType;

#[SchemaType('JobPosting')]
class JobPosting extends SchemaObject
{
    public function title(string $title): static
    {
        return $this->set('title', $title);
    }

    public function datePosted(DateTimeInterface|string $date): static
    {
        return $this->date('datePosted', $date);
    }
}

Schema::register(JobPosting::class);

Head::schema(
    Schema::jobPosting()
        ->title('Senior Laravel Developer')
        ->datePosted(now())
);
```

<a name="rendering"></a>
<!-- ## Rendering -->
## Rendering

<!-- Laravel Head resolves page metadata into tags for the current response. How these tags are rendered depends on your application stack. -->
Laravel Headは、現在のレスポンスのページメタデータをタグに変換します。これらのタグがどのようにレンダリングされるかは、アプリケーションのスタックによって異なります。

<!-- The HTML renderer powers the `@head` directive and the rendered elements that Laravel Head shares with Inertia via the `head` prop. The array renderer powers `Head::toArray()` for applications that need the resolved metadata as structured data. -->
HTMLレンダラは、`@head` ディレクティブと、Laravel Head が `head` prop を介して Inertia と共有するレンダリング済み要素を処理します。配列レンダラは、解決済みメタデータを構造化データとして必要とするアプリケーション向けに `Head::toArray()` を処理します。

<a name="blade"></a>
<!-- ### Blade -->
### Blade

<!-- Render the accumulated tags in your layout's `<head>` with the `@head` directive: -->
レイアウトの `<head>` に蓄積されたタグを `@head` ディレクティブで出力します。

```blade
<head>
    <meta charset="utf-8">
    @head
</head>
```

<!-- The `@head` directive renders synchronously, so you should define page metadata before the layout is rendered. -->
`@head` ディレクティブは同期的にレンダリングされるため、レイアウトがレンダリングされる前にページのメタデータを定義してください。

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- Livewire applications use the same `@head` directive in their document layout: -->
Livewire アプリケーションでは、ドキュメントレイアウトで同じ `@head` ディレクティブを使用します。

```blade
<head>
    @head
</head>

<body>
    {{ $slot }}

    @livewireScripts
</body>
```

<!-- No Livewire-specific configuration is required. Laravel Head metadata is resolved per request, and the resolver is request-scoped. Therefore, each `wire:navigate` visit fetches a fresh document whose `@head` output reflects the destination route's metadata. Pages visited using `wire:navigate` receive the appropriate route, runtime, and error metadata without requiring component-level head code. -->
Livewire 固有の設定は必要ありません。Laravel Head のメタデータはリクエストごとに解決され、リゾルバはリクエストスコープで動作します。そのため、`wire:navigate` による訪問では毎回新しいドキュメントが取得され、その `@head` の出力には移動先ルートのメタデータが反映されます。`wire:navigate` で訪問したページでは、コンポーネントレベルで head コードを記述しなくても、適切なルート、ランタイム、エラーのメタデータが適用されます。

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- Use the same `@head` directive in your Inertia root template, alongside Inertia's own components: -->
Inertia 独自のコンポーネントとともに、Inertia のルートテンプレートでも同じ `@head` ディレクティブを使用します。

```blade
<html>
<head>
    <meta charset="utf-8">
    @head

    @viteReactRefresh
    @vite(['resources/css/app.css', 'resources/js/app.tsx'])
    <x-inertia::head />
</head>
<body>
    <x-inertia::app />
</body>
</html>
```

<!-- When Inertia is installed, Laravel Head automatically shares the page-managed head as an array of rendered element strings under a `head` prop on every page object: -->
Inertia をインストールすると、Laravel Head はページで管理される head を、レンダリング済みの要素文字列の配列として、すべてのページオブジェクトの `head` prop に自動的に共有します。

```json
{
    "props": {
        "head": [
            "<title data-inertia=\"title\">Dashboard - Laravel</title>",
            "<meta data-inertia=\"description\" name=\"description\" content=\"Your application overview.\">"
        ]
    }
}
```

<!-- Enable Inertia's `serverHead` option wherever your application calls `createInertiaApp()`. The option is available in Inertia 3.5 and later: -->
アプリケーションで `createInertiaApp()` を呼び出しているすべての箇所で、Inertia の `serverHead` オプションを有効にします。このオプションは Inertia 3.5 以降で利用できます。

```js
createInertiaApp({
    // ...
    serverHead: true,
});
```

<!-- Each page-managed element has a stable `data-inertia` key. The `@head` directive renders the initial document, after which Inertia adopts those elements and keeps them synchronized during standard visits, [instant visits](https://inertiajs.com/docs/v3/the-basics/instant-visits), and back and forward navigation. The elements are present in the initial HTML response, so crawlers and link-preview bots can read them without executing JavaScript. No client-side `<Head>` component is required. -->
ページで管理される各要素には、安定した `data-inertia` キーがあります。`@head` ディレクティブが初期ドキュメントをレンダリングした後、Inertia はそれらの要素を引き継ぎ、通常の訪問、[instant visits](https://inertiajs.com/docs/v3/the-basics/instant-visits)、戻る操作や進む操作によるナビゲーション中も同期を維持します。これらの要素は初期の HTML レスポンスに含まれるため、クローラやリンクプレビュー用のボットは JavaScript を実行しなくても読み取れます。クライアント側の `<Head>` コンポーネントは必要ありません。

<!-- This works with or without [server-side rendering (SSR)](https://inertiajs.com/docs/v3/advanced/server-side-rendering). If your application has a separate SSR entry point, enable `serverHead` there too. Laravel Head automatically deduplicates page-managed elements between `@head` and `<x-inertia::head />`, regardless of their order, while preserving other head elements produced by JavaScript SSR. -->
これは [server-side rendering (SSR)](https://inertiajs.com/docs/v3/advanced/server-side-rendering) の有無にかかわらず動作します。アプリケーションに個別の SSR エントリポイントがある場合は、そこでも `serverHead` を有効にしてください。Laravel Head は、`@head` と `<x-inertia::head />` の間でページが管理する要素を順序に関係なく自動的に重複排除します。同時に、JavaScript の SSR が生成するその他の head 要素は保持します。

> [!NOTE]
> 既存の Inertia アプリケーションに Laravel Head を追加する場合は、Laravel Head が最終的なドキュメントタイトルを管理できるように、`resources/js/app.tsx` と `resources/js/ssr.tsx` から title コールバックを削除してください。また、Inertia の [`<Head>` component](https://inertiajs.com/docs/v3/the-basics/title-and-meta) が管理しているタグを Laravel Head に移し、両者が同じ要素を定義しないようにしてください。

<!-- The `head` prop is omitted from partial reload responses, so Inertia retains the last full page's head. Instant visits likewise retain the current head until the background response arrives. If your application already uses the `head` prop, change its name in a service provider: -->
部分リロードのレスポンスでは `head` prop が省略されるため、Inertia は直前の完全なページの head を保持します。Instant visits でも、バックグラウンドのレスポンスが到着するまで現在の head が保持されます。アプリケーションですでに `head` prop を使用している場合は、サービスプロバイダでその名前を変更してください。

```php
use Laravel\Head\Facades\Head;

public function boot(): void
{
    Head::inertia(prop: '_head');
}
```

<!-- Then point Inertia at the same prop with `serverHead: '_head'`. -->
次に、`serverHead: '_head'` を使って、Inertia が同じ prop を参照するようにします。

<a name="static-inertia-tags"></a>
<!-- #### Static Inertia Tags -->
#### Static Inertia Tags

<!-- Most tags should live in defaults, route metadata, or runtime metadata so Laravel Head can resolve the right value for each page. Use Inertia globals only for document tags rendered in the first HTML response and left unchanged by Inertia for the rest of the session. -->
ほとんどのタグは、Laravel Head が各ページに適した値を解決できるよう、defaults、ルートメタデータ、または実行時メタデータに定義します。Inertia globals は、最初の HTML レスポンスでレンダリングされ、セッションの残りの期間は Inertia によって変更されないドキュメントタグにのみ使用してください。

<!-- Register them in a service provider with `Head::inertiaGlobals()`: -->
サービスプロバイダで `Head::inertiaGlobals()` を使って登録します。

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::inertiaGlobals(function (HeadBuilder $head) {
    $head
        ->viewport('width=device-width, initial-scale=1')
        ->colorScheme('light dark')
        ->icon('/favicon.svg', type: 'image/svg+xml')
        ->appleTouchIcon('/apple-touch-icon.png', sizes: '180x180')
        ->manifest('/site.webmanifest');
});
```

<!-- Inertia globals are excluded from the `head` prop, rendered without `data-inertia` ownership attributes, and never updated after the first response. These globals are suitable for stable browser hints such as viewport, color scheme, favicons, touch icons, and manifests. If a tag is page-specific, SEO-relevant, or may be overridden later, put it in `defaults`, route metadata, or runtime metadata instead. -->
Inertia のグローバルは `head` プロパティから除外され、`data-inertia` 所有権属性なしでレンダリングされ、最初のレスポンス後に更新されることもありません。これらのグローバルは、viewport、カラースキーム、ファビコン、タッチアイコン、マニフェストなど、安定したブラウザヒントに適しています。タグがページ固有のもの、SEO に関係するもの、または後から上書きされる可能性があるものなら、代わりに `defaults`、ルートメタデータ、またはランタイムメタデータに配置してください。

<!-- Applications that need the resolved metadata as structured data instead of rendered tags may call `Head::toArray()`. The returned data includes titles, Open Graph values, JSON-LD schemas, and other resolved metadata. -->
レンダリング済みのタグではなく、解決済みのメタデータを構造化データとして必要とするアプリケーションでは、`Head::toArray()` を呼び出せます。返されるデータには、タイトル、Open Graph の値、JSON-LD スキーマ、その他の解決済みメタデータが含まれます。
