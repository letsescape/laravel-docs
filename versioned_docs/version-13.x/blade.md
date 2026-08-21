<!-- # Blade Templates -->
# Blade Templates

- [Introduction](#introduction)
    - [Supercharging Blade With Livewire](#supercharging-blade-with-livewire)
- [Displaying Data](#displaying-data)
    - [HTML Entity Encoding](#html-entity-encoding)
    - [Blade and JavaScript Frameworks](#blade-and-javascript-frameworks)
- [Blade Directives](#blade-directives)
    - [If Statements](#if-statements)
    - [Switch Statements](#switch-statements)
    - [Loops](#loops)
    - [The Loop Variable](#the-loop-variable)
    - [Conditional Classes](#conditional-classes)
    - [Additional Attributes](#additional-attributes)
    - [Including Subviews](#including-subviews)
    - [The `@once` Directive](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [Fonts](#fonts)
    - [Comments](#comments)
- [Components](#components)
    - [Rendering Components](#rendering-components)
    - [Index Components](#index-components)
    - [Passing Data to Components](#passing-data-to-components)
    - [Component Attributes](#component-attributes)
    - [Reserved Keywords](#reserved-keywords)
    - [Slots](#slots)
    - [Inline Component Views](#inline-component-views)
    - [Dynamic Components](#dynamic-components)
    - [Manually Registering Components](#manually-registering-components)
- [Anonymous Components](#anonymous-components)
    - [Anonymous Index Components](#anonymous-index-components)
    - [Data Properties / Attributes](#data-properties-attributes)
    - [Accessing Parent Data](#accessing-parent-data)
    - [Anonymous Component Paths](#anonymous-component-paths)
- [Building Layouts](#building-layouts)
    - [Layouts Using Components](#layouts-using-components)
    - [Layouts Using Template Inheritance](#layouts-using-template-inheritance)
- [Forms](#forms)
    - [CSRF Field](#csrf-field)
    - [Method Field](#method-field)
    - [Validation Errors](#validation-errors)
- [Stacks](#stacks)
- [Service Injection](#service-injection)
- [Rendering Inline Blade Templates](#rendering-inline-blade-templates)
- [Rendering Blade Fragments](#rendering-blade-fragments)
- [Extending Blade](#extending-blade)
    - [Custom Echo Handlers](#custom-echo-handlers)
    - [Custom If Statements](#custom-if-statements)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Blade is the simple, yet powerful templating engine that is included with Laravel. Unlike some PHP templating engines, Blade does not restrict you from using plain PHP code in your templates. In fact, all Blade templates are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade template files use the `.blade.php` file extension and are typically stored in the `resources/views` directory. -->
Blade는 Laravel에 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리 Blade는 템플릿에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 일반 PHP 코드로 컴파일되고 수정될 때까지 캐시됩니다. 즉, Blade는 기본적으로 애플리케이션에 오버헤드가 전혀 추가되지 않습니다. Blade 템플릿 파일은 `.blade.php` 파일 확장자를 사용하며 일반적으로 `resources/views` 디렉터리에 저장됩니다.

<!-- Blade views may be returned from routes or controllers using the global `view` helper. Of course, as mentioned in the documentation on [views](/docs/13.x/views), data may be passed to the Blade view using the `view` helper's second argument: -->
Blade 뷰는 전역 `view` 도우미를 사용하여 라우트 또는 컨트롤러에서 반환될 수 있습니다. 물론 [views](/docs/13.x/views) 문서에 언급된 대로 데이터는 `view` 도우미의 두 번째 인수를 사용하여 Blade 뷰에 전달될 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
<!-- ### Supercharging Blade With Livewire -->
### Supercharging Blade With Livewire

<!-- Want to take your Blade templates to the next level and build dynamic interfaces with ease? Check out [Laravel Livewire](https://livewire.laravel.com). Livewire allows you to write Blade components that are augmented with dynamic functionality that would typically only be possible via frontend frameworks like React, Svelte, or Vue, providing a great approach to building modern, reactive frontends without the complexities, client-side rendering, or build steps of many JavaScript frameworks. -->
Blade 템플릿을 한 단계 더 발전시키고 동적 인터페이스를 쉽게 구축하고 싶으십니까? [Laravel Livewire](https://livewire.laravel.com)를 확인하세요. Livewire를 사용하면 일반적으로 React, Svelte 또는 Vue와 같은 프론트엔드 프레임워크를 통해서만 가능한 동적 기능으로 강화된 Blade 컴포넌트를 작성할 수 있으며, 이는 복잡성, 클라이언트 측 렌더링 또는 많은 JavaScript 프레임워크의 구축 단계 없이 현대적이고 반응적인 프론트엔드를 구축하는 훌륭한 접근 방식을 제공합니다.

<a name="displaying-data"></a>
<!-- ## Displaying Data -->
## Displaying Data

<!-- You may display data that is passed to your Blade views by wrapping the variable in curly braces. For example, given the following route: -->
변수를 중괄호로 묶어 Blade 뷰에 전달된 데이터를 표시할 수 있습니다. 예를 들어, 다음 라우트가 주어지면:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

<!-- You may display the contents of the `name` variable like so: -->
다음과 같이 `name` 변수의 내용을 표시할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 에코 문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 기능을 통해 자동으로 전송됩니다.

<!-- You are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement: -->
뷰에 전달된 변수의 내용을 표시하는 것으로 제한되지는 않습니다. PHP 함수의 결과를 에코할 수도 있습니다. 실제로 Blade echo 문 안에 원하는 PHP 코드를 넣을 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
<!-- ### HTML Entity Encoding -->
### HTML Entity Encoding

<!-- By default, Blade (and the Laravel `e` function) will double encode HTML entities. If you would like to disable double encoding, call the `Blade::withoutDoubleEncoding` method from the `boot` method of your `AppServiceProvider`: -->
기본적으로 Blade(및 Laravel `e` 함수)는 HTML 엔터티를 이중으로 인코딩합니다. 이중 인코딩을 비활성화하려면 `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
<!-- #### Displaying Unescaped Data -->
#### Displaying Unescaped Data

<!-- By default, Blade `{{ }}` statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax: -->
기본적으로 Blade `{{ }}` 문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 기능을 통해 자동으로 전송됩니다. 데이터가 이스케이프되는 것을 원하지 않으면 다음 구문을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자가 제공한 콘텐츠를 에코할 때는 매우 주의하세요. 사용자 제공 데이터를 표시할 때 XSS 공격을 방지하려면 일반적으로 이스케이프된 이중 중괄호 구문을 사용해야 합니다.

<a name="blade-and-javascript-frameworks"></a>
<!-- ### Blade and JavaScript Frameworks -->
### Blade and JavaScript Frameworks

<!-- Since many JavaScript frameworks also use "curly" braces to indicate a given expression should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example: -->
많은 JavaScript 프레임워크는 주어진 표현식이 브라우저에 표시되어야 함을 나타내기 위해 "중괄호"를 사용하므로 `@` 기호를 사용하여 표현식이 그대로 유지되어야 함을 Blade 렌더링 엔진에 알릴 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

<!-- In this example, the `@` symbol will be removed by Blade; however, the `{{ name }}` expression will remain untouched by the Blade engine, allowing it to be rendered by your JavaScript framework. -->
이 예에서 `@` 기호는 Blade에 의해 제거됩니다. 그러나 `{{ name }}` 표현식은 Blade 엔진의 영향을 받지 않고 그대로 유지되므로 JavaScript 프레임워크에서 렌더링할 수 있습니다.

<!-- The `@` symbol may also be used to escape Blade directives: -->
`@` 기호는 Blade 지시문을 이스케이프하는 데 사용될 수도 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
<!-- #### Rendering JSON -->
#### Rendering JSON

<!-- Sometimes you may pass an array to your view with the intention of rendering it as JSON in order to initialize a JavaScript variable. For example: -->
때로는 JavaScript 변수를 초기화하기 위해 배열을 JSON로 렌더링하려는 의도로 뷰에 배열을 전달할 수도 있습니다. 예를 들어:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

<!-- However, instead of manually calling `json_encode`, you may use the `Illuminate\Support\Js::from` method. The `from` method accepts the same arguments as PHP's `json_encode` function; however, it will ensure that the resulting JSON has been properly escaped for inclusion within HTML quotes. The `from` method will return a string `JSON.parse` JavaScript statement that will convert the given object or array into a valid JavaScript object: -->
그러나 `json_encode`를 수동으로 호출하는 대신 `Illuminate\Support\Js::from` 메서드를 사용할 수도 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 허용합니다. 그러나 결과 JSON가 HTML 인용문에 포함되도록 올바르게 이스케이프되었는지 확인합니다. `from` 메소드는 주어진 개체 또는 배열을 유효한 JavaScript 개체로 변환하는 문자열 `JSON.parse` JavaScript 문을 반환합니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

<!-- The latest versions of the Laravel application skeleton include a `Js` facade, which provides convenient access to this functionality within your Blade templates: -->
Laravel 애플리케이션 스켈레톤의 최신 버전에는 `Js` 외관이 포함되어 있어 Blade 템플릿 내에서 이 기능에 편리하게 액세스할 수 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> 기존 변수를 JSON로 렌더링하려면 `Js::from` 메서드만 사용해야 합니다. Blade 템플릿은 정규식을 기반으로 하며 복잡한 표현식을 지시문에 전달하려고 하면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
<!-- #### The `@verbatim` Directive -->
#### The `@verbatim` Directive

<!-- If you are displaying JavaScript variables in a large portion of your template, you may wrap the HTML in the `@verbatim` directive so that you do not have to prefix each Blade echo statement with an `@` symbol: -->
템플릿의 많은 부분에 JavaScript 변수를 표시하는 경우 각 Blade 에코 문 앞에 `@` 기호를 붙일 필요가 없도록 HTML을 `@verbatim` 지시어로 래핑할 수 있습니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
<!-- ## Blade Directives -->
## Blade Directives

<!-- In addition to template inheritance and displaying data, Blade also provides convenient shortcuts for common PHP control structures, such as conditional statements and loops. These shortcuts provide a very clean, terse way of working with PHP control structures while also remaining familiar to their PHP counterparts. -->
템플릿 상속 및 데이터 표시 외에도 Blade는 조건문 및 루프와 같은 일반적인 PHP 제어 구조에 대한 편리한 바로 가기를 제공합니다. 이러한 단축키는 PHP 제어 구조에 대한 친숙함을 유지하면서 PHP 제어 구조로 작업하는 매우 깔끔하고 간결한 방법을 제공합니다.

<a name="if-statements"></a>
<!-- ### If Statements -->
### If Statements

<!-- You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts: -->
`@if`, `@elseif`, `@else` 및 `@endif` 지시어를 사용하여 `if` 문을 생성할 수 있습니다. 이러한 지시어는 해당 PHP 지시어와 동일하게 작동합니다.

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

<!-- For convenience, Blade also provides an `@unless` directive: -->
편의를 위해 Blade는 `@unless` 지시문도 제공합니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

<!-- In addition to the conditional directives already discussed, the `@isset` and `@empty` directives may be used as convenient shortcuts for their respective PHP functions: -->
이미 설명한 조건부 지시문 외에도 `@isset` 및 `@empty` 지시문을 해당 PHP 기능에 대한 편리한 바로 가기로 사용할 수 있습니다.

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```

<a name="authentication-directives"></a>
<!-- #### Authentication Directives -->
#### Authentication Directives

<!-- The `@auth` and `@guest` directives may be used to quickly determine if the current user is [authenticated](/docs/13.x/authentication) or is a guest: -->
`@auth` 및 `@guest` 지시어를 사용하면 현재 사용자가 [authenticated](/docs/13.x/authentication)되었는지 아니면 게스트인지 빠르게 확인할 수 있습니다.

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

<!-- If needed, you may specify the authentication guard that should be checked when using the `@auth` and `@guest` directives: -->
필요한 경우 `@auth` 및 `@guest` 지시문을 사용할 때 확인해야 하는 인증 가드를 지정할 수 있습니다.

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```

<a name="environment-directives"></a>
<!-- #### Environment Directives -->
#### Environment Directives

<!-- You may check if the application is running in the production environment using the `@production` directive: -->
`@production` 지시문을 사용하여 애플리케이션이 프로덕션 환경에서 실행되고 있는지 확인할 수 있습니다.

```blade
@production
    // Production specific content...
@endproduction
```

<!-- Or, you may determine if the application is running in a specific environment using the `@env` directive: -->
또는 `@env` 지시어를 사용하여 애플리케이션이 특정 환경에서 실행되고 있는지 확인할 수 있습니다.

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```

<a name="section-directives"></a>
<!-- #### Section Directives -->
#### Section Directives

<!-- You may determine if a template inheritance section has content using the `@hasSection` directive: -->
`@hasSection` 지시문을 사용하여 템플릿 상속 섹션에 콘텐츠가 있는지 확인할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

<!-- You may use the `sectionMissing` directive to determine if a section does not have content: -->
섹션에 내용이 없는지 확인하려면 `sectionMissing` 지시문을 사용할 수 있습니다.

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
<!-- #### Session Directives -->
#### Session Directives

<!-- The `@session` directive may be used to determine if a [session](/docs/13.x/session) value exists. If the session value exists, the template contents within the `@session` and `@endsession` directives will be evaluated. Within the `@session` directive's contents, you may echo the `$value` variable to display the session value: -->
`@session` 지시어는 [session](/docs/13.x/session) 값이 존재하는지 확인하는 데 사용될 수 있습니다. 세션 값이 존재하는 경우 `@session` 및 `@endsession` 지시문 내의 템플릿 내용이 평가됩니다. `@session` 지시문의 내용 내에서 `$value` 변수를 에코하여 세션 값을 표시할 수 있습니다.

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
<!-- #### Context Directives -->
#### Context Directives

<!-- The `@context` directive may be used to determine if a [context](/docs/13.x/context) value exists. If the context value exists, the template contents within the `@context` and `@endcontext` directives will be evaluated. Within the `@context` directive's contents, you may echo the `$value` variable to display the context value: -->
`@context` 지시어는 [context](/docs/13.x/context) 값이 존재하는지 확인하는 데 사용될 수 있습니다. 컨텍스트 값이 존재하는 경우 `@context` 및 `@endcontext` 지시문 내의 템플릿 내용이 평가됩니다. `@context` 지시문의 내용 내에서 `$value` 변수를 에코하여 컨텍스트 값을 표시할 수 있습니다.

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
<!-- ### Switch Statements -->
### Switch Statements

<!-- Switch statements can be constructed using the `@switch`, `@case`, `@break`, `@default` and `@endswitch` directives: -->
Switch 문은 `@switch`, `@case`, `@break`, `@default` 및 `@endswitch` 지시문을 사용하여 구성할 수 있습니다.

```blade
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```

<a name="loops"></a>
<!-- ### Loops -->
### Loops

<!-- In addition to conditional statements, Blade provides simple directives for working with PHP's loop structures. Again, each of these directives functions identically to their PHP counterparts: -->
조건문 외에도 Blade는 PHP의 루프 구조 작업을 위한 간단한 지시문을 제공합니다. 다시 말하지만, 이러한 각 지시문은 PHP 대응 항목과 동일하게 작동합니다.

```blade
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

> [!NOTE]
> `foreach` 루프를 반복하는 동안 [loop variable](#the-loop-variable)를 사용하여 루프를 통해 첫 번째 또는 마지막 반복에 있는지와 같은 루프에 대한 귀중한 정보를 얻을 수 있습니다.

<!-- When using loops you may also skip the current iteration or end the loop using the `@continue` and `@break` directives: -->
루프를 사용할 때 현재 반복을 건너뛰거나 `@continue` 및 `@break` 지시문을 사용하여 루프를 종료할 수도 있습니다.

```blade
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```

<!-- You may also include the continuation or break condition within the directive declaration: -->
지시문 선언 내에 연속 또는 중단 조건을 포함할 수도 있습니다.

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
<!-- ### The Loop Variable -->
### The Loop Variable

<!-- While iterating through a `foreach` loop, a `$loop` variable will be available inside of your loop. This variable provides access to some useful bits of information such as the current loop index and whether this is the first or last iteration through the loop: -->
`foreach` 루프를 반복하는 동안 루프 내에서 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 루프 인덱스 및 이것이 루프를 통한 첫 번째 또는 마지막 반복인지 여부와 같은 몇 가지 유용한 정보에 대한 액세스를 제공합니다.

```blade
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```

<!-- If you are in a nested loop, you may access the parent loop's `$loop` variable via the `parent` property: -->
중첩 루프에 있는 경우 `parent` 속성을 통해 상위 루프의 `$loop` 변수에 액세스할 수 있습니다.

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

<!-- The `$loop` variable also contains a variety of other useful properties: -->
`$loop` 변수에는 다음과 같은 다양한 유용한 속성도 포함되어 있습니다.

<div class="overflow-auto">

<!-- | Property | Description | | ------------------ | ------------------------------------------------------ | | `$loop->index` | The index of the current loop iteration (starts at 0). | | `$loop->iteration` | The current loop iteration (starts at 1). | | `$loop->remaining` | The iterations remaining in the loop. | | `$loop->count` | The total number of items in the array being iterated. | | `$loop->first` | Whether this is the first iteration through the loop. | | `$loop->last` | Whether this is the last iteration through the loop. | | `$loop->even` | Whether this is an even iteration through the loop. | | `$loop->odd` | Whether this is an odd iteration through the loop. | | `$loop->depth` | The nesting level of the current loop. | | `$loop->parent` | When in a nested loop, the parent's loop variable. | -->
| 속성 | 설명 |
| ------------------ | ------------------------------------------------------ |
| `$loop->index` | 현재 루프 반복의 인덱스입니다(0에서 시작). |
| `$loop->iteration` | 현재 루프 반복(1에서 시작)              |
| `$loop->remaining` | 루프에 남아 있는 반복입니다.                  |
| `$loop->count` | 반복되는 배열의 총 항목 수입니다. |
| `$loop->first` | 이것이 루프를 통한 첫 번째 반복인지 여부입니다.  |
| `$loop->last` | 이것이 루프를 통한 마지막 반복인지 여부입니다.   |
| `$loop->even` | 루프를 통한 짝수 반복인지 여부입니다.    |
| `$loop->odd` | 루프를 통한 홀수 반복인지 여부입니다.     |
| `$loop->depth` | 현재 루프의 중첩 수준입니다.                 |
| `$loop->parent` | 중첩 루프에 있는 경우 상위 루프 변수입니다.     |

</div>

<a name="conditional-classes"></a>
<!-- ### Conditional Classes & Styles -->
### Conditional Classes & Styles

<!-- The `@class` directive conditionally compiles a CSS class string. The directive accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`@class` 지시문은 CSS 클래스 문자열을 조건부로 컴파일합니다. 지시어는 배열 키에 추가하려는 클래스가 포함되어 있고 값은 부울 표현식인 클래스 배열을 허용합니다. 배열 요소에 숫자 키가 있으면 렌더링된 클래스 목록에 항상 포함됩니다.

```blade
@php
    $isActive = false;
    $hasError = true;
@endphp

<span @class([
    'p-4',
    'font-bold' => $isActive,
    'text-gray-500' => ! $isActive,
    'bg-red' => $hasError,
])></span>

<span class="p-4 text-gray-500 bg-red"></span>
```

<!-- Likewise, the `@style` directive may be used to conditionally add inline CSS styles to an HTML element: -->
마찬가지로 `@style` 지시문을 사용하여 HTML 요소에 인라인 CSS 스타일을 조건부로 추가할 수 있습니다.

```blade
@php
    $isActive = true;
@endphp

<span @style([
    'background-color: red',
    'font-weight: bold' => $isActive,
])></span>

<span style="background-color: red; font-weight: bold;"></span>
```

<a name="additional-attributes"></a>
<!-- ### Additional Attributes -->
### Additional Attributes

<!-- For convenience, you may use the `@checked` directive to easily indicate if a given HTML checkbox input is "checked". This directive will echo `checked` if the provided condition evaluates to `true`: -->
편의를 위해 `@checked` 지시문을 사용하여 주어진 HTML 확인란 입력이 "선택"되었는지 쉽게 나타낼 수 있습니다. 제공된 조건이 `true`로 평가되면 이 지시어는 `checked`를 표시합니다.

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

<!-- Likewise, the `@selected` directive may be used to indicate if a given select option should be "selected": -->
마찬가지로 `@selected` 지시문을 사용하여 주어진 선택 옵션을 "선택"해야 하는지 여부를 나타낼 수 있습니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

<!-- Additionally, the `@disabled` directive may be used to indicate if a given element should be "disabled": -->
또한 `@disabled` 지시문을 사용하여 특정 요소를 "비활성화"해야 하는지 여부를 나타낼 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

<!-- Moreover, the `@readonly` directive may be used to indicate if a given element should be "readonly": -->
또한 `@readonly` 지시문을 사용하여 특정 요소가 "읽기 전용"인지 여부를 나타낼 수 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

<!-- In addition, the `@required` directive may be used to indicate if a given element should be "required": -->
또한 `@required` 지시문을 사용하여 특정 요소가 "필수"인지 여부를 나타낼 수 있습니다.

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
<!-- ### Including Subviews -->
### Including Subviews

> [!NOTE]
> `@include` 지시문을 자유롭게 사용할 수 있지만 Blade [components](#components)는 유사한 기능을 제공하고 데이터 및 속성 바인딩과 같은 `@include` 지시문에 비해 여러 가지 이점을 제공합니다.

<!-- Blade's `@include` directive allows you to include a Blade view from within another view. All variables that are available to the parent view will be made available to the included view: -->
Blade의 `@include` 지시어를 사용하면 다른 뷰 내에 Blade 뷰를 포함할 수 있습니다. 상위 뷰에서 사용할 수 있는 모든 변수는 포함된 뷰에서도 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

<!-- Even though the included view will inherit all data available in the parent view, you may also pass an array of additional data that should be made available to the included view: -->
포함된 뷰가 상위 뷰에서 사용 가능한 모든 데이터를 상속하더라도 포함된 뷰에서 사용 가능해야 하는 추가 데이터 배열을 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

<!-- If you attempt to `@include` a view which does not exist, Laravel will throw an error. If you would like to include a view that may or may not be present, you should use the `@includeIf` directive: -->
존재하지 않는 뷰를 `@include`하려고 시도하면 Laravel에서 오류가 발생합니다. 존재하거나 존재하지 않을 수 있는 뷰를 포함하려면 `@includeIf` 지시문을 사용해야 합니다.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

<!-- If you would like to `@include` a view if a given boolean expression evaluates to `true` or `false`, you may use the `@includeWhen` and `@includeUnless` directives: -->
주어진 부울 표현식이 `true` 또는 `false`로 평가되는 경우 `@include` 및 뷰를 수행하려면 `@includeWhen` 및 `@includeUnless` 지시문을 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

<!-- To include the first view that exists from a given array of views, you may use the `includeFirst` directive: -->
주어진 뷰 배열에 존재하는 첫 번째 뷰를 포함하려면 `includeFirst` 지시문을 사용할 수 있습니다.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

<!-- If you would like to include a view without inheriting any variables from the parent view, you may use the `@includeIsolated` directive. The included view will only have access to variables you explicitly pass: -->
상위 뷰에서 변수를 상속하지 않고 뷰를 포함하려면 `@includeIsolated` 지시문을 사용할 수 있습니다. 포함된 뷰는 명시적으로 전달한 변수에만 액세스할 수 있습니다.

```blade
@includeIsolated('view.name', ['user' => $user])
```

> [!WARNING]
> Blade 뷰에서 `__DIR__` 및 `__FILE__` 상수는 캐시되고 컴파일된 뷰의 위치를 ​​참조하므로 사용을 피해야 합니다.

<a name="rendering-views-for-collections"></a>
<!-- #### Rendering Views for Collections -->
#### Rendering Views for Collections

<!-- You may combine loops and includes into one line with Blade's `@each` directive: -->
Blade의 `@each` 지시문을 사용하여 루프와 포함을 한 줄로 결합할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

<!-- The `@each` directive's first argument is the view to render for each element in the array or collection. The second argument is the array or collection you wish to iterate over, while the third argument is the variable name that will be assigned to the current iteration within the view. So, for example, if you are iterating over an array of `jobs`, typically you will want to access each job as a `job` variable within the view. The array key for the current iteration will be available as the `key` variable within the view. -->
`@each` 지시문의 첫 번째 인수는 배열 또는 컬렉션의 각 요소에 대해 렌더링하는 뷰입니다. 두 번째 인수는 반복하려는 배열 또는 컬렉션이고, 세 번째 인수는 뷰 내에서 현재 반복에 할당될 변수 이름입니다. 따라서 예를 들어 `jobs` 배열을 반복하는 경우 일반적으로 각 작업을 뷰 내의 `job` 변수로 액세스하려고 합니다. 현재 반복의 배열 키는 뷰 내에서 `key` 변수로 사용할 수 있습니다.

<!-- You may also pass a fourth argument to the `@each` directive. This argument determines the view that will be rendered if the given array is empty. -->
`@each` 지시문에 네 번째 인수를 전달할 수도 있습니다. 이 인수는 주어진 배열이 비어 있는 경우 렌더링될 뷰를 결정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`를 통해 렌더링된 뷰는 상위 뷰로부터 변수를 상속받지 않습니다. 하위 뷰에 이러한 변수가 필요한 경우 대신 `@foreach` 및 `@include` 지시어를 사용해야 합니다.

<a name="the-once-directive"></a>
<!-- ### The `@once` Directive -->
### The `@once` Directive

<!-- The `@once` directive allows you to define a portion of the template that will only be evaluated once per rendering cycle. This may be useful for pushing a given piece of JavaScript into the page's header using [stacks](#stacks). For example, if you are rendering a given [component](#components) within a loop, you may wish to only push the JavaScript to the header the first time the component is rendered: -->
`@once` 지시문을 사용하면 렌더링 주기당 한 번만 평가되는 템플릿 부분을 정의할 수 있습니다. 이는 [stacks](#stacks)을 사용하여 JavaScript의 특정 부분을 페이지 헤더에 푸시하는 데 유용할 수 있습니다. 예를 들어, 루프 내에서 특정 [component](#components)를 렌더링하는 경우 컴포넌트가 처음 렌더링될 때 JavaScript만 헤더에 푸시할 수 있습니다.

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

<!-- Since the `@once` directive is often used in conjunction with the `@push` or `@prepend` directives, the `@pushOnce` and `@prependOnce` directives are available for your convenience: -->
`@once` 지시어는 `@push` 또는 `@prepend` 지시어와 함께 사용되는 경우가 많으므로 편의를 위해 `@pushOnce` 및 `@prependOnce` 지시어를 사용할 수 있습니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<!-- If you are pushing duplicate content from two separate Blade templates, you should provide a unique identifier as the second argument to the `@pushOnce` directive to ensure the content is only rendered once: -->
두 개의 개별 Blade 템플릿에서 중복 콘텐츠를 푸시하는 경우 콘텐츠가 한 번만 렌더링되도록 `@pushOnce` 지시어에 대한 두 번째 인수로 고유 식별자를 제공해야 합니다.

```blade
<!-- pie-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce

<!-- line-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce
```

<a name="raw-php"></a>
<!-- ### Raw PHP -->
### Raw PHP

<!-- In some situations, it's useful to embed PHP code into your views. You can use the Blade `@php` directive to execute a block of plain PHP within your template: -->
어떤 상황에서는 PHP 코드를 뷰에 삽입하는 것이 유용합니다. Blade `@php` 지시문을 사용하여 템플릿 내에서 일반 PHP 블록을 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

<!-- Or, if you only need to use PHP to import a class, you may use the `@use` directive: -->
또는 클래스를 가져오기 위해 PHP만 사용해야 하는 경우 `@use` 지시문을 사용할 수 있습니다.

```blade
@use('App\Models\Flight')
```

<!-- A second argument may be provided to the `@use` directive to alias the imported class: -->
가져온 클래스의 별칭을 지정하기 위해 `@use` 지시문에 두 번째 인수를 제공할 수 있습니다.

```blade
@use('App\Models\Flight', 'FlightModel')
```

<!-- If you have multiple classes within the same namespace, you may group the imports of those classes: -->
동일한 네임스페이스 내에 여러 클래스가 있는 경우 해당 클래스의 가져오기를 그룹화할 수 있습니다.

```blade
@use('App\Models\{Flight, Airport}')
```

<!-- The `@use` directive also supports importing PHP functions and constants by prefixing the import path with the `function` or `const` modifiers: -->
`@use` 지시문은 가져오기 경로 앞에 `function` 또는 `const` 수정자를 추가하여 PHP 함수 및 상수 가져오기를 지원합니다.

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

<!-- Just like class imports, aliases are supported for functions and constants as well: -->
클래스 가져오기와 마찬가지로 함수와 상수에도 별칭이 지원됩니다.

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

<!-- Grouped imports are also supported with both function and const modifiers, allowing you to import multiple symbols from the same namespace in a single directive: -->
그룹화된 가져오기는 function 및 const 한정자 모두에서 지원되므로 단일 지시어로 동일한 네임스페이스에서 여러 기호를 가져올 수 있습니다.

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="fonts"></a>
<!-- ### Fonts -->
### Fonts

<!-- When using [Laravel's Vite font optimization](/docs/13.x/vite#working-with-fonts), you may use the `@fonts` directive to render your configured font preload links and inline font CSS in your application's layout: -->
[Laravel's Vite font optimization](/docs/13.x/vite#working-with-fonts)를 사용할 때, `@fonts` 디렉티브를 사용하여 애플리케이션 레이아웃에 설정된 폰트 프리로드 링크와 인라인 폰트 CSS를 렌더링할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @fonts
    @vite('resources/js/app.js')
</head>
```

<!-- The `@fonts` directive renders all font families configured in your `vite.config.js` file. The directive should typically be placed in the `<head>` of your application's root layout before any content that uses those fonts. -->
`@fonts` 디렉티브는 `vite.config.js` 파일에 설정된 모든 폰트 패밀리를 렌더링합니다. 이 디렉티브는 일반적으로 해당 폰트를 사용하는 콘텐츠보다 앞서, 애플리케이션 루트 레이아웃의 `<head>` 안에 배치해야 합니다.

<!-- If a page only needs some of your configured fonts, you may pass one or more font aliases to the directive: -->
페이지에서 설정된 폰트 중 일부만 필요한 경우, 디렉티브에 하나 이상의 폰트 별칭(alias)을 전달할 수 있습니다.

```blade
{{-- Load a single font alias... --}}
@fonts('sans')

{{-- Load multiple font aliases... --}}
@fonts(['sans', 'mono'])
```

<!-- Font aliases are configured using the `alias` option when defining fonts in your Vite configuration. The `@fonts` directive calls the `fonts` method provided by the `Vite` facade, which may also be invoked directly: -->
폰트 별칭은 Vite 설정에서 폰트를 정의할 때 `alias` 옵션을 사용하여 설정합니다. `@fonts` 디렉티브는 `Vite` 파사드가 제공하는 `fonts` 메서드를 호출하며, 이 메서드를 직접 호출할 수도 있습니다.

```blade
{{ Vite::fonts(['sans', 'mono']) }}
```

<a name="comments"></a>
<!-- ### Comments -->
### Comments

<!-- Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application: -->
Blade를 사용하면 뷰에 주석을 정의할 수도 있습니다. 그러나 HTML 주석과 달리 Blade 주석은 애플리케이션에서 반환된 HTML에 포함되지 않습니다.

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
<!-- ## Components -->
## Components

<!-- Components and slots provide similar benefits to sections, layouts, and includes; however, some may find the mental model of components and slots easier to understand. There are two approaches to writing components: class-based components and anonymous components. -->
컴포넌트와 슬롯은 섹션, 레이아웃 및 포함과 유사한 이점을 제공합니다. 그러나 일부는 컴포넌트와 슬롯의 정신적 모델을 이해하기가 더 쉽다고 생각할 수도 있습니다. 컴포넌트를 작성하는 방법에는 클래스 기반 컴포넌트와 익명 컴포넌트라는 두 가지 접근 방식이 있습니다.

<!-- To create a class-based component, you may use the `make:component` Artisan command. To illustrate how to use components, we will create a simple `Alert` component. The `make:component` command will place the component in the `app/View/Components` directory: -->
클래스 기반 컴포넌트를 생성하려면 `make:component` Artisan 명령을 사용할 수 있습니다. 컴포넌트 사용 방법을 설명하기 위해 간단한 `Alert` 컴포넌트를 만들어 보겠습니다. `make:component` 명령은 컴포넌트를 `app/View/Components` 디렉터리에 배치합니다.

```shell
php artisan make:component Alert
```

<!-- The `make:component` command will also create a view template for the component. The view will be placed in the `resources/views/components` directory. When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory, so no further component registration is typically required. -->
`make:component` 명령은 컴포넌트에 대한 뷰 템플릿도 생성합니다. 뷰는 `resources/views/components` 디렉토리에 배치됩니다. 자신의 애플리케이션에 대한 컴포넌트를 작성할 때 컴포넌트는 `app/View/Components` 디렉터리 및 `resources/views/components` 디렉터리 내에서 자동으로 검색되므로 일반적으로 추가 컴포넌트 등록이 필요하지 않습니다.

<!-- You may also create components within subdirectories: -->
하위 디렉터리 내에 컴포넌트를 생성할 수도 있습니다.

```shell
php artisan make:component Forms/Input
```

<!-- The command above will create an `Input` component in the `app/View/Components/Forms` directory and the view will be placed in the `resources/views/components/forms` directory. -->
위 명령은 `app/View/Components/Forms` 디렉터리에 `Input` 컴포넌트를 생성하고 뷰는 `resources/views/components/forms` 디렉터리에 배치됩니다.

<a name="manually-registering-package-components"></a>
<!-- #### Manually Registering Package Components -->
#### Manually Registering Package Components

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
자신의 애플리케이션에 대한 컴포넌트를 작성할 때 컴포넌트는 `app/View/Components` 디렉터리 및 `resources/views/components` 디렉터리 내에서 자동으로 검색됩니다.

<!-- However, if you are building a package that utilizes Blade components, you will need to manually register your component class and its HTML tag alias. You should typically register your components in the `boot` method of your package's service provider: -->
그러나 Blade 컴포넌트를 활용하는 패키지를 구축하는 경우 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지 서비스 프로바이더의 `boot` 메서드에 컴포넌트를 등록해야 합니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
컴포넌트가 등록되면 태그 별칭을 사용하여 렌더링될 수 있습니다.

```blade
<x-package-alert/>
```

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
또는 `componentNamespace` 메서드를 사용하여 규칙에 따라 컴포넌트 클래스를 자동 로드할 수도 있습니다. 예를 들어, `Nightshade` 패키지에는 `Package\Views\Components` 네임스페이스 내에 상주하는 `Calendar` 및 `ColorPicker` 컴포넌트가 있을 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
이렇게 하면 `package-name::` 구문을 사용하여 공급업체 네임스페이스에서 패키지 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 대소문자로 구분하여 이 컴포넌트에 연결된 클래스를 자동으로 감지합니다. 하위 디렉터리도 "점" 표기법을 사용하여 지원됩니다.

<a name="rendering-components"></a>
<!-- ### Rendering Components -->
### Rendering Components

<!-- To display a component, you may use a Blade component tag within one of your Blade templates. Blade component tags start with the string `x-` followed by the kebab case name of the component class: -->
컴포넌트를 표시하려면 Blade 템플릿 중 하나에서 Blade 컴포넌트 태그를 사용할 수 있습니다. Blade 컴포넌트 태그는 `x-` 문자열로 시작하고 그 뒤에 컴포넌트 클래스의 케밥 케이스 이름이 옵니다.

```blade
<x-alert/>

<x-user-profile/>
```

<!-- If the component class is nested deeper within the `app/View/Components` directory, you may use the `.` character to indicate directory nesting. For example, if we assume a component is located at `app/View/Components/Inputs/Button.php`, we may render it like so: -->
컴포넌트 클래스가 `app/View/Components` 디렉터리 내에서 더 깊게 중첩된 경우 `.` 문자를 사용하여 디렉터리 중첩을 나타낼 수 있습니다. 예를 들어 컴포넌트가 `app/View/Components/Inputs/Button.php`에 있다고 가정하면 다음과 같이 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

<!-- If you would like to conditionally render your component, you may define a `shouldRender` method on your component class. If the `shouldRender` method returns `false` the component will not be rendered: -->
컴포넌트를 조건부로 렌더링하려면 컴포넌트 클래스에 `shouldRender` 메소드를 정의하면 됩니다. `shouldRender` 메소드가 `false`를 반환하면 컴포넌트가 렌더링되지 않습니다.

```php
use Illuminate\Support\Str;

/**
 * Whether the component should be rendered
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
<!-- ### Index Components -->
### Index Components

<!-- Sometimes components are part of a component group and you may wish to group the related components within a single directory. For example, imagine a "card" component with the following class structure: -->
때로는 컴포넌트가 컴포넌트 그룹의 일부이고 단일 디렉터리 내에서 관련 컴포넌트를 그룹화할 수도 있습니다. 예를 들어, 다음과 같은 클래스 구조를 가진 "카드" 컴포넌트를 상상해 보세요.

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

<!-- Since the root `Card` component is nested within a `Card` directory, you might expect that you would need to render the component via `<x-card.card>`. However, when a component's file name matches the name of the component's directory, Laravel automatically assumes that component is the "root" component and allows you to render the component without repeating the directory name: -->
루트 `Card` 컴포넌트가 `Card` 디렉터리 내에 중첩되어 있으므로 `<x-card.card>`를 통해 컴포넌트를 렌더링해야 한다고 생각할 수 있습니다. 그러나 컴포넌트의 파일 이름이 컴포넌트의 디렉터리 이름과 일치하는 경우 Laravel는 자동으로 컴포넌트가 "루트" 컴포넌트라고 가정하고 디렉터리 이름을 반복하지 않고 컴포넌트를 렌더링할 수 있도록 합니다.

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
<!-- ### Passing Data to Components -->
### Passing Data to Components

<!-- You may pass data to Blade components using HTML attributes. Hard-coded, primitive values may be passed to the component using simple HTML attribute strings. PHP expressions and variables should be passed to the component via attributes that use the `:` character as a prefix: -->
HTML 속성을 사용하여 Blade 컴포넌트에 데이터를 전달할 수 있습니다. 하드 코딩된 기본 값은 간단한 HTML 속성 문자열을 사용하여 컴포넌트에 전달될 수 있습니다. PHP 표현식과 변수는 `:` 문자를 접두사로 사용하는 속성을 통해 컴포넌트에 전달되어야 합니다.

```blade
<x-alert type="error" :message="$message"/>
```

<!-- You should define all of the component's data attributes in its class constructor. All public properties on a component will automatically be made available to the component's view. It is not necessary to pass the data to the view from the component's `render` method: -->
클래스 생성자에서 컴포넌트의 모든 데이터 속성을 정의해야 합니다. 컴포넌트의 모든 공용 속성은 컴포넌트의 뷰에서 자동으로 사용할 수 있게 됩니다. 컴포넌트의 `render` 메서드에서 뷰로 데이터를 전달할 필요는 없습니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

<!-- When your component is rendered, you may display the contents of your component's public variables by echoing the variables by name: -->
컴포넌트가 렌더링되면 변수를 이름으로 에코하여 컴포넌트의 공용 변수 내용을 표시할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
<!-- #### Casing -->
#### Casing

<!-- Component constructor arguments should be specified using `camelCase`, while `kebab-case` should be used when referencing the argument names in your HTML attributes. For example, given the following component constructor: -->
컴포넌트 생성자 인수는 `camelCase`를 사용하여 지정해야 하며, `kebab-case`는 HTML 속성에서 인수 이름을 참조할 때 사용해야 합니다. 예를 들어 다음과 같은 컴포넌트 생성자가 있다고 가정합니다.

```php
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```

<!-- The `$alertType` argument may be provided to the component like so: -->
`$alertType` 인수는 다음과 같이 컴포넌트에 제공될 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
<!-- #### Short Attribute Syntax -->
#### Short Attribute Syntax

<!-- When passing attributes to components, you may also use a "short attribute" syntax. This is often convenient since attribute names frequently match the variable names they correspond to: -->
속성을 컴포넌트에 전달할 때 "짧은 속성" 구문을 사용할 수도 있습니다. 속성 이름은 해당 변수 이름과 자주 일치하므로 이는 편리한 경우가 많습니다.

```blade
{{-- Short attribute syntax... --}}
<x-profile :$userId :$name />

{{-- Is equivalent to... --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
<!-- #### Escaping Attribute Rendering -->
#### Escaping Attribute Rendering

<!-- Since some JavaScript frameworks such as Alpine.js also use colon-prefixed attributes, you may use a double colon (`::`) prefix to inform Blade that the attribute is not a PHP expression. For example, given the following component: -->
Alpine.js와 같은 일부 JavaScript 프레임워크도 콜론 접두사 속성을 사용하므로 이중 콜론(`::`) 접두사를 사용하여 해당 속성이 PHP 표현식이 아님을 Blade에 알릴 수 있습니다. 예를 들어 다음 컴포넌트가 있다고 가정해 보겠습니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

<!-- The following HTML will be rendered by Blade: -->
다음 HTML은 Blade에 의해 렌더링됩니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
<!-- #### Component Methods -->
#### Component Methods

<!-- In addition to public variables being available to your component template, any public methods on the component may be invoked. For example, imagine a component that has an `isSelected` method: -->
컴포넌트 템플릿에 사용할 수 있는 공용 변수 외에도 컴포넌트의 모든 공용 메서드를 호출할 수 있습니다. 예를 들어 `isSelected` 메서드가 있는 컴포넌트를 상상해 보세요.

```php
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

<!-- You may execute this method from your component template by invoking the variable matching the name of the method: -->
메소드 이름과 일치하는 변수를 호출하여 컴포넌트 템플릿에서 이 메소드를 실행할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
<!-- #### Accessing Attributes and Slots Within Component Classes -->
#### Accessing Attributes and Slots Within Component Classes

<!-- Blade components also allow you to access the component name, attributes, and slot inside the class's render method. However, in order to access this data, you should return a closure from your component's `render` method: -->
Blade 컴포넌트를 사용하면 클래스의 렌더링 메서드 내 컴포넌트 이름, 속성 및 슬롯에 액세스할 수도 있습니다. 그러나 이 데이터에 액세스하려면 컴포넌트의 `render` 메서드에서 클로저를 반환해야 합니다.

```php
use Closure;

/**
 * Get the view / contents that represent the component.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

<!-- The closure returned by your component's `render` method may also receive a `$data` array as its only argument. This array will contain several elements that provide information about the component: -->
컴포넌트의 `render` 메서드에서 반환된 클로저는 `$data` 배열을 유일한 인수로 받을 수도 있습니다. 이 배열에는 컴포넌트에 대한 정보를 제공하는 여러 요소가 포함됩니다.

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 요소는 `render` 메서드에서 반환된 Blade 문자열에 직접 포함되어서는 안 됩니다. 그렇게 하면 악성 특성 콘텐츠를 통해 원격 코드가 실행될 수 있습니다.

<!-- The `componentName` is equal to the name used in the HTML tag after the `x-` prefix. So `<x-alert />`'s `componentName` will be `alert`. The `attributes` element will contain all of the attributes that were present on the HTML tag. The `slot` element is an `Illuminate\Support\HtmlString` instance with the contents of the component's slot. -->
`componentName`는 HTML 태그에서 `x-` 접두사 뒤에 사용되는 이름과 같습니다. 따라서 `<x-alert />`의 `componentName`는 `alert`가 됩니다. `attributes` 요소에는 HTML 태그에 있던 모든 속성이 포함됩니다. `slot` 요소는 컴포넌트 슬롯의 콘텐츠가 포함된 `Illuminate\Support\HtmlString` 인스턴스입니다.

<!-- The closure should return a string. If the returned string corresponds to an existing view, that view will be rendered; otherwise, the returned string will be evaluated as an inline Blade view. -->
클로저는 문자열을 반환해야 합니다. 반환된 문자열이 기존 뷰에 해당하는 경우 해당 뷰가 렌더링됩니다. 그렇지 않으면 반환된 문자열은 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
<!-- #### Additional Dependencies -->
#### Additional Dependencies

<!-- If your component requires dependencies from Laravel's [service container](/docs/13.x/container), you may list them before any of the component's data attributes and they will automatically be injected by the container: -->
컴포넌트에 Laravel의 [service container](/docs/13.x/container)의 종속성이 필요한 경우 컴포넌트의 데이터 속성 앞에 이를 나열할 수 있으며 컨테이너에 의해 자동으로 주입됩니다.

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
<!-- #### Hiding Attributes / Methods -->
#### Hiding Attributes / Methods

<!-- If you would like to prevent some public methods or properties from being exposed as variables to your component template, you may add them to an `$except` array property on your component: -->
일부 공용 메서드나 속성이 컴포넌트 템플릿에 변수로 노출되는 것을 방지하려면 해당 항목을 컴포넌트의 `$except` 배열 속성에 추가할 수 있습니다.

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The properties / methods that should not be exposed to the component template.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
<!-- ### Component Attributes -->
### Component Attributes

<!-- We've already examined how to pass data attributes to a component; however, sometimes you may need to specify additional HTML attributes, such as `class`, that are not part of the data required for a component to function. Typically, you want to pass these additional attributes down to the root element of the component template. For example, imagine we want to render an `alert` component like so: -->
우리는 이미 데이터 속성을 컴포넌트에 전달하는 방법을 살펴보았습니다. 그러나 때로는 컴포넌트가 작동하는 데 필요한 데이터의 일부가 아닌 `class`와 같은 추가 HTML 속성을 지정해야 할 수도 있습니다. 일반적으로 이러한 추가 특성을 컴포넌트 템플릿의 루트 요소에 전달하려고 합니다. 예를 들어 다음과 같이 `alert` 컴포넌트를 렌더링한다고 가정해 보겠습니다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

<!-- All of the attributes that are not part of the component's constructor will automatically be added to the component's "attribute bag". This attribute bag is automatically made available to the component via the `$attributes` variable. All of the attributes may be rendered within the component by echoing this variable: -->
컴포넌트 생성자의 일부가 아닌 모든 속성은 컴포넌트의 "속성 모음"에 자동으로 추가됩니다. 이 속성 백은 `$attributes` 변수를 통해 컴포넌트에 자동으로 사용 가능해집니다. 모든 속성은 다음 변수를 에코하여 컴포넌트 내에서 렌더링될 수 있습니다.

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 컴포넌트 태그 내에서 `@env`와 같은 지시문을 사용하는 것은 현재 지원되지 않습니다. 예를 들어, `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
<!-- #### Default / Merged Attributes -->
#### Default / Merged Attributes

<!-- Sometimes you may need to specify default values for attributes or merge additional values into some of the component's attributes. To accomplish this, you may use the attribute bag's `merge` method. This method is particularly useful for defining a set of default CSS classes that should always be applied to a component: -->
때로는 속성에 대한 기본값을 지정하거나 추가 값을 일부 컴포넌트 속성에 병합해야 할 수도 있습니다. 이를 달성하려면 속성 백의 `merge` 메소드를 사용할 수 있습니다. 이 메서드는 컴포넌트에 항상 적용되어야 하는 기본 CSS 클래스 집합을 정의하는 데 특히 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- If we assume this component is utilized like so: -->
이 컴포넌트가 다음과 같이 활용된다고 가정하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<!-- The final, rendered HTML of the component will appear like the following: -->
컴포넌트의 최종 렌더링된 HTML은 다음과 같이 표시됩니다.

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
<!-- #### Conditionally Merge Classes -->
#### Conditionally Merge Classes

<!-- Sometimes you may wish to merge classes if a given condition is `true`. You can accomplish this via the `class` method, which accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
때로는 주어진 조건이 `true`인 경우 클래스를 병합하고 싶을 수도 있습니다. 이 작업은 배열 키에 추가하려는 클래스가 포함되어 있고 값은 부울 표현식인 클래스 배열을 허용하는 `class` 메서드를 통해 수행할 수 있습니다. 배열 요소에 숫자 키가 있으면 렌더링된 클래스 목록에 항상 포함됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

<!-- If you need to merge other attributes onto your component, you can chain the `merge` method onto the `class` method: -->
다른 속성을 컴포넌트에 병합해야 하는 경우 `merge` 메서드를 `class` 메서드에 연결할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성을 수신하면 안 되는 다른 HTML 요소에 대한 클래스를 조건부로 컴파일해야 하는 경우 [@class directive](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
<!-- #### Non-Class Attribute Merging -->
#### Non-Class Attribute Merging

<!-- When merging attributes that are not `class` attributes, the values provided to the `merge` method will be considered the "default" values of the attribute. However, unlike the `class` attribute, these attributes will not be merged with injected attribute values. Instead, they will be overwritten. For example, a `button` component's implementation may look like the following: -->
`class` 속성이 아닌 속성을 병합하는 경우 `merge` 메소드에 제공된 값은 속성의 "기본" 값으로 간주됩니다. 그러나 `class` 속성과 달리 이러한 속성은 삽입된 속성 값과 병합되지 않습니다. 대신 덮어쓰게 됩니다. 예를 들어 `button` 컴포넌트의 구현은 다음과 같을 수 있습니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

<!-- To render the button component with a custom `type`, it may be specified when consuming the component. If no type is specified, the `button` type will be used: -->
사용자 지정 `type`를 사용하여 버튼 컴포넌트를 렌더링하려면 컴포넌트를 사용할 때 지정할 수 있습니다. 유형이 지정되지 않으면 `button` 유형이 사용됩니다.

```blade
<x-button type="submit">
    Submit
</x-button>
```

<!-- The rendered HTML of the `button` component in this example would be: -->
이 예에서 `button` 컴포넌트의 렌더링된 HTML은 다음과 같습니다.

```blade
<button type="submit">
    Submit
</button>
```

<!-- If you would like an attribute other than `class` to have its default value and injected values joined together, you may use the `prepends` method. In this example, the `data-controller` attribute will always begin with `profile-controller` and any additional injected `data-controller` values will be placed after this default value: -->
`class` 이외의 속성에 기본값과 주입된 값을 함께 결합하려면 `prepends` 방법을 사용할 수 있습니다. 이 예에서 `data-controller` 속성은 항상 `profile-controller`로 시작하고 추가로 주입된 `data-controller` 값은 이 기본값 뒤에 배치됩니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
<!-- #### Retrieving and Filtering Attributes -->
#### Retrieving and Filtering Attributes

<!-- You may filter attributes using the `filter` method. This method accepts a closure which should return `true` if you wish to retain the attribute in the attribute bag: -->
`filter` 방법을 사용하여 속성을 필터링할 수 있습니다. 이 메소드는 속성 백에 속성을 유지하려는 경우 `true`를 반환해야 하는 클로저를 허용합니다.

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

<!-- For convenience, you may use the `whereStartsWith` method to retrieve all attributes whose keys begin with a given string: -->
편의를 위해 `whereStartsWith` 메소드를 사용하여 키가 주어진 문자열로 시작하는 모든 속성을 검색할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

<!-- Conversely, the `whereDoesntStartWith` method may be used to exclude all attributes whose keys begin with a given string: -->
반대로, `whereDoesntStartWith` 메소드는 키가 주어진 문자열로 시작하는 모든 속성을 제외하는 데 사용될 수 있습니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

<!-- Using the `first` method, you may render the first attribute in a given attribute bag: -->
`first` 메소드를 사용하면 주어진 속성 모음의 첫 번째 속성을 렌더링할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

<!-- If you would like to check if an attribute is present on the component, you may use the `has` method. This method accepts the attribute name as its only argument and returns a boolean indicating whether or not the attribute is present: -->
컴포넌트에 속성이 있는지 확인하려면 `has` 방법을 사용할 수 있습니다. 이 메소드는 속성 이름을 유일한 인수로 받아들이고 속성이 존재하는지 여부를 나타내는 부울 값을 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

<!-- If an array is passed to the `has` method, the method will determine if all of the given attributes are present on the component: -->
배열이 `has` 메소드에 전달되면 해당 메소드는 지정된 속성이 모두 컴포넌트에 있는지 확인합니다.

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

<!-- The `hasAny` method may be used to determine if any of the given attributes are present on the component: -->
`hasAny` 메소드는 주어진 속성 중 하나라도 컴포넌트에 존재하는지 확인하는 데 사용될 수 있습니다.

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

<!-- You may retrieve a specific attribute's value using the `get` method: -->
`get` 메소드를 사용하여 특정 속성의 값을 검색할 수 있습니다:

```blade
{{ $attributes->get('class') }}
```

<!-- The `only` method may be used to retrieve only the attributes with the given keys: -->
`only` 메소드는 주어진 키를 가진 속성만을 검색하는데 사용될 수 있습니다:

```blade
{{ $attributes->only(['class']) }}
```

<!-- The `except` method may be used to retrieve all attributes except those with the given keys: -->
`except` 메소드는 주어진 키를 가진 속성을 제외한 모든 속성을 검색하는 데 사용될 수 있습니다:

```blade
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
<!-- ### Reserved Keywords -->
### Reserved Keywords

<!-- By default, some keywords are reserved for Blade's internal use in order to render components. The following keywords cannot be defined as public properties or method names within your components: -->
기본적으로 일부 키워드는 컴포넌트를 렌더링하기 위해 Blade의 내부 사용을 위해 예약되어 있습니다. 다음 키워드는 컴포넌트 내에서 공용 속성이나 메서드 이름으로 정의할 수 없습니다.

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a name="slots"></a>
<!-- ### Slots -->
### Slots

<!-- You will often need to pass additional content to your component via "slots". Component slots are rendered by echoing the `$slot` variable. To explore this concept, let's imagine that an `alert` component has the following markup: -->
"슬롯"을 통해 컴포넌트에 추가 콘텐츠를 전달해야 하는 경우가 종종 있습니다. 컴포넌트 슬롯은 `$slot` 변수를 반영하여 렌더링됩니다. 이 개념을 살펴보기 위해 `alert` 컴포넌트에 다음 마크업이 있다고 가정해 보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- We may pass content to the `slot` by injecting content into the component: -->
컴포넌트에 콘텐츠를 주입하여 `slot`에 콘텐츠를 전달할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- Sometimes a component may need to render multiple different slots in different locations within the component. Let's modify our alert component to allow for the injection of a "title" slot: -->
때로는 컴포넌트가 컴포넌트 내 서로 다른 위치에 여러 개의 서로 다른 슬롯을 렌더링해야 할 수도 있습니다. "제목" 슬롯 삽입을 허용하도록 경고 컴포넌트를 수정해 보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- You may define the content of the named slot using the `x-slot` tag. Any content not within an explicit `x-slot` tag will be passed to the component in the `$slot` variable: -->
`x-slot` 태그를 사용하여 명명된 슬롯의 내용을 정의할 수 있습니다. 명시적인 `x-slot` 태그 내에 없는 모든 콘텐츠는 `$slot` 변수의 컴포넌트에 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- You may invoke a slot's `isEmpty` method to determine if the slot contains content: -->
슬롯의 `isEmpty` 메소드를 호출하여 슬롯에 콘텐츠가 포함되어 있는지 확인할 수 있습니다.

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>
```

<!-- Additionally, the `hasActualContent` method may be used to determine if the slot contains any "actual" content that is not an HTML comment: -->
또한 `hasActualContent` 메소드를 사용하여 슬롯에 HTML 주석이 아닌 "실제" 콘텐츠가 포함되어 있는지 확인할 수 있습니다.

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
<!-- #### Scoped Slots -->
#### Scoped Slots

<!-- If you have used a JavaScript framework such as Vue, you may be familiar with "scoped slots", which allow you to access data or methods from the component within your slot. You may achieve similar behavior in Laravel by defining public methods or properties on your component and accessing the component within your slot via the `$component` variable. In this example, we will assume that the `x-alert` component has a public `formatAlert` method defined on its component class: -->
Vue와 같은 JavaScript 프레임워크를 사용한 적이 있다면 슬롯 내 컴포넌트의 데이터나 메서드에 액세스할 수 있는 "범위 지정 슬롯"에 익숙할 수 있습니다. 컴포넌트에 공용 메서드나 속성을 정의하고 `$component` 변수를 통해 슬롯 내의 컴포넌트에 액세스하면 Laravel에서 유사한 동작을 얻을 수 있습니다. 이 예에서는 `x-alert` 컴포넌트의 컴포넌트 클래스에 공개 `formatAlert` 메서드가 정의되어 있다고 가정합니다.

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
<!-- #### Slot Attributes -->
#### Slot Attributes

<!-- Like Blade components, you may assign additional [attributes](#component-attributes) to slots such as CSS class names: -->
Blade 컴포넌트와 마찬가지로 CSS 클래스 이름과 같은 슬롯에 추가 [attributes](#component-attributes)을 할당할 수 있습니다.

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot:footer class="text-sm">
        Footer
    </x-slot>
</x-card>
```

<!-- To interact with slot attributes, you may access the `attributes` property of the slot's variable. For more information on how to interact with attributes, please consult the documentation on [component attributes](#component-attributes): -->
슬롯 속성과 상호 작용하려면 슬롯 변수의 `attributes` 속성에 액세스하면 됩니다. 속성과 상호 작용하는 방법에 대한 자세한 내용은 [component attributes](#component-attributes) 문서를 참조하세요.

```blade
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```

<a name="inline-component-views"></a>
<!-- ### Inline Component Views -->
### Inline Component Views

<!-- For very small components, it may feel cumbersome to manage both the component class and the component's view template. For this reason, you may return the component's markup directly from the `render` method: -->
매우 작은 컴포넌트의 경우 컴포넌트 클래스와 컴포넌트의 뷰 템플릿을 모두 관리하는 것이 번거로울 수 있습니다. 이러한 이유로 `render` 메소드에서 직접 컴포넌트의 마크업을 반환할 수 있습니다.

```php
/**
 * Get the view / contents that represent the component.
 */
public function render(): string
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```

<a name="generating-inline-view-components"></a>
<!-- #### Generating Inline View Components -->
#### Generating Inline View Components

<!-- To create a component that renders an inline view, you may use the `inline` option when executing the `make:component` command: -->
인라인 뷰를 렌더링하는 컴포넌트를 생성하려면 `make:component` 명령을 실행할 때 `inline` 옵션을 사용할 수 있습니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
<!-- ### Dynamic Components -->
### Dynamic Components

<!-- Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable: -->
때로는 컴포넌트를 렌더링해야 하지만 런타임까지 어떤 컴포넌트를 렌더링해야 하는지 알 수 없는 경우가 있습니다. 이 상황에서는 Laravel에 내장된 `dynamic-component` 컴포넌트를 사용하여 런타임 값이나 변수를 기반으로 컴포넌트를 렌더링할 수 있습니다.

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
<!-- ### Manually Registering Components -->
### Manually Registering Components

> [!WARNING]
> 컴포넌트 수동 등록에 대한 다음 문서는 주로 뷰 컴포넌트가 포함된 Laravel 패키지를 작성하는 사용자에게 적용됩니다. 패키지를 작성하지 않는 경우 컴포넌트 문서의 이 부분은 관련이 없을 수 있습니다.

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
자신의 애플리케이션에 대한 컴포넌트를 작성할 때 컴포넌트는 `app/View/Components` 디렉터리 및 `resources/views/components` 디렉터리 내에서 자동으로 검색됩니다.

<!-- However, if you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider: -->
그러나 Blade 컴포넌트를 활용하는 패키지를 구축하거나 기존 디렉토리가 아닌 디렉토리에 컴포넌트를 배치하는 경우 Laravel가 컴포넌트를 찾을 수 있는 위치를 알 수 있도록 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지 서비스 프로바이더의 `boot` 메서드에 컴포넌트를 등록해야 합니다.

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
컴포넌트가 등록되면 태그 별칭을 사용하여 렌더링될 수 있습니다.

```blade
<x-package-alert/>
```

<!-- #### Autoloading Package Components -->
#### Autoloading Package Components

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
또는 `componentNamespace` 메서드를 사용하여 규칙에 따라 컴포넌트 클래스를 자동 로드할 수도 있습니다. 예를 들어, `Nightshade` 패키지에는 `Package\Views\Components` 네임스페이스 내에 상주하는 `Calendar` 및 `ColorPicker` 컴포넌트가 있을 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
이렇게 하면 `package-name::` 구문을 사용하여 공급업체 네임스페이스에서 패키지 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 대소문자로 구분하여 이 컴포넌트에 연결된 클래스를 자동으로 감지합니다. 하위 디렉터리도 "점" 표기법을 사용하여 지원됩니다.

<a name="anonymous-components"></a>
<!-- ## Anonymous Components -->
## Anonymous Components

<!-- Similar to inline components, anonymous components provide a mechanism for managing a component via a single file. However, anonymous components utilize a single view file and have no associated class. To define an anonymous component, you only need to place a Blade template within your `resources/views/components` directory. For example, assuming you have defined a component at `resources/views/components/alert.blade.php`, you may simply render it like so: -->
인라인 컴포넌트와 유사하게 익명 컴포넌트는 단일 파일을 통해 컴포넌트를 관리하는 메커니즘을 제공합니다. 그러나 익명 컴포넌트는 단일 뷰 파일을 활용하며 연결된 클래스가 없습니다. 익명 컴포넌트를 정의하려면 `resources/views/components` 디렉터리 내에 Blade 템플릿을 배치하기만 하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 정의했다고 가정하면 다음과 같이 간단하게 렌더링할 수 있습니다.

```blade
<x-alert/>
```

<!-- You may use the `.` character to indicate if a component is nested deeper inside the `components` directory. For example, assuming the component is defined at `resources/views/components/inputs/button.blade.php`, you may render it like so: -->
`.` 문자를 사용하여 컴포넌트가 `components` 디렉터리 내부에 더 깊이 중첩되어 있는지 여부를 나타낼 수 있습니다. 예를 들어 컴포넌트가 `resources/views/components/inputs/button.blade.php`에 정의되어 있다고 가정하면 다음과 같이 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

<!-- To create an anonymous component via Artisan, you may use the `--view` flag when invoking the `make:component` command: -->
Artisan를 통해 익명 컴포넌트를 생성하려면 `make:component` 명령을 호출할 때 `--view` 플래그를 사용할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

<!-- The command above will create a Blade file at `resources/views/components/forms/input.blade.php` which can be rendered as a component via `<x-forms.input />`. -->
위 명령은 `resources/views/components/forms/input.blade.php`에 `<x-forms.input />`를 통해 컴포넌트로 렌더링될 수 있는 Blade 파일을 생성합니다.

<a name="anonymous-index-components"></a>
<!-- ### Anonymous Index Components -->
### Anonymous Index Components

<!-- Sometimes, when a component is made up of many Blade templates, you may wish to group the given component's templates within a single directory. For example, imagine an "accordion" component with the following directory structure: -->
때로는 컴포넌트가 많은 Blade 템플릿으로 구성된 경우 단일 디렉터리 내에서 지정된 컴포넌트의 템플릿을 그룹화할 수 있습니다. 예를 들어, 다음 디렉터리 구조를 가진 "아코디언" 컴포넌트를 상상해 보세요.

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<!-- This directory structure allows you to render the accordion component and its item like so: -->
이 디렉터리 구조를 사용하면 아코디언 컴포넌트와 해당 항목을 다음과 같이 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

<!-- However, in order to render the accordion component via `x-accordion`, we were forced to place the "index" accordion component template in the `resources/views/components` directory instead of nesting it within the `accordion` directory with the other accordion related templates. -->
그러나 `x-accordion`를 통해 아코디언 컴포넌트를 렌더링하기 위해 "인덱스" 아코디언 컴포넌트 템플릿을 다른 아코디언 관련 템플릿과 함께 `accordion` 디렉터리 내에 중첩하는 대신 `resources/views/components` 디렉터리에 배치해야 했습니다.

<!-- Thankfully, Blade allows you to place a file matching the component's directory name within the component's directory itself. When this template exists, it can be rendered as the "root" element of the component even though it is nested within a directory. So, we can continue to use the same Blade syntax given in the example above; however, we will adjust our directory structure like so: -->
다행히도 Blade를 사용하면 컴포넌트의 디렉터리 이름과 일치하는 파일을 컴포넌트의 디렉터리 자체에 배치할 수 있습니다. 이 템플릿이 존재하면 디렉터리 내에 중첩되어 있더라도 컴포넌트의 "루트" 요소로 렌더링될 수 있습니다. 따라서 위의 예에 제공된 것과 동일한 Blade 구문을 계속 사용할 수 있습니다. 그러나 디렉토리 구조를 다음과 같이 조정하겠습니다.

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
<!-- ### Data Properties / Attributes -->
### Data Properties / Attributes

<!-- Since anonymous components do not have any associated class, you may wonder how you may differentiate which data should be passed to the component as variables and which attributes should be placed in the component's [attribute bag](#component-attributes). -->
익명 컴포넌트에는 연결된 클래스가 없으므로 컴포넌트에 변수로 전달되어야 하는 데이터와 컴포넌트의 [attribute bag](#component-attributes)에 배치되어야 하는 속성을 어떻게 구별할 수 있는지 궁금할 수 있습니다.

<!-- You may specify which attributes should be considered data variables using the `@props` directive at the top of your component's Blade template. All other attributes on the component will be available via the component's attribute bag. If you wish to give a data variable a default value, you may specify the variable's name as the array key and the default value as the array value: -->
컴포넌트의 Blade 템플릿 상단에 있는 `@props` 지시어를 사용하여 데이터 변수로 간주되어야 하는 속성을 지정할 수 있습니다. 컴포넌트의 다른 모든 속성은 컴포넌트의 속성 모음을 통해 사용할 수 있습니다. 데이터 변수에 기본값을 지정하려면 변수 이름을 배열 키로 지정하고 기본값을 배열 값으로 지정할 수 있습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- Given the component definition above, we may render the component like so: -->
위의 컴포넌트 정의가 주어지면 컴포넌트를 다음과 같이 렌더링할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
<!-- ### Accessing Parent Data -->
### Accessing Parent Data

<!-- Sometimes you may want to access data from a parent component inside a child component. In these cases, you may use the `@aware` directive. For example, imagine we are building a complex menu component consisting of a parent `<x-menu>` and child `<x-menu.item>`: -->
때로는 하위 컴포넌트 내부의 상위 컴포넌트에서 데이터에 액세스하고 싶을 수도 있습니다. 이러한 경우 `@aware` 지시문을 사용할 수 있습니다. 예를 들어, 상위 `<x-menu>`와 하위 `<x-menu.item>`로 구성된 복잡한 메뉴 컴포넌트를 구축한다고 가정해 보겠습니다.

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

<!-- The `<x-menu>` component may have an implementation like the following: -->
`<x-menu>` 컴포넌트는 다음과 같은 구현을 가질 수 있습니다.

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

<!-- Because the `color` prop was only passed into the parent (`<x-menu>`), it won't be available inside `<x-menu.item>`. However, if we use the `@aware` directive, we can make it available inside `<x-menu.item>` as well: -->
`color` 소품은 상위(`<x-menu>`)에만 전달되었으므로 `<x-menu.item>` 내에서는 사용할 수 없습니다. 그러나 `@aware` 지시어를 사용하면 `<x-menu.item>` 내부에서도 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시문은 HTML 속성을 통해 상위 컴포넌트에 명시적으로 전달되지 않은 상위 ​​데이터에 액세스할 수 없습니다. 상위 컴포넌트에 명시적으로 전달되지 않은 기본 `@props` 값은 `@aware` 지시어로 액세스할 수 없습니다.

<a name="anonymous-component-paths"></a>
<!-- ### Anonymous Component Paths -->
### Anonymous Component Paths

<!-- As previously discussed, anonymous components are typically defined by placing a Blade template within your `resources/views/components` directory. However, you may occasionally want to register other anonymous component paths with Laravel in addition to the default path. -->
이전에 설명한 대로 익명 컴포넌트는 일반적으로 `resources/views/components` 디렉터리 내에 Blade 템플릿을 배치하여 정의됩니다. 그러나 기본 경로 외에 Laravel을 사용하여 다른 익명 컴포넌트 경로를 등록하려는 경우도 있습니다.

<!-- The `anonymousComponentPath` method accepts the "path" to the anonymous component location as its first argument and an optional "namespace" that components should be placed under as its second argument. Typically, this method should be called from the `boot` method of one of your application's [service providers](/docs/13.x/providers): -->
`anonymousComponentPath` 메소드는 익명 컴포넌트 위치에 대한 "경로"를 첫 번째 인수로 받아들이고 컴포넌트가 배치되어야 하는 선택적 "네임스페이스"를 두 번째 인수로 받아들입니다. 일반적으로 이 메소드는 애플리케이션의 [service providers](/docs/13.x/providers) 중 하나의 `boot` 메소드에서 호출되어야 합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

<!-- When component paths are registered without a specified prefix as in the example above, they may be rendered in your Blade components without a corresponding prefix as well. For example, if a `panel.blade.php` component exists in the path registered above, it may be rendered like so: -->
위의 예와 같이 지정된 접두사 없이 컴포넌트 경로가 등록되면 해당 접두사 없이 Blade 컴포넌트에서도 렌더링될 수 있습니다. 예를 들어 위에서 등록한 경로에 `panel.blade.php` 컴포넌트가 존재하는 경우 다음과 같이 렌더링될 수 있습니다.

```blade
<x-panel />
```

<!-- Prefix "namespaces" may be provided as the second argument to the `anonymousComponentPath` method: -->
접두사 "네임스페이스"는 `anonymousComponentPath` 메소드의 두 번째 인수로 제공될 수 있습니다.

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

<!-- When a prefix is provided, components within that "namespace" may be rendered by prefixing the component's namespace to the component name when the component is rendered: -->
접두사가 제공되면 해당 "네임스페이스" 내의 컴포넌트는 컴포넌트가 렌더링될 때 컴포넌트 이름에 컴포넌트의 네임스페이스 접두사를 추가하여 렌더링될 수 있습니다.

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
<!-- ## Building Layouts -->
## Building Layouts

<a name="layouts-using-components"></a>
<!-- ### Layouts Using Components -->
### Layouts Using Components

<!-- Most web applications maintain the same general layout across various pages. It would be incredibly cumbersome and hard to maintain our application if we had to repeat the entire layout HTML in every view we create. Thankfully, it's convenient to define this layout as a single [Blade component](#components) and then use it throughout our application. -->
대부분의 웹 애플리케이션은 다양한 페이지에서 동일한 일반 레이아웃을 유지합니다. 우리가 생성하는 모든 뷰에서 전체 레이아웃 HTML을 반복해야 한다면 애플리케이션을 유지 관리하는 것이 엄청나게 번거롭고 어려울 것입니다. 다행히도 이 레이아웃을 단일 [Blade component](#components)로 정의한 다음 애플리케이션 전체에서 사용하는 것이 편리합니다.

<a name="defining-the-layout-component"></a>
<!-- #### Defining the Layout Component -->
#### Defining the Layout Component

<!-- For example, imagine we are building a "todo" list application. We might define a `layout` component that looks like the following: -->
예를 들어, "todo" 목록 애플리케이션을 구축한다고 가정해 보겠습니다. 다음과 같은 `layout` 컴포넌트를 정의할 수 있습니다.

```blade
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```

<a name="applying-the-layout-component"></a>
<!-- #### Applying the Layout Component -->
#### Applying the Layout Component

<!-- Once the `layout` component has been defined, we may create a Blade view that utilizes the component. In this example, we will define a simple view that displays our task list: -->
`layout` 컴포넌트가 정의되면 해당 컴포넌트를 활용하는 Blade 뷰를 만들 수 있습니다. 이 예에서는 작업 목록을 표시하는 간단한 뷰를 정의합니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

<!-- Remember, content that is injected into a component will be supplied to the default `$slot` variable within our `layout` component. As you may have noticed, our `layout` also respects a `$title` slot if one is provided; otherwise, a default title is shown. We may inject a custom title from our task list view using the standard slot syntax discussed in the [component documentation](#components): -->
컴포넌트에 삽입된 콘텐츠는 `layout` 컴포넌트 내의 기본 `$slot` 변수에 제공됩니다. 아시다시피 `layout`는 `$title` 슬롯이 제공되는 경우 이를 존중합니다. 그렇지 않으면 기본 제목이 표시됩니다. [component documentation](#components)에 설명된 표준 슬롯 구문을 사용하여 작업 목록 뷰에서 사용자 지정 제목을 삽입할 수 있습니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

<!-- Now that we have defined our layout and task list views, we just need to return the `task` view from a route: -->
이제 레이아웃과 작업 목록 뷰를 정의했으므로 라우트에서 `task` 뷰를 반환하면 됩니다.

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
<!-- ### Layouts Using Template Inheritance -->
### Layouts Using Template Inheritance

<a name="defining-a-layout"></a>
<!-- #### Defining a Layout -->
#### Defining a Layout

<!-- Layouts may also be created via "template inheritance". This was the primary way of building applications prior to the introduction of [components](#components). -->
레이아웃은 "템플릿 상속"을 통해 생성될 수도 있습니다. 이는 [components](#components)가 도입되기 전에 애플리케이션을 구축하는 기본 방법이었습니다.

<!-- To get started, let's take a look at a simple example. First, we will examine a page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view: -->
시작하려면 간단한 예를 살펴보겠습니다. 먼저 페이지 레이아웃을 살펴보겠습니다. 대부분의 웹 애플리케이션은 다양한 페이지에서 동일한 일반 레이아웃을 유지하므로 이 레이아웃을 단일 Blade 뷰로 정의하는 것이 편리합니다.

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

<!-- As you can see, this file contains typical HTML mark-up. However, take note of the `@section` and `@yield` directives. The `@section` directive, as the name implies, defines a section of content, while the `@yield` directive is used to display the contents of a given section. -->
보시다시피 이 파일에는 일반적인 HTML 마크업이 포함되어 있습니다. 그러나 `@section` 및 `@yield` 지시어에 유의하세요. `@section` 지시문은 이름에서 알 수 있듯이 콘텐츠 섹션을 정의하는 반면 `@yield` 지시문은 지정된 섹션의 콘텐츠를 표시하는 데 사용됩니다.

<!-- Now that we have defined a layout for our application, let's define a child page that inherits the layout. -->
이제 애플리케이션의 레이아웃을 정의했으므로 레이아웃을 상속하는 하위 페이지를 정의해 보겠습니다.

<a name="extending-a-layout"></a>
<!-- #### Extending a Layout -->
#### Extending a Layout

<!-- When defining a child view, use the `@extends` Blade directive to specify which layout the child view should "inherit". Views which extend a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`: -->
하위 뷰를 정의할 때 `@extends` Blade 지시문을 사용하여 하위 뷰가 "상속"해야 하는 레이아웃을 지정합니다. Blade 레이아웃을 확장하는 뷰는 `@section` 지시문을 사용하여 레이아웃 섹션에 콘텐츠를 삽입할 수 있습니다. 위의 예에서 볼 수 있듯이 이러한 섹션의 내용은 `@yield`를 사용하여 레이아웃에 표시됩니다.

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

<!-- In this example, the `sidebar` section is utilizing the `@@parent` directive to append (rather than overwriting) content to the layout's sidebar. The `@@parent` directive will be replaced by the content of the layout when the view is rendered. -->
이 예에서 `sidebar` 섹션은 `@@parent` 지시문을 활용하여 레이아웃의 사이드바에 콘텐츠를 덮어쓰는 대신 추가합니다. `@@parent` 지시어는 뷰가 렌더링될 때 레이아웃의 내용으로 대체됩니다.

> [!NOTE]
> 이전 예와 달리 이 `sidebar` 섹션은 `@show` 대신 `@endsection`로 끝납니다. `@endsection` 지시문은 섹션만 정의하는 반면, `@show`는 섹션을 정의하고 **즉시 생성**합니다.

<!-- The `@yield` directive also accepts a default value as its second parameter. This value will be rendered if the section being yielded is undefined: -->
`@yield` 지시문은 두 번째 매개변수로 기본값을 허용합니다. 생성되는 섹션이 정의되지 않은 경우 이 값이 렌더링됩니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
<!-- ## Forms -->
## Forms

<a name="csrf-field"></a>
<!-- ### CSRF Field -->
### CSRF Field

<!-- Anytime you define an HTML form in your application, you should include a hidden CSRF token field in the form so that [the CSRF protection](/docs/13.x/csrf) middleware can validate the request. You may use the `@csrf` Blade directive to generate the token field: -->
애플리케이션에서 HTML 양식을 정의할 때마다 [the CSRF protection](/docs/13.x/csrf) 미들웨어가 요청을 확인할 수 있도록 양식에 숨겨진 CSRF 토큰 필드를 포함해야 합니다. `@csrf` Blade 지시문을 사용하여 토큰 필드를 생성할 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
<!-- ### Method Field -->
### Method Field

<!-- Since HTML forms can't make `PUT`, `PATCH`, or `DELETE` requests, you will need to add a hidden `_method` field to spoof these HTTP verbs. The `@method` Blade directive can create this field for you: -->
HTML 양식은 `PUT`, `PATCH` 또는 `DELETE` 요청을 만들 수 없으므로 이러한 HTTP 동사를 스푸핑하려면 숨겨진 `_method` 필드를 추가해야 합니다. `@method` Blade 지시어는 다음 필드를 생성할 수 있습니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
<!-- ### Validation Errors -->
### Validation Errors

<!-- The `@error` directive may be used to quickly check if [validation error messages](/docs/13.x/validation#quick-displaying-the-validation-errors) exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
`@error` 지시문을 사용하면 특정 속성에 [validation error messages](/docs/13.x/validation#quick-displaying-the-validation-errors)가 있는지 빠르게 확인할 수 있습니다. `@error` 지시문 내에서 `$message` 변수를 에코하여 오류 메시지를 표시할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- Since the `@error` directive compiles to an "if" statement, you may use the `@else` directive to render content when there is not an error for an attribute: -->
`@error` 지시문은 "if" 문으로 컴파일되므로 속성에 오류가 없을 때 `@else` 지시문을 사용하여 콘텐츠를 렌더링할 수 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

<!-- You may pass [the name of a specific error bag](/docs/13.x/validation#named-error-bags) as the second parameter to the `@error` directive to retrieve validation error messages on pages containing multiple forms: -->
[the name of a specific error bag](/docs/13.x/validation#named-error-bags)을 `@error` 지시문의 두 번째 매개변수로 전달하여 여러 양식이 포함된 페이지에서 유효성 검사 오류 메시지를 검색할 수 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror"
/>

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
<!-- ## Stacks -->
## Stacks

<!-- Blade allows you to push to named stacks which can be rendered somewhere else in another view or layout. This can be particularly useful for specifying any JavaScript libraries required by your child views: -->
Blade를 사용하면 다른 뷰 또는 레이아웃의 다른 위치에 렌더링될 수 있는 명명된 스택으로 푸시할 수 있습니다. 이는 자녀 뷰에 필요한 JavaScript 라이브러리를 지정하는 데 특히 유용할 수 있습니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

<!-- If you would like to `@push` content if a given boolean expression evaluates to `true`, you may use the `@pushIf` directive: -->
주어진 부울 표현식이 `true`로 평가되는 경우 `@push` 콘텐츠를 원하는 경우 `@pushIf` 지시문을 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

<!-- You may push to a stack as many times as needed. To render the complete stack contents, pass the name of the stack to the `@stack` directive: -->
필요한 만큼 여러 번 스택에 푸시할 수 있습니다. 전체 스택 내용을 렌더링하려면 스택 이름을 `@stack` 지시어에 전달하세요.

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

<!-- If you would like to prepend content onto the beginning of a stack, you should use the `@prepend` directive: -->
스택 시작 부분에 콘텐츠를 추가하려면 `@prepend` 지시문을 사용해야 합니다.

```blade
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```

<!-- The `@hasstack` directive may be used to determine if a stack is empty: -->
`@hasstack` 지시어는 스택이 비어 있는지 확인하는 데 사용될 수 있습니다.

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a name="service-injection"></a>
<!-- ## Service Injection -->
## Service Injection

<!-- The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/13.x/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class or interface name of the service you wish to resolve: -->
`@inject` 지시어는 Laravel [service container](/docs/13.x/container)에서 서비스를 검색하는 데 사용될 수 있습니다. `@inject`에 전달된 첫 번째 인수는 서비스가 배치될 변수의 이름이고, 두 번째 인수는 해결하려는 서비스의 클래스 또는 인터페이스 이름입니다.

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
<!-- ## Rendering Inline Blade Templates -->
## Rendering Inline Blade Templates

<!-- Sometimes you may need to transform a raw Blade template string into valid HTML. You may accomplish this using the `render` method provided by the `Blade` facade. The `render` method accepts the Blade template string and an optional array of data to provide to the template: -->
때로는 원시 Blade 템플릿 문자열을 유효한 HTML로 변환해야 할 수도 있습니다. `Blade` 파사드에서 제공하는 `render` 메소드를 사용하여 이를 수행할 수 있습니다. `render` 메서드는 Blade 템플릿 문자열과 템플릿에 제공할 선택적 데이터 배열을 허용합니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

<!-- Laravel renders inline Blade templates by writing them to the `storage/framework/views` directory. If you would like Laravel to remove these temporary files after rendering the Blade template, you may provide the `deleteCachedView` argument to the method: -->
Laravel는 인라인 Blade 템플릿을 `storage/framework/views` 디렉터리에 작성하여 렌더링합니다. Blade 템플릿을 렌더링한 후 Laravel가 이러한 임시 파일을 제거하도록 하려면 메서드에 `deleteCachedView` 인수를 제공할 수 있습니다.

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
<!-- ## Rendering Blade Fragments -->
## Rendering Blade Fragments

<!-- When using frontend frameworks such as [Turbo](https://turbo.hotwired.dev/) and [htmx](https://htmx.org/), you may occasionally need to only return a portion of a Blade template within your HTTP response. Blade "fragments" allow you to do just that. To get started, place a portion of your Blade template within `@fragment` and `@endfragment` directives: -->
[Turbo](https://turbo.hotwired.dev/) 및 [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때 때때로 HTTP 응답 내에서 Blade 템플릿의 일부만 반환해야 할 수도 있습니다. Blade "조각"을 사용하면 바로 이러한 작업을 수행할 수 있습니다. 시작하려면 `@fragment` 및 `@endfragment` 지시문 내에 Blade 템플릿의 일부를 배치하세요.

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

<!-- Then, when rendering the view that utilizes this template, you may invoke the `fragment` method to specify that only the specified fragment should be included in the outgoing HTTP response: -->
그런 다음 이 템플릿을 활용하는 뷰를 렌더링할 때 `fragment` 메서드를 호출하여 지정된 조각만 나가는 HTTP 응답에 포함되도록 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

<!-- The `fragmentIf` method allows you to conditionally return a fragment of a view based on a given condition. Otherwise, the entire view will be returned: -->
`fragmentIf` 메서드를 사용하면 주어진 조건에 따라 뷰의 조각을 조건부로 반환할 수 있습니다. 그렇지 않으면 전체 뷰가 반환됩니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

<!-- The `fragments` and `fragmentsIf` methods allow you to return multiple view fragments in the response. The fragments will be concatenated together: -->
`fragments` 및 `fragmentsIf` 메서드를 사용하면 응답에서 여러 뷰 조각을 반환할 수 있습니다. 조각은 서로 연결됩니다.

```php
view('dashboard', ['users' => $users])
    ->fragments(['user-list', 'comment-list']);

view('dashboard', ['users' => $users])
    ->fragmentsIf(
        $request->hasHeader('HX-Request'),
        ['user-list', 'comment-list']
    );
```

<a name="extending-blade"></a>
<!-- ## Extending Blade -->
## Extending Blade

<!-- Blade allows you to define your own custom directives using the `directive` method. When the Blade compiler encounters the custom directive, it will call the provided callback with the expression that the directive contains. -->
Blade를 사용하면 `directive` 메서드를 사용하여 사용자 지정 지시문을 정의할 수 있습니다. Blade 컴파일러는 사용자 지정 지시문을 발견하면 지시문에 포함된 표현식을 사용하여 제공된 콜백을 호출합니다.

<!-- The following example creates a `@datetime($var)` directive which formats a given `$var`, which should be an instance of `DateTime`: -->
다음 예에서는 `DateTime`의 인스턴스여야 하는 지정된 `$var`의 형식을 지정하는 `@datetime($var)` 지시어를 생성합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

<!-- As you can see, we will chain the `format` method onto whatever expression is passed into the directive. So, in this example, the final PHP generated by this directive will be: -->
보시다시피 지시문에 전달되는 표현식에 `format` 메서드를 연결합니다. 따라서 이 예에서 이 지시어에 의해 생성된 최종 PHP는 다음과 같습니다.

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 지시문의 논리를 업데이트한 후에는 캐시된 Blade 뷰를 모두 삭제해야 합니다. 캐시된 Blade 뷰는 `view:clear` Artisan 명령을 사용하여 제거할 수 있습니다.

<a name="custom-echo-handlers"></a>
<!-- ### Custom Echo Handlers -->
### Custom Echo Handlers

<!-- If you attempt to "echo" an object using Blade, the object's `__toString` method will be invoked. The [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
Blade를 사용하여 개체를 "에코"하려고 하면 개체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "마법 메서드" 중 하나입니다. 그러나 상호 작용하는 클래스가 타사 라이브러리에 속하는 경우와 같이 특정 클래스의 `__toString` 메서드를 제어할 수 없는 경우도 있습니다.

<!-- In these cases, Blade allows you to register a custom echo handler for that particular type of object. To accomplish this, you should invoke Blade's `stringable` method. The `stringable` method accepts a closure. This closure should type-hint the type of object that it is responsible for rendering. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이러한 경우 Blade를 사용하면 특정 유형의 개체에 대한 사용자 지정 에코 처리기를 등록할 수 있습니다. 이를 수행하려면 Blade의 `stringable` 메서드를 호출해야 합니다. `stringable` 메소드는 클로저를 허용합니다. 이 클로저는 렌더링을 담당하는 객체의 유형을 유형 힌트해야 합니다. 일반적으로 `stringable` 메서드는 애플리케이션 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출되어야 합니다.

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<!-- Once your custom echo handler has been defined, you may simply echo the object in your Blade template: -->
사용자 지정 에코 핸들러가 정의되면 Blade 템플릿에 객체를 간단히 에코할 수 있습니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
<!-- ### Custom If Statements -->
### Custom If Statements

<!-- Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade provides a `Blade::if` method which allows you to quickly define custom conditional directives using closures. For example, let's define a custom conditional that checks the configured default "disk" for the application. We may do this in the `boot` method of our `AppServiceProvider`: -->
사용자 지정 지시어 프로그래밍은 간단한 사용자 지정 조건문을 정의할 때 필요한 것보다 더 복잡한 경우가 있습니다. 이러한 이유로 Blade는 클로저를 사용하여 사용자 지정 조건부 지시문을 빠르게 정의할 수 있는 `Blade::if` 메서드를 제공합니다. 예를 들어, 애플리케이션에 대해 구성된 기본 "디스크"를 확인하는 사용자 지정 조건을 정의해 보겠습니다. `AppServiceProvider`의 `boot` 메서드에서 이 작업을 수행할 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

<!-- Once the custom conditional has been defined, you can use it within your templates: -->
사용자 지정 조건이 정의되면 템플릿 내에서 사용할 수 있습니다.

```blade
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```
