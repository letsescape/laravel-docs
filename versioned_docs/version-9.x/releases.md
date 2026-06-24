<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 9](#laravel-9)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~February), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel과 그 외 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 주요 프레임워크 릴리스는 매년(약 2월경) 한 번씩 진행되며, 마이너 또는 패치 릴리스는 매주 출시될 수 있습니다. 마이너 및 패치 릴리스에는 **절대** 호환성 문제를 일으키는 변경 사항이 포함되지 않습니다.

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^9.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 컴포넌트를 참조할 때는 항상 `^9.0` 과 같은 버전 제약을 사용해야 합니다. 이는 Laravel의 주요 버전 업그레이드에서는 호환성 깨짐(breaking changes)이 발생할 수 있기 때문입니다. 하지만, 주요 버전으로 업그레이드할 때도 하루 이내로 마이그레이션할 수 있도록 최대한 노력하고 있습니다.

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 보장 정책에 포함되지 않습니다. Laravel 코드베이스의 품질 향상을 위해 필요시 함수 인수명을 변경할 수 있습니다. 따라서, Laravel의 메서드를 호출할 때 네임드 인수를 사용할 경우, 향후 인수명이 변경될 수 있음을 염두에 두고 주의해서 사용해야 합니다.

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/9.x/database#introduction). -->
모든 Laravel 릴리스는 18개월간 버그 수정, 2년간 보안 패치가 제공됩니다. Lumen을 포함한 모든 추가 라이브러리에서는 최신 주요 버전만이 버그 수정을 받습니다. 또한, Laravel이 지원하는 데이터베이스 버전도 반드시 [supported by Laravel](/docs/9.x/database#introduction)에서 확인해 주세요.

| 버전 | PHP (*) | 릴리스 | 버그 수정 지원 종료 | 보안 패치 지원 종료 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2 - 8.0 | 2019년 9월 3일 | 2022년 1월 25일 | 2022년 9월 6일 |
| 7 | 7.2 - 8.0 | 2020년 3월 3일 | 2020년 10월 6일 | 2021년 3월 3일 |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |

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
(*) 지원되는 PHP 버전

<a name="laravel-9"></a>
<!-- ## Laravel 9 -->
## Laravel 9

<!-- As you may know, Laravel transitioned to yearly releases with the release of Laravel 8. Previously, major versions were released every 6 months. This transition is intended to ease the maintenance burden on the community and challenge our development team to ship amazing, powerful new features without introducing breaking changes. Therefore, we have shipped a variety of robust features to Laravel 8 without breaking backwards compatibility, such as parallel testing support, improved Breeze starter kits, HTTP client improvements, and even new Eloquent relationship types such as "has one of many". -->
알고 계시듯, Laravel은 Laravel 8 릴리스부터 연 1회 주요 버전 출시 정책으로 전환하였습니다. 이전에는 6개월마다 주요 버전이 출시되었습니다. 이 전환의 목적은 커뮤니티의 유지 보수 부담을 덜고, 개발팀이 기존에 호환성 문제 없이 멋진 신규 기능을 더 자주 추가할 수 있도록 하기 위함입니다. 실제로 Laravel 8에서도 병렬 테스트 지원, Breeze 스타터 킷 개선, HTTP 클라이언트 개선, "has one of many" 등 새로운 Eloquent 연관관계 유형 등 다양한 강력한 기능을 하위 호환성을 깨뜨리지 않고 제공했습니다.

<!-- Therefore, this commitment to ship great new features during the current release will likely lead to future "major" releases being primarily used for "maintenance" tasks such as upgrading upstream dependencies, which can be seen in these release notes. -->
따라서, 이 릴리스 정책 아래에서는 향후 "주요" 릴리스가 주로 상위 의존성 업그레이드 등 "유지 보수" 성격의 변경(주로 breaking change와 연관)만을 포함하는 형태가 될 가능성이 높습니다. 바로 이 점이 본 릴리스 노트에도 반영되어 있습니다.

<!-- Laravel 9 continues the improvements made in Laravel 8.x by introducing support for Symfony 6.0 components, Symfony Mailer, Flysystem 3.0, improved `route:list` output, a Laravel Scout database driver, new Eloquent accessor / mutator syntax, implicit route bindings via Enums, and a variety of other bug fixes and usability improvements. -->
Laravel 9은 Laravel 8.x에서 도입된 개선 사항을 이어받아, Symfony 6.0 컴포넌트 및 Symfony Mailer 지원, Flysystem 3.0, 향상된 `route:list` 출력, Laravel Scout 데이터베이스 드라이버, 새로운 Eloquent Accessor·Mutator 문법, Enum을 활용한 암묵적(implicit) 라우트 바인딩, 기타 여러 버그 수정과 개발 편의성 개선 등을 제공합니다.

<a name="php-8"></a>
<!-- ### PHP 8.0 -->
### PHP 8.0

<!-- Laravel 9.x requires a minimum PHP version of 8.0. -->
Laravel 9.x를 사용하려면 최소 PHP 8.0 버전이 필요합니다.

<a name="symfony-mailer"></a>
<!-- ### Symfony Mailer -->
### Symfony Mailer

<!-- _Symfony Mailer support was contributed by [Dries Vints](https://github.com/driesvints)_, [James Brooks](https://github.com/jbrooksuk), and [Julius Kiekbusch](https://github.com/Jubeki). -->
_Symfony Mailer 지원은 [Dries Vints](https://github.com/driesvints)_, [James Brooks](https://github.com/jbrooksuk), [Julius Kiekbusch](https://github.com/Jubeki)이 기여하였습니다.

<!-- Previous releases of Laravel utilized the [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html) library to send outgoing email. However, that library is no longer maintained and has been succeeded by Symfony Mailer. -->
기존 Laravel 릴리스에서는 [Swift Mailer](https://swiftmailer.symfony.com/docs/introduction.html) 라이브러리를 사용해 이메일을 발송했습니다. 하지만 Swift Mailer는 더 이상 유지보수가 되지 않으며, Symfony Mailer로 대체되었습니다.

<!-- Please review the [upgrade guide](/docs/9.x/upgrade#symfony-mailer) to learn more about ensuring your application is compatible with Symfony Mailer. -->
애플리케이션이 Symfony Mailer와 호환되는지 확인하려면 [upgrade guide](/docs/9.x/upgrade#symfony-mailer)를 참고해 주세요.

<a name="flysystem-3"></a>
<!-- ### Flysystem 3.x -->
### Flysystem 3.x

<!-- _Flysystem 3.x support was contributed by [Dries Vints](https://github.com/driesvints)_. -->
_Flysystem 3.x 지원은 [Dries Vints](https://github.com/driesvints)가 기여하였습니다._

<!-- Laravel 9.x upgrades our upstream Flysystem dependency to Flysystem 3.x. Flysystem powers all of filesystem interactions offered by the `Storage` facade. -->
Laravel 9.x는 Flysystem의 상위 의존성을 Flysystem 3.x로 업그레이드했습니다. Flysystem은 `Storage` 파사드를 통해 제공되는 모든 파일 시스템 기능의 핵심 역할을 합니다.

<!-- Please review the [upgrade guide](/docs/9.x/upgrade#flysystem-3) to learn more about ensuring your application is compatible with Flysystem 3.x. -->
Flysystem 3.x와 호환되는지 확인하려면 [upgrade guide](/docs/9.x/upgrade#flysystem-3)를 참고하세요.

<a name="eloquent-accessors-and-mutators"></a>
<!-- ### Improved Eloquent Accessors / Mutators -->
### Improved Eloquent Accessors / Mutators

<!-- _Improved Eloquent accessors / mutators was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_Eloquent Accessor/Mutator 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- Laravel 9.x offers a new way to define Eloquent [accessors and mutators](/docs/9.x/eloquent-mutators#accessors-and-mutators). In previous releases of Laravel, the only way to define accessors and mutators was by defining prefixed methods on your model like so: -->
Laravel 9.x는 Eloquent [accessors and mutators](/docs/9.x/eloquent-mutators#accessors-and-mutators)를 정의하는 새로운 방법을 제공합니다. 이전에는 아래와 같이 접두사가 붙은 메서드를 통해서만 Accessor, Mutator를 정의할 수 있었습니다:

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
Laravel 9.x에서는 반환 타입을 `Illuminate\Database\Eloquent\Casts\Attribute`로 지정한, 접두사가 없는 단일 메서드로 Accessor와 Mutator를 함께 정의할 수 있습니다.

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
또한, 이 방식으로 정의된 Accessor는 반환된 객체 값이 [custom cast classes](/docs/9.x/eloquent-mutators#custom-casts)처럼 캐싱됩니다.

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
> Enum casting은 PHP 8.1 이상에서만 지원됩니다.

<!-- _Enum casting was contributed by [Mohamed Said](https://github.com/themsaid)_. -->
_Enum casting은 [Mohamed Said](https://github.com/themsaid)가 기여하였습니다._

<!-- Eloquent now allows you to cast your attribute values to PHP ["backed" Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `$casts` property array: -->
이제 Eloquent에서 속성 값을 PHP ["backed" Enums](https://www.php.net/manual/en/language.enumerations.backed.php)으로 casting할 수 있도록 지원합니다. 사용하려면, 모델의 `$casts` 속성 배열에 해당 속성과 연결할 Enum 클래스를 지정해주면 됩니다.

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
cast가 지정되면 해당 속성은 Enum 인스턴스로 자동 변환되어 접근·저장할 수 있습니다.

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
_암묵적 Enum 바인딩은 [Nuno Maduro](https://github.com/nunomaduro)가 기여하였습니다._

<!-- PHP 8.1 introduces support for [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). Laravel 9.x introduces the ability to type-hint an Enum on your route definition and Laravel will only invoke the route if that route segment is a valid Enum value in the URI. Otherwise, an HTTP 404 response will be returned automatically. For example, given the following Enum: -->
PHP 8.1부터 [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)이 도입되었습니다. Laravel 9.x에서는 라우트 정의에 type-hint로 Enum을 지정하면, 해당 세그먼트가 Enum의 값 중 하나일 때만 라우트가 정상적으로 실행됩니다. 그렇지 않은 경우에는 자동으로 HTTP 404 응답이 반환됩니다. 예를 들어, 아래와 같은 Enum이 있다고 가정해봅시다:

```php
enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

<!-- You may define a route that will only be invoked if the `{category}` route segment is `fruits` or `people`. Otherwise, an HTTP 404 response will be returned: -->
이 Enum을 사용해 `{category}` 구간이 `fruits` 또는 `people`일 때만 라우트가 실행됩니다. 그 외 값일 경우 자동으로 HTTP 404가 반환됩니다.

```php
Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="forced-scoping-of-route-bindings"></a>
<!-- ### Forced Scoping Of Route Bindings -->
### Forced Scoping Of Route Bindings

<!-- _Forced scoped bindings was contributed by [Claudio Dekker](https://github.com/claudiodekker)_. -->
_강제 스코프 바인딩은 [Claudio Dekker](https://github.com/claudiodekker)가 기여하였습니다._

<!-- In previous releases of Laravel, you may wish to scope the second Eloquent model in a route definition such that it must be a child of the previous Eloquent model. For example, consider this route definition that retrieves a blog post by slug for a specific user: -->
기존 Laravel에서는 중첩된 라우트 파라미터에서 두 번째 Eloquent 모델이 반드시 첫 번째 모델의 하위(자식)여야 할 때, 즉 특정 사용자의 특정 블로그 포스트를 slug로 조회하는 등의 상황에서 바인딩 스코프를 설정할 수 있었습니다:

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. However, this behavior was only previously supported by Laravel when a custom key was used for the child route binding. -->
이렇게 커스텀 키를 사용한 자식 바인딩에서는 부모와의 연관관계를 자동으로 추측해서 쿼리가 제한되었습니다. 하지만, 커스텀 키를 지정하지 않은 경우에는 이전 버전에서는 적용되지 않았습니다.

<!-- However, in Laravel 9.x, you may now instruct Laravel to scope "child" bindings even when a custom key is not provided. To do so, you may invoke the `scopeBindings` method when defining your route: -->
Laravel 9.x부터는 커스텀 키를 사용하지 않아도 "자식" 바인딩의 스코핑을 강제로 적용할 수 있습니다. 라우트 정의 시 `scopeBindings` 메서드를 호출하면 됩니다.

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

<!-- Or, you may instruct an entire group of route definitions to use scoped bindings: -->
또는, 라우트 그룹 전체에 대해 스코프 바인딩을 적용할 수도 있습니다.

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
_라우트 그룹 개선은 [Luke Downing](https://github.com/lukeraymonddowning)이 기여하였습니다._

<!-- You may now use the `controller` method to define the common controller for all of the routes within the group. Then, when defining the routes, you only need to provide the controller method that they invoke: -->
이제 `controller` 메서드를 사용해 그룹 내 모든 라우트에 공통 컨트롤러를 지정할 수 있습니다. 각 라우트에서는 호출할 컨트롤러 메서드명만 명시하면 됩니다.

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
_전체 텍스트 인덱스/where 절 기능은 [Taylor Otwell](https://github.com/taylorotwell), [Dries Vints](https://github.com/driesvints)가 기여하였습니다._

<!-- When using MySQL or PostgreSQL, the `fullText` method may now be added to column definitions to generate full text indexes: -->
MySQL 또는 PostgreSQL을 사용할 때, 칼럼 정의에 `fullText` 메서드를 추가해 전체 텍스트 인덱스를 생성할 수 있습니다.

```
$table->text('bio')->fullText();
```

<!-- In addition, the `whereFullText` and `orWhereFullText` methods may be used to add full text "where" clauses to a query for columns that have [full text indexes](/docs/9.x/migrations#available-index-types). These methods will be transformed into the appropriate SQL for the underlying database system by Laravel. For example, a `MATCH AGAINST` clause will be generated for applications utilizing MySQL: -->
또한, `whereFullText`, `orWhereFullText` 메서드를 사용하면 [full text indexes](/docs/9.x/migrations#available-index-types)가 설정된 칼럼에 쿼리할 수 있습니다. 이 메서드는 데이터베이스 종류에 맞는 SQL로 자동 변환됩니다. 예를 들어 MySQL에선 아래와 같이 `MATCH AGAINST` 구문이 사용됩니다.

```
$users = DB::table('users')
           ->whereFullText('bio', 'web developer')
           ->get();
```

<a name="laravel-scout-database-engine"></a>
<!-- ### Laravel Scout Database Engine -->
### Laravel Scout Database Engine

<!-- _The Laravel Scout database engine was contributed by [Taylor Otwell](https://github.com/taylorotwell) and [Dries Vints](https://github.com/driesvints)_. -->
_Laravel Scout 데이터베이스 엔진 지원은 [Taylor Otwell](https://github.com/taylorotwell), [Dries Vints](https://github.com/driesvints)가 기여하였습니다._

<!-- If your application interacts with small to medium sized databases or has a light workload, you may now use Scout's "database" engine instead of a dedicated search service such as Algolia or MeiliSearch. The database engine will use "where like" clauses and full text indexes when filtering results from your existing database to determine the applicable search results for your query. -->
애플리케이션에서 소규모~중간 규모의 데이터베이스를 사용하거나, 워크로드가 적을 경우, 별도의 검색 엔진(예: Algolia, MeiliSearch) 대신 Scout의 "database" 엔진을 사용할 수 있습니다. 이 엔진은 기존 데이터베이스에서 "where like" 쿼리 및 전체 텍스트 인덱스를 이용해 검색 결과를 필터링합니다.

<!-- To learn more about the Scout database engine, consult the [Scout documentation](/docs/9.x/scout). -->
Scout 데이터베이스 엔진에 대한 자세한 내용은 [Scout documentation](/docs/9.x/scout)를 참고하세요.

<a name="rendering-inline-blade-templates"></a>
<!-- ### Rendering Inline Blade Templates -->
### Rendering Inline Blade Templates

<!-- _Rendering inline Blade templates was contributed by [Jason Beggs](https://github.com/jasonlbeggs). Rendering inline Blade components was contributed by [Toby Zerner](https://github.com/tobyzerner)_. -->
_인라인 Blade 템플릿 렌더링 기능은 [Jason Beggs](https://github.com/jasonlbeggs), 인라인 Blade 컴포넌트 렌더링 기능은 [Toby Zerner](https://github.com/tobyzerner)가 기여하였습니다._

<!-- Sometimes you may need to transform a raw Blade template string into valid HTML. You may accomplish this using the `render` method provided by the `Blade` facade. The `render` method accepts the Blade template string and an optional array of data to provide to the template: -->
가끔 Blade 템플릿 문자열을 HTML로 변환해야 할 때가 있습니다. `Blade` 파사드의 `render` 메서드를 사용하면 이를 쉽게 구현할 수 있습니다. `render`는 Blade 템플릿 문자열과, 선택적으로 해당 템플릿에 전달할 데이터 배열을 인자로 받습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

<!-- Similarly, the `renderComponent` method may be used to render a given class component by passing the component instance to the method: -->
비슷하게, `renderComponent` 메서드를 사용하면 클래스 컴포넌트 인스턴스를 전달하여 렌더할 수 있습니다.

```php
use App\View\Components\HelloComponent;

return Blade::renderComponent(new HelloComponent('Julian Bashir'));
```

<a name="slot-name-shortcut"></a>
<!-- ### Slot Name Shortcut -->
### Slot Name Shortcut

<!-- _Slot name shortcuts were contributed by [Caleb Porzio](https://github.com/calebporzio)._ -->
_슬롯 이름 단축 문법은 [Caleb Porzio](https://github.com/calebporzio)가 기여하였습니다._

<!-- In previous releases of Laravel, slot names were provided using a `name` attribute on the `x-slot` tag: -->
이전에는 `x-slot` 태그의 `name` 속성으로 슬롯 이름을 지정해야 했습니다.

```blade
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- However, beginning in Laravel 9.x, you may specify the slot's name using a convenient, shorter syntax: -->
Laravel 9.x부터는 아래와 같이 더 간결하게 슬롯 이름을 지정할 수 있습니다.

```xml
<x-slot:title>
    Server Error
</x-slot>
```

<a name="checked-selected-blade-directives"></a>
<!-- ### Checked / Selected Blade Directives -->
### Checked / Selected Blade Directives

<!-- _Checked and selected Blade directives were contributed by [Ash Allen](https://github.com/ash-jc-allen) and [Taylor Otwell](https://github.com/taylorotwell)_. -->
_@checked 및 @selected Blade 지시어는 [Ash Allen](https://github.com/ash-jc-allen), [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- For convenience, you may now use the `@checked` directive to easily indicate if a given HTML checkbox input is "checked". This directive will echo `checked` if the provided condition evaluates to `true`: -->
이제 `@checked` 지시어를 사용해, HTML 체크박스 인풋이 체크되어 있는지 쉽게 표현할 수 있습니다. 지정한 조건이 `true`이면 `checked`가 자동으로 출력됩니다.

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

<!-- Likewise, the `@selected` directive may be used to indicate if a given select option should be "selected": -->
마찬가지로, `@selected` 지시어는 주어진 select 옵션이 선택되어야 하는지 쉽게 지정할 수 있습니다.

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
_Bootstrap 5 페이지네이션 뷰는 [Jared Lewis](https://github.com/jrd-lewis)가 기여하였습니다._

<!-- Laravel now includes pagination views built using [Bootstrap 5](https://getbootstrap.com/). To use these views instead of the default Tailwind views, you may call the paginator's `useBootstrapFive` method within the `boot` method of your `App\Providers\AppServiceProvider` class: -->
Laravel은 이제 [Bootstrap 5](https://getbootstrap.com/)로 구현된 페이지네이션 뷰도 기본 제공합니다. 기본 Tailwind 뷰 대신 이를 사용하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 paginator의 `useBootstrapFive` 메서드를 호출하면 됩니다.

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
_중첩 배열 입력에 대한 유효성 검사 개선은 [Steve Bauman](https://github.com/stevebauman)이 기여하였습니다._

<!-- Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may now accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element: -->
유효성 검사 규칙에서 중첩 배열 요소의 값을 참조해야 할 때가 있습니다. 이제 `Rule::forEach` 메서드를 사용해 이런 유효성 검사를 쉽게 구현할 수 있습니다. `forEach`는 배열 요소마다 클로저를 호출하며, 해당 요소의 값과 완전한 속성명을 인자로 전달합니다. 클로저는 반환된 배열에 해당 요소에 적용할 규칙을 명시합니다.

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
_Laravel Breeze API 스캐폴딩과 Next.js 스타터 킷은 [Taylor Otwell](https://github.com/taylorotwell), [Miguel Piedrafita](https://twitter.com/m1guelpf)가 기여하였습니다._

<!-- The [Laravel Breeze](/docs/9.x/starter-kits#breeze-and-next) starter kit has received an "API" scaffolding mode and complimentary [Next.js](https://nextjs.org) [frontend implementation](https://github.com/laravel/breeze-next). This starter kit scaffolding may be used to jump start your Laravel applications that are serving as a backend, Laravel Sanctum authenticated API for a JavaScript frontend. -->
[Laravel Breeze](/docs/9.x/starter-kits#breeze-and-next) 스타터 킷에 "API" 스캐폴딩 모드가 추가되었으며, 이를 활용한 [Next.js](https://nextjs.org) [frontend implementation](https://github.com/laravel/breeze-next)도 함께 제공됩니다. 이 스캐폴딩은 자바스크립트 프론트엔드와 Laravel Sanctum 인증 API로 백엔드를 구성하려는 프로젝트의 시작점으로 활용할 수 있습니다.

<a name="exception-page"></a>
<!-- ### Improved Ignition Exception Page -->
### Improved Ignition Exception Page

<!-- _Ignition is developed by [Spatie](https://spatie.be/)._ -->
_Ignition은 [Spatie](https://spatie.be/)에서 개발한 오픈소스 예외 디버깅 페이지입니다._

<!-- Ignition, the open source exception debug page created by Spatie, has been redesigned from the ground up. The new, improved Ignition ships with Laravel 9.x and includes light / dark themes, customizable "open in editor" functionality, and more. -->
Ignition 예외 디버그 페이지가 완전히 새롭게 리디자인되었습니다. 새 버전은 Laravel 9.x에 기본 포함되며, 라이트/다크 테마, "에디터에서 열기" 기능 커스터마이즈 등 다양한 기능이 개선되었습니다.

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
_향상된 `route:list` CLI 출력은 [Nuno Maduro](https://github.com/nunomaduro)가 기여하였습니다._

<!-- The `route:list` CLI output has been significantly improved for the Laravel 9.x release, offering a beautiful new experience when exploring your route definitions. -->
Laravel 9.x에서 `route:list` CLI 출력이 크게 개선되어, 라우트 정의를 더 직관적이고 아름답게 확인할 수 있게 되었습니다.

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
_Artisan `test` 명령어의 테스트 커버리지 기능은 [Nuno Maduro](https://github.com/nunomaduro)가 기여하였습니다._

<!-- The Artisan `test` command has received a new `--coverage` option that you may use to explore the amount of code coverage your tests are providing to your application: -->
Artisan `test` 명령어에 `--coverage` 옵션이 추가되어, 테스트가 코드의 어느 부분까지 커버하는지 CLI에서 바로 확인할 수 있습니다.

```shell
php artisan test --coverage
```

<!-- The test coverage results will be displayed directly within the CLI output. -->
테스트 커버리지 결과는 CLI 출력에 바로 표시됩니다.

<!--
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>
-->
<p align="center">
<img width="100%" src="https://user-images.githubusercontent.com/5457236/150133237-440290c2-3538-4d8e-8eac-4fdd5ec7bd9e.png"/>
</p>

<!-- In addition, if you would like to specify a minimum threshold that your test coverage percentage must meet, you may use the `--min` option. The test suite will fail if the given minimum threshold is not met: -->
또한, 테스트 커버리지 비율이 지정한 최소값에 미달하면 실패하도록 강제하는 `--min` 옵션도 제공합니다.

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
_Soketi Echo 서버는 [Alex Renoki](https://github.com/rennokki)가 개발하였습니다._

<!-- Although not exclusive to Laravel 9.x, Laravel has recently assisted with the documentation of Soketi, a [Laravel Echo](/docs/9.x/broadcasting) compatible Web Socket server written for Node.js. Soketi provides a great, open source alternative to Pusher and Ably for those applications that prefer to manage their own Web Socket server. -->
Laravel 9.x 전용 기능은 아니지만, 최근 Laravel에서는 [Laravel Echo](/docs/9.x/broadcasting)와 호환되는 Node.js 기반 Web Socket 서버인 Soketi의 문서화 작업에 기여하였습니다. Soketi는 푸셔(Pusher), Ably 등 상용 서비스 대신 자체적으로 Web Socket 서버를 운영하고 싶은 애플리케이션에 적합한 오픈소스 대안입니다.

<!-- For more information on using Soketi, please consult the [broadcasting documentation](/docs/9.x/broadcasting) and [Soketi documentation](https://docs.soketi.app/). -->
Soketi 사용 방법은 [broadcasting documentation](/docs/9.x/broadcasting)와 [Soketi documentation](https://docs.soketi.app/)를 참고하세요.

<a name="improved-collections-ide-support"></a>
<!-- ### Improved Collections IDE Support -->
### Improved Collections IDE Support

<!-- _Improved collections IDE support was contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_컬렉션 IDE 지원 개선은 [Nuno Maduro](https://github.com/nunomaduro)가 기여하였습니다._

<!-- Laravel 9.x adds improved, "generic" style type definitions to the collections component, improving IDE and static analysis support. IDEs such as [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections) or static analysis tools such as [PHPStan](https://phpstan.org) will now better understand Laravel collections natively. -->
Laravel 9.x는 컬렉션 컴포넌트에 "제너릭(Generic)" 스타일의 타입 정의가 추가되어, IDE와 정적 분석 도구에서 컬렉션 코드를 더욱 똑똑하게 지원합니다. [PHPStorm](https://blog.jetbrains.com/phpstorm/2021/12/phpstorm-2021-3-release/#support_for_future_laravel_collections)과 [PHPStan](https://phpstan.org) 같은 도구에서 더 뛰어난 코드 완성, 분석이 가능합니다.

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
Laravel 9.x에는 개발에 유용한 두 가지 신규 헬퍼 함수가 추가되었습니다.

<a name="new-helpers-str"></a>
<!-- #### `str` -->
#### `str`

<!-- The `str` function returns a new `Illuminate\Support\Stringable` instance for the given string. This function is equivalent to the `Str::of` method: -->
`str` 함수는 주어진 문자열을 `Illuminate\Support\Stringable` 인스턴스로 반환합니다. 이는 `Str::of` 메서드와 동일합니다.

```
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<!-- If no argument is provided to the `str` function, the function returns an instance of `Illuminate\Support\Str`: -->
인자를 생략하면 `str` 함수는 `Illuminate\Support\Str` 인스턴스를 반환합니다.

```
$snake = str()->snake('LaravelFramework');

// 'laravel_framework'
```

<a name="new-helpers-to-route"></a>
<!-- #### `to_route` -->
#### `to_route`

<!-- The `to_route` function generates a redirect HTTP response for a given named route, providing an expressive way to redirect to named routes from your routes and controllers: -->
`to_route` 함수는 지정한 이름의 라우트로 리다이렉트하는 HTTP 응답을 생성합니다. 라우트 및 컨트롤러에서 명확하게 리다이렉트할 수 있도록 도와줍니다.

```
return to_route('users.show', ['user' => 1]);
```

<!-- If necessary, you may pass the HTTP status code that should be assigned to the redirect and any additional response headers as the third and fourth arguments to the to_route method: -->
필요하다면, 세 번째·네 번째 인자를 통해 리다이렉트 시 사용할 HTTP 상태 코드와 추가 응답 헤더도 지정할 수 있습니다.

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```
