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
[Laravel Head](https://github.com/laravel/head)는 애플리케이션의 문서 `<head>` 요소를 관리하기 위한 유연한 API를 제공합니다. 여기에는 제목 및 메타 태그, Open Graph 메타데이터, 표준 URL, robots 지시문, 성능 힌트, 구조화된 데이터가 포함됩니다. Blade, Livewire, Inertia와 함께 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Laravel Head using the Composer package manager: -->
Composer 패키지 관리자를 사용해 Laravel Head를 설치할 수 있습니다.

```shell
composer require laravel/head
```

<a name="quickstart"></a>
<!-- ## Quickstart -->
## Quickstart

<!-- Register site-wide defaults in a service provider: -->
서비스 전체 기본값을 서비스 프로바이더에 등록합니다:

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head
    ->title('Laravel', suffix: ' - Laravel')
    ->description('Build something great.'));
```

<!-- Set page-specific metadata at runtime: -->
런타임에 페이지별 메타데이터를 설정합니다:

```php
Head::title($post->title)
    ->description($post->description);
```

<!-- Render the resolved tags in your layout: -->
레이아웃에 확인된 태그를 렌더링합니다:

```blade
<head>
    @head
</head>
```

<a name="resolution-precedence"></a>
<!-- ## Resolution Precedence -->
## Resolution Precedence

<!-- Page metadata resolves from five layers, listed from lowest to highest priority: -->
페이지 메타데이터는 우선순위가 낮은 계층부터 높은 계층 순으로 나열된 다음 다섯 계층에서 확인됩니다:

<!-- 1. Page defaults 2. Route group metadata 3. Route metadata 4. Runtime metadata 5. Error metadata -->
1. 페이지 기본값
2. 라우트 그룹 메타데이터
3. 라우트 메타데이터
4. 런타임 메타데이터
5. 오류 메타데이터

<!-- Higher layers replace lower layers field by field. For example, a runtime title replaces the route title without replacing the route description. The sections that follow describe how to set metadata at each layer. For information about rendering the resolved metadata in Blade, Livewire, and Inertia, see [Rendering](#rendering). -->
상위 레이어는 필드별로 하위 레이어를 대체합니다. 예를 들어 런타임 제목은 라우트 설명을 대체하지 않고 라우트 제목을 대체합니다. 이어지는 섹션에서는 각 레이어에서 메타데이터를 설정하는 방법을 설명합니다. Blade, Livewire, Inertia에서 확인된 메타데이터를 렌더링하는 방법은 [Rendering](#rendering)을 참고하세요.

<a name="defining-metadata"></a>
<!-- ## Defining Metadata -->
## Defining Metadata

<!-- Laravel Head allows you to define metadata using site-wide defaults, route metadata, runtime calls, and error page definitions. -->
Laravel Head를 사용하면 사이트 전체 기본값, 라우트 메타데이터, 런타임 호출 및 오류 페이지 정의를 사용해 메타데이터를 정의할 수 있습니다.

<a name="defaults"></a>
<!-- ### Defaults -->
### Defaults

<!-- Register page defaults in a service provider: -->
서비스 프로바이더에서 페이지 기본값을 등록합니다:

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
Defaults는 페이지 메타데이터 계층 중 우선순위가 가장 낮습니다. 라우트, 런타임 또는 오류 메타데이터에서 제목을 설정하지 않으면 `Laravel`이 있는 그대로 렌더링됩니다. 더 높은 계층에서 페이지 제목을 설정하면 상속된 접미사가 적용되므로 `Head::title('About')`은 `About - Laravel`로 렌더링됩니다. 상속된 접두사 또는 접미사를 무시해야 하는 제목에는 `exact: true`를 전달합니다.

<!-- Calling `Head::canonical()` renders a canonical URL using the current request URL. To set an explicit URL, pass a string such as `Head::canonical('/about')`. Canonical URLs are normalized to `https` by default; pass `forceHttps: false` to preserve the request scheme. -->
`Head::canonical()`을 호출하면 현재 요청 URL을 사용해 canonical URL을 렌더링합니다. 명시적인 URL을 설정하려면 `Head::canonical('/about')`와 같이 문자열을 전달합니다. canonical URL은 기본적으로 `https`로 정규화되며, 요청 스킴을 유지하려면 `forceHttps: false`를 전달합니다.

<!-- Robots directives may be passed as a raw string, as `RobotsRule` enum cases, or as a list mixing both forms. Lists are rendered as comma-separated directives, so `Head::robots([RobotsRule::NoIndex, RobotsRule::NoFollow])` renders `noindex, nofollow`. -->
Robots 지시어는 원시 문자열, `RobotsRule` 열거형 케이스 또는 두 형식을 혼합한 목록으로 전달할 수 있습니다. 목록은 쉼표로 구분된 지시어로 렌더링되므로 `Head::robots([RobotsRule::NoIndex, RobotsRule::NoFollow])`는 `noindex, nofollow`로 렌더링됩니다.

<!-- For convenience, the `searchableByRobots` method renders `all`, while the `hiddenFromRobots` method renders `none`. -->
편의를 위해 `searchableByRobots` 메서드는 `all`을 렌더링하고 `hiddenFromRobots` 메서드는 `none`을 렌더링합니다.

<a name="route-metadata"></a>
<!-- ### Route Metadata -->
### Route Metadata

<!-- You may define metadata directly on routes, which is especially useful for semi-static pages whose metadata is known ahead of time. -->
라우트에 메타데이터를 직접 정의할 수 있으며, 이는 메타데이터를 미리 알고 있는 반정적 페이지에 특히 유용합니다.

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
공유 라우트 메타데이터는 체인의 어느 위치에서든 그룹에 적용할 수 있습니다:

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
리소스 및 싱글턴 라우트에 대한 메타데이터도 정의할 수 있습니다.

```php
Route::resource('posts', PostController::class)->withHead(
    robots: 'index, follow',
);

Route::singleton('profile', ProfileController::class)->withHead(
    title: 'Your Profile',
);
```

<!-- The `withHead` method stores plain arrays through Laravel's native route metadata API. It is equivalent to calling the `metadata` method with the attributes nested under a `head` key, so the metadata remains compatible with cached routes. -->
`withHead` 메서드는 Laravel의 네이티브 라우트 메타데이터 API를 통해 일반 배열을 저장합니다. 이는 `head` 키 아래에 속성을 중첩하여 `metadata` 메서드를 호출하는 것과 동일하므로, 메타데이터가 캐시된 라우트와의 호환성을 유지합니다.

<!-- The named arguments are intentionally limited to Laravel Head's built-in route properties so editors and static analysis can catch misspelled names. Route attributes registered by custom tag builders may be passed through `extensions`: -->
이름이 지정된 인수는 편집기와 정적 분석 도구가 철자가 틀린 이름을 감지할 수 있도록 Laravel Head에 내장된 라우트 속성으로 의도적으로 제한되어 있습니다. 사용자 지정 태그 빌더에 등록된 라우트 속성은 `extensions`를 통해 전달할 수 있습니다.

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
지원되는 라우트 속성은 fluent builder 메서드와 동일한 이름으로 매핑됩니다:

<!-- | Category | Properties | | --- | --- | | Document | `title`, `description`, `canonical`, `robots` | | Application metadata | `themeColor`, `applicationName`, `colorScheme`, `referrer`, `viewport`, `appleWebAppTitle`, `webAppCapable`, `appleWebAppStatusBarStyle` | | Social | `og`, `ogImage`, `ogVideo`, `ogAudio`, `twitter`, `twitterImage` | | Performance | `preload`, `prefetch`, `preconnect`, `dnsPrefetch` | | Discovery | `alternates`, `feed`, `icon`, `favicon`, `appleTouchIcon`, `appleTouchStartupImage`, `maskIcon`, `manifest` | | Structured data | `schema` | | Custom tags | `meta`, `link` | -->
| 카테고리 | 속성 |
| --- | --- |
| 문서 | `title`, `description`, `canonical`, `robots` |
| 애플리케이션 메타데이터 | `themeColor`, `applicationName`, `colorScheme`, `referrer`, `viewport`, `appleWebAppTitle`, `webAppCapable`, `appleWebAppStatusBarStyle` |
| 소셜 | `og`, `ogImage`, `ogVideo`, `ogAudio`, `twitter`, `twitterImage` |
| 성능 | `preload`, `prefetch`, `preconnect`, `dnsPrefetch` |
| 검색 | `alternates`, `feed`, `icon`, `favicon`, `appleTouchIcon`, `appleTouchStartupImage`, `maskIcon`, `manifest` |
| 구조화된 데이터 | `schema` |
| 사용자 지정 태그 | `meta`, `link` |

<!-- Nested option names use the same `camelCase` naming as the fluent API, such as `forceHttps`, `siteName`, and `secureUrl`. -->
중첩 옵션 이름은 fluent API와 동일한 `camelCase` 명명 규칙을 사용합니다. 예를 들어 `forceHttps`, `siteName`, `secureUrl`이 있습니다.

<!-- Repeatable properties, such as `ogImage`, `preload`, `feed`, `schema`, `icon`, and `appleTouchStartupImage`, accept either a single value or a list. -->
`ogImage`, `preload`, `feed`, `schema`, `icon`, `appleTouchStartupImage`와 같은 반복 가능한 속성은 단일 값이나 목록을 사용할 수 있습니다.

<a name="runtime-metadata"></a>
<!-- ### Runtime Metadata -->
### Runtime Metadata

<!-- When a value isn't known until a request arrives, such as the title of a post being viewed, you may set it at runtime: -->
요청이 들어올 때까지 값을 알 수 없는 경우, 예를 들어 조회 중인 게시물의 제목과 같은 값은 런타임에 설정할 수 있습니다:

```php
use Laravel\Head\Facades\Head;

public function __invoke(Post $post): Response
{
    Head::title($post->title);

    // ...
}
```

<!-- Runtime calls made via the `Head` facade override route metadata for request-dependent data. Controllers and actions are the most common places to make these calls: -->
`Head` 파사드를 통해 수행되는 런타임 호출은 요청에 의존하는 데이터의 라우트 메타데이터를 재정의합니다. 컨트롤러와 액션은 이러한 호출을 수행하는 가장 일반적인 위치입니다:

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
여러 런타임 호출은 실행되는 순서대로 병합됩니다. title, description, canonical URL, robots 지시어와 같은 단일 값 필드에서는 나중에 호출된 값이 우선합니다. 반복 가능한 필드는 여러 항목을 유지하지만, 동일한 키를 다시 추가하면 앞서 추가된 항목이 업데이트됩니다. `ogImage` 메서드에서는 URL이 키입니다:

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
기본 설정에서 상속된 Open Graph 미디어는 대체 수단으로 사용됩니다. 라우트, 런타임 또는 오류 메타데이터가 동일한 타입의 미디어를 자체적으로 정의하면 기본 미디어는 병합되지 않고 대체되므로, 페이지의 `og:image`가 사이트 전체의 기본 이미지보다 우선합니다.

<!-- You may fluently define conditional metadata using the `when` and `unless` methods: -->
`when` 및 `unless` 메서드를 사용하면 조건부 메타데이터를 유창하게 정의할 수 있습니다:

```php
Head::title($post->title)
    ->when($post->isDraft(), fn ($head) => $head->hiddenFromRobots());
```

<a name="error-pages"></a>
<!-- ### Error Pages -->
### Error Pages

<!-- Typically, you should register error metadata within the `boot` method of your application's `AppServiceProvider` class: -->
일반적으로 애플리케이션의 `AppServiceProvider` 클래스에서 `boot` 메서드 내에 오류 메타데이터를 등록해야 합니다:

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
`defaults` 및 `status` 메서드도 `Head::defaults()`에서 사용하는 것과 동일한 플루언트 빌더 콜백을 허용합니다:

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
응답이 등록된 오류 상태로 렌더링되면 해당 메타데이터가 다른 모든 계층보다 우선합니다.

<!-- Laravel automatically detects the response status when rendering an error view or executing a respond-phase hook such as Inertia's `handleExceptionsUsing()` method. If you render an error response inside an `$exceptions->render()` callback, call `Head::status(404)` before rendering so the error metadata is applied. -->
Laravel은 오류 뷰를 렌더링하거나 Inertia의 `handleExceptionsUsing()` 메서드와 같은 응답 단계 훅을 실행할 때 응답 상태를 자동으로 감지합니다. `$exceptions->render()` 콜백 내부에서 오류 응답을 렌더링한다면, 렌더링하기 전에 `Head::status(404)`를 호출하여 오류 메타데이터가 적용되도록 해야 합니다.

<a name="open-graph"></a>
<!-- ## Open Graph -->
## Open Graph

<!-- You may set Open Graph properties using the `og` method. Repeatable media may be added using the top-level methods, which accept named arguments directly: -->
`og` 메서드를 사용해 Open Graph 속성을 설정할 수 있습니다. 반복 가능한 미디어는 이름이 지정된 인수를 직접 받는 최상위 메서드를 사용해 추가할 수 있습니다:

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
`ogImage`, `ogVideo`, `ogAudio` 메서드는 첫 번째 인수로 URL을 받으며, Open Graph 사양에서 지원하는 경우 `alt`, `width`, `height`, `type`, `secureUrl`와 같은 선택적 명명 인수도 받습니다.

<!-- You may pass image MIME types as `ImageType` enum cases anywhere the API accepts an image `type`, such as `ImageType::Svg`, `ImageType::Png`, `ImageType::Jpeg`, and `ImageType::Webp`. -->
이미지 `type`을 허용하는 API의 모든 곳에서 `ImageType::Svg`, `ImageType::Png`, `ImageType::Jpeg`, `ImageType::Webp`와 같은 `ImageType` enum 케이스로 이미지 MIME 타입을 전달할 수 있습니다.

> [!NOTE]
> 문서의 `title`과 `description`은 누락된 `og:title`과 `og:description` 값을 자동으로 채웁니다.

<!-- For a single Open Graph image with no other attributes, you may pass the `image` named argument to the `og` method: -->
다른 속성 없이 Open Graph 이미지 하나만 지정하려면 `og` 메서드에 `image` 이름 지정 인수를 전달할 수 있습니다:

```php
Head::og(
    type: OgType::Website,
    title: $page->title,
    description: $page->description,
    image: $page->og_image_url,
);
```

<!-- The `og(image: ...)` and `ogImage(...)` calls write to the same underlying image list, so you may use whichever is more expressive at the call site. You may use the [`meta`](#custom-tags) method for custom Open Graph extensions such as product or article properties. -->
`og(image: ...)` 및 `ogImage(...)` 호출은 동일한 내부 이미지 목록에 기록하므로, 호출 위치에서 더 표현력이 높은 방식을 사용하면 됩니다. 제품 또는 문서 속성과 같은 사용자 지정 Open Graph 확장에는 [`meta`](#custom-tags) 메서드를 사용할 수 있습니다.

<a name="twitter-cards"></a>
<!-- ### X / Twitter Cards -->
### X / Twitter Cards

<!-- To render X / Twitter cards from the same title, description, and image used by Open Graph, register `twitter()` in your defaults: -->
Open Graph에 사용하는 것과 동일한 제목, 설명, 이미지를 사용해 X / Twitter 카드를 렌더링하려면 기본값에 `twitter()`를 등록합니다:

```php
use Laravel\Head\Enums\TwitterCard;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head->twitter(
    card: TwitterCard::SummaryWithLargeImage,
));
```

<!-- Then set page-level metadata: -->
그런 다음 페이지 수준 메타데이터를 설정합니다:

```php
Head::title('Introducing Laravel Head')
    ->description('A fluent API for Laravel document head metadata.')
    ->ogImage('https://example.com/social.jpg', alt: 'Introducing Laravel Head');
```

<!-- This renders matching Twitter tags: -->
다음은 일치하는 Twitter 태그를 렌더링합니다:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Introducing Laravel Head">
<meta name="twitter:description" content="A fluent API for Laravel document head metadata.">
<meta name="twitter:image" content="https://example.com/social.jpg">
<meta name="twitter:image:alt" content="Introducing Laravel Head">
```

<!-- You may customize individual pages with explicit Twitter values: -->
개별 페이지에 명시적인 Twitter 값을 지정할 수 있습니다:

```php
Head::twitter(title: $post->social_title)
    ->twitterImage($post->social_image_url, alt: $post->title);
```

<!-- Route metadata accepts `twitter` and `twitterImage`. -->
라우트 메타데이터는 `twitter`와 `twitterImage`를 허용합니다.

<a name="theme-colors"></a>
<!-- ## Theme Colors -->
## Theme Colors

<!-- You may set theme colors globally, per route, or at runtime: -->
테마 색상은 전역, 라우트별 또는 런타임에 설정할 수 있습니다:

```php
Head::themeColor('#0f172a');
```

<!-- This renders a `<meta name="theme-color">` tag. For media-specific theme colors, you may use the `Media` enum: -->
`<meta name="theme-color">` 태그를 렌더링합니다. 미디어별 테마 색상에는 `Media` enum을 사용할 수 있습니다:

```php
use Laravel\Head\Enums\Media;

Head::themeColor('#ffffff', media: Media::Light)
    ->themeColor('#111827', media: Media::Dark);
```

<!-- The `Media` enum also includes `Portrait` and `Landscape`. The `media` argument also accepts a custom media query string. -->
`Media` enum에는 `Portrait`와 `Landscape`도 포함되어 있습니다. `media` 인수에는 사용자 지정 미디어 쿼리 문자열도 전달할 수 있습니다.

<!-- Route metadata supports a single theme color through the same `camelCase` key: -->
라우트 메타데이터는 동일한 `camelCase` 키를 통해 하나의 테마 색상을 지원합니다:

```php
Route::view('/dashboard', 'dashboard')->withHead(
    themeColor: '#0f172a',
);
```

<a name="app-metadata-and-icons"></a>
<!-- ## Application Metadata and Icons -->
## Application Metadata and Icons

<!-- Laravel Head includes methods for common browser and application metadata: -->
Laravel Head에는 자주 사용하는 브라우저 및 애플리케이션 메타데이터를 위한 메서드가 포함되어 있습니다:

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
`favicon` 메서드는 `icon` 메서드의 별칭이며 동일한 `type`, `sizes`, `media` 인수를 받습니다.

<!-- Route metadata uses the same names: -->
라우트 메타데이터는 동일한 이름을 사용합니다:

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
`pwa` 메서드는 설치 가능한 웹 앱에 필요한 일반적인 문서 `<head>` 태그를 설정합니다:

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
애플리케이션 이름, 웹 애플리케이션 매니페스트 링크, iOS 독립 실행형 메타데이터를 렌더링합니다. 제공된 경우 테마 색상, Apple 상태 표시줄 스타일, Apple 터치 아이콘도 렌더링합니다. 웹 애플리케이션 매니페스트를 생성하고 서비스 워커를 등록하는 일은 애플리케이션의 책임입니다.

<!-- You may use the `pwa` method in defaults or runtime metadata. Route metadata supports the individual properties shown above. -->
defaults 또는 runtime metadata에서 `pwa` 메서드를 사용할 수 있습니다. 라우트 메타데이터는 위에 설명된 개별 프로퍼티를 지원합니다.

<a name="performance-and-discovery"></a>
<!-- ## Performance and Discovery -->
## Performance and Discovery

<!-- Laravel Head renders performance hints, pagination links, locale alternates, and feed discovery: -->
Laravel Head는 성능 힌트, 페이지네이션 링크, 로케일 대체 링크, 피드 검색 정보를 렌더링합니다:

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
로컬 에셋의 경우 `preloadAsset()` 및 `prefetchAsset()`는 `asset()` 헬퍼를 통해 URL을 확인하고 파일 확장자에서 `as` 속성을 감지합니다. 글꼴 프리로드에는 동일 출처 글꼴에도 프리로드 사양에서 요구하는 `crossorigin`이 자동으로 포함됩니다:

```php
Head::preloadAsset('fonts/inter.woff2')
    ->prefetchAsset('images/next.webp');
```

```html
<link rel="preload" href="https://example.com/fonts/inter.woff2" as="font" crossorigin>
<link rel="prefetch" href="https://example.com/images/next.webp" as="image">
```

<!-- You may pass `as` explicitly to override detection. The `preloadAsset` method will throw an exception when the `as` attribute cannot be detected from the extension because browsers ignore preloads without this attribute; the `prefetchAsset` method will simply omit it. -->
`as`를 명시적으로 전달하여 감지를 재정의할 수 있습니다. 브라우저는 이 속성이 없는 preload를 무시하므로, 확장자에서 `as` 속성을 감지할 수 없으면 `preloadAsset` 메서드는 예외를 발생시키며 `prefetchAsset` 메서드는 해당 속성을 생략합니다.

<a name="custom-tags"></a>
<!-- ## Custom Tags -->
## Custom Tags

<!-- For tags without a dedicated method, use `meta()` and `link()`: -->
전용 메서드가 없는 태그에는 `meta()`와 `link()`를 사용합니다:

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
브라우저가 일치하는 조건에서만 해당 태그를 적용해야 한다면 meta 태그에 미디어 쿼리를 포함할 수 있습니다:

```php
use Laravel\Head\Enums\Media;

Head::meta('theme-color', '#ffffff', media: Media::Light)
    ->meta('theme-color', '#111827', media: Media::Dark);
```

<!-- The `meta` method uses the `name` attribute for regular meta tags. For keys that typically use the `property` attribute, such as Open Graph (`og:`) or article metadata (`article:`), the method switches automatically: -->
`meta` 메서드는 일반 메타 태그에 `name` 속성을 사용합니다. Open Graph(`og:`)나 아티클 메타데이터(`article:`)처럼 일반적으로 `property` 속성을 사용하는 키의 경우 메서드가 자동으로 전환합니다:

```php
Head::meta('description', 'About Laravel')
    ->meta('og:title', 'About Laravel');
```

```html
<meta name="description" content="About Laravel">
<meta property="og:title" content="About Laravel">
```

<!-- You may pass `property: true` or `property: false` to explicitly select either attribute. -->
`property: true` 또는 `property: false`를 전달해 속성을 명시적으로 선택할 수 있습니다.

<a name="schemas"></a>
<!-- ## Schemas -->
## Schemas

<!-- Built-in schema builders cover the common JSON-LD types: -->
내장 스키마 빌더는 일반적인 JSON-LD 타입을 다룹니다:

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
기본 제공 팩토리 메서드는 `article`, `blogPosting`, `product`, `offer`, `brand`, `breadcrumbs`, `faq`, `organization`, `person`, `webPage`, `webSite`입니다. 알 수 없는 팩토리 메서드는 일반 스키마 객체를 생성하므로, 사용자 지정 schema.org 타입도 표현할 수 있습니다.

<!-- When JSON-LD schema data is invalid, Laravel Head throws an exception in non-production environments and logs a warning in production. -->
JSON-LD 스키마 데이터가 유효하지 않으면 Laravel Head는 프로덕션 환경이 아닌 환경에서 예외를 발생시키고, 프로덕션에서는 경고를 기록합니다.

<a name="breadcrumbs"></a>
<!-- ### Breadcrumbs -->
### Breadcrumbs

<!-- Breadcrumb items may be added one at a time or in bulk. Positions are assigned automatically in the order the items are added: -->
Breadcrumb 항목은 하나씩 추가하거나 한 번에 여러 개 추가할 수 있습니다. 위치는 항목을 추가한 순서에 따라 자동으로 할당됩니다.

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
단일 브레드크럼 항목을 추가하려면 `item` 메서드를 사용할 수 있습니다:

```php
Schema::breadcrumbs()
    ->item('Home', route('home'))
    ->item('Shop', route('shop.index'));
```

<a name="faqs"></a>
<!-- ### FAQs -->
### FAQs

<!-- FAQ entries follow the same pattern. You may add them one at a time using the `question` method or in bulk using the `questions` method: -->
FAQ 항목도 같은 패턴을 따릅니다. `question` 메서드를 사용해 하나씩 추가하거나 `questions` 메서드를 사용해 일괄적으로 추가할 수 있습니다.

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
사용자 지정 스키마 타입을 명시적으로 등록할 수도 있습니다:

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
Laravel Head는 현재 응답의 페이지 메타데이터를 태그로 변환합니다. 이러한 태그가 렌더링되는 방식은 애플리케이션 스택에 따라 달라집니다.

<!-- The HTML renderer powers the `@head` directive and the rendered elements that Laravel Head shares with Inertia via the `head` prop. The array renderer powers `Head::toArray()` for applications that need the resolved metadata as structured data. -->
HTML 렌더러는 `@head` 디렉티브와 Laravel Head가 `head` 프로퍼티를 통해 Inertia와 공유하는 렌더링된 요소를 처리합니다. 배열 렌더러는 확인된 메타데이터를 구조화된 데이터로 사용해야 하는 애플리케이션을 위해 `Head::toArray()`를 처리합니다.

<a name="blade"></a>
<!-- ### Blade -->
### Blade

<!-- Render the accumulated tags in your layout's `<head>` with the `@head` directive: -->
레이아웃의 `<head>`에 `@head` 디렉티브를 사용해 누적된 태그를 렌더링합니다:

```blade
<head>
    <meta charset="utf-8">
    @head
</head>
```

<!-- The `@head` directive renders synchronously, so you should define page metadata before the layout is rendered. -->
`@head` 디렉티브는 동기적으로 렌더링되므로 레이아웃이 렌더링되기 전에 페이지 메타데이터를 정의해야 합니다.

<a name="livewire"></a>
<!-- ### Livewire -->
### Livewire

<!-- Livewire applications use the same `@head` directive in their document layout: -->
Livewire 애플리케이션은 문서 레이아웃에서 동일한 `@head` 디렉티브를 사용합니다:

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
Livewire 전용 설정은 필요하지 않습니다. Laravel Head 메타데이터는 요청마다 확인되며, resolver는 요청 범위로 동작합니다. 따라서 각 `wire:navigate` 방문은 대상 라우트의 메타데이터가 반영된 `@head` 출력을 포함하는 새로운 문서를 가져옵니다. `wire:navigate`를 사용해 방문한 페이지는 컴포넌트 수준의 head 코드 없이 적절한 라우트, 런타임 및 오류 메타데이터를 받습니다.

<a name="inertia"></a>
<!-- ### Inertia -->
### Inertia

<!-- Use the same `@head` directive in your Inertia root template, alongside Inertia's own components: -->
Inertia의 자체 컴포넌트와 함께 Inertia 루트 템플릿에서도 동일한 `@head` 디렉티브를 사용합니다:

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
Inertia를 설치하면 Laravel Head는 페이지에서 관리하는 head를 렌더링된 요소 문자열의 배열로 자동 공유하며, 모든 페이지 객체에서 `head` prop으로 사용할 수 있도록 합니다:

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
애플리케이션에서 `createInertiaApp()`을 호출하는 모든 곳에서 Inertia의 `serverHead` 옵션을 활성화합니다. 이 옵션은 Inertia 3.5 이상에서 사용할 수 있습니다.

```js
createInertiaApp({
    // ...
    serverHead: true,
});
```

<!-- Each page-managed element has a stable `data-inertia` key. The `@head` directive renders the initial document, after which Inertia adopts those elements and keeps them synchronized during standard visits, [instant visits](https://inertiajs.com/docs/v3/the-basics/instant-visits), and back and forward navigation. The elements are present in the initial HTML response, so crawlers and link-preview bots can read them without executing JavaScript. No client-side `<Head>` component is required. -->
각 페이지 관리 요소에는 안정적인 `data-inertia` 키가 있습니다. `@head` 디렉티브는 초기 문서를 렌더링하며, 이후 Inertia는 해당 요소를 관리하고 일반 방문, [instant visits](https://inertiajs.com/docs/v3/the-basics/instant-visits), 뒤로 가기 및 앞으로 가기 탐색 중에 요소를 동기화된 상태로 유지합니다. 요소는 초기 HTML 응답에 포함되므로 크롤러와 링크 미리보기 봇은 JavaScript를 실행하지 않고도 요소를 읽을 수 있습니다. 클라이언트 측 `<Head>` 컴포넌트는 필요하지 않습니다.

<!-- This works with or without [server-side rendering (SSR)](https://inertiajs.com/docs/v3/advanced/server-side-rendering). If your application has a separate SSR entry point, enable `serverHead` there too. Laravel Head automatically deduplicates page-managed elements between `@head` and `<x-inertia::head />`, regardless of their order, while preserving other head elements produced by JavaScript SSR. -->
이는 [server-side rendering (SSR)](https://inertiajs.com/docs/v3/advanced/server-side-rendering) 여부와 관계없이 작동합니다. 애플리케이션에 별도의 SSR 진입점이 있다면 해당 진입점에서도 `serverHead`를 활성화해야 합니다. Laravel Head는 순서와 관계없이 `@head`와 `<x-inertia::head />` 사이에서 페이지가 관리하는 요소의 중복을 자동으로 제거하면서, JavaScript SSR이 생성한 다른 head 요소는 그대로 유지합니다.

> [!NOTE]
> 기존 Inertia 애플리케이션에 Laravel Head를 추가할 때는 `resources/js/app.tsx`와 `resources/js/ssr.tsx`에서 모든 title 콜백을 제거하여 Laravel Head가 최종 문서 제목을 관리하도록 해야 합니다. 또한 Inertia의 [`<Head>` component](https://inertiajs.com/docs/v3/the-basics/title-and-meta)가 관리하는 태그를 Laravel Head로 옮겨 두 도구가 동일한 요소를 정의하지 않도록 해야 합니다.

<!-- The `head` prop is omitted from partial reload responses, so Inertia retains the last full page's head. Instant visits likewise retain the current head until the background response arrives. If your application already uses the `head` prop, change its name in a service provider: -->
부분 재로드 응답에서는 `head` prop이 생략되므로 Inertia는 마지막 전체 페이지의 head를 유지합니다. 즉시 방문에서도 백그라운드 응답이 도착할 때까지 현재 head를 유지합니다. 애플리케이션에서 이미 `head` prop을 사용하고 있다면 서비스 프로바이더에서 이름을 변경합니다:

```php
use Laravel\Head\Facades\Head;

public function boot(): void
{
    Head::inertia(prop: '_head');
}
```

<!-- Then point Inertia at the same prop with `serverHead: '_head'`. -->
그런 다음 `serverHead: '_head'`를 사용해 Inertia가 동일한 prop을 가리키도록 설정합니다.

<a name="static-inertia-tags"></a>
<!-- #### Static Inertia Tags -->
#### Static Inertia Tags

<!-- Most tags should live in defaults, route metadata, or runtime metadata so Laravel Head can resolve the right value for each page. Use Inertia globals only for document tags rendered in the first HTML response and left unchanged by Inertia for the rest of the session. -->
대부분의 태그는 기본값, 라우트 메타데이터 또는 런타임 메타데이터에 정의해야 Laravel Head가 각 페이지에 맞는 값을 확인할 수 있습니다. Inertia 전역 변수는 첫 번째 HTML 응답에서 렌더링되고 나머지 세션 동안 Inertia가 변경하지 않는 문서 태그에만 사용하세요.

<!-- Register them in a service provider with `Head::inertiaGlobals()`: -->
서비스 프로바이더에서 `Head::inertiaGlobals()`를 사용해 등록합니다:

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
Inertia 전역은 `head` prop에서 제외되고 `data-inertia` 소유권 속성 없이 렌더링되며 첫 번째 응답 이후에는 업데이트되지 않습니다. 이러한 전역은 뷰포트, 색 구성표, 파비콘, 터치 아이콘, 매니페스트처럼 안정적인 브라우저 힌트에 적합합니다. 태그가 페이지별로 다르거나 SEO와 관련이 있거나 나중에 재정의될 수 있다면 대신 `defaults`, 라우트 메타데이터 또는 런타임 메타데이터에 지정하세요.

<!-- Applications that need the resolved metadata as structured data instead of rendered tags may call `Head::toArray()`. The returned data includes titles, Open Graph values, JSON-LD schemas, and other resolved metadata. -->
렌더링된 태그 대신 확인된 메타데이터를 구조화된 데이터로 사용해야 하는 애플리케이션은 `Head::toArray()`를 호출할 수 있습니다. 반환되는 데이터에는 제목, Open Graph 값, JSON-LD 스키마 및 기타 확인된 메타데이터가 포함됩니다.
