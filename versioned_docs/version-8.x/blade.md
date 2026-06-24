<!-- # Blade Templates -->
# Blade Templates

- [Introduction](#introduction)
- [Displaying Data](#displaying-data)
    - [HTML Entity Encoding](#html-entity-encoding)
    - [Blade & JavaScript Frameworks](#blade-and-javascript-frameworks)
- [Blade Directives](#blade-directives)
    - [If Statements](#if-statements)
    - [Switch Statements](#switch-statements)
    - [Loops](#loops)
    - [The Loop Variable](#the-loop-variable)
    - [Conditional Classes](#conditional-classes)
    - [Including Subviews](#including-subviews)
    - [The `@once` Directive](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [Comments](#comments)
- [Components](#components)
    - [Rendering Components](#rendering-components)
    - [Passing Data To Components](#passing-data-to-components)
    - [Component Attributes](#component-attributes)
    - [Reserved Keywords](#reserved-keywords)
    - [Slots](#slots)
    - [Inline Component Views](#inline-component-views)
    - [Anonymous Components](#anonymous-components)
    - [Dynamic Components](#dynamic-components)
    - [Manually Registering Components](#manually-registering-components)
- [Building Layouts](#building-layouts)
    - [Layouts Using Components](#layouts-using-components)
    - [Layouts Using Template Inheritance](#layouts-using-template-inheritance)
- [Forms](#forms)
    - [CSRF Field](#csrf-field)
    - [Method Field](#method-field)
    - [Validation Errors](#validation-errors)
- [Stacks](#stacks)
- [Service Injection](#service-injection)
- [Extending Blade](#extending-blade)
    - [Custom Echo Handlers](#custom-echo-handlers)
    - [Custom If Statements](#custom-if-statements)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Blade is the simple, yet powerful templating engine that is included with Laravel. Unlike some PHP templating engines, Blade does not restrict you from using plain PHP code in your templates. In fact, all Blade templates are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade template files use the `.blade.php` file extension and are typically stored in the `resources/views` directory. -->
블레이드(Blade)는 Laravel에 기본 포함된 간결하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, 블레이드는 템플릿 내에서 일반 PHP 코드를 자유롭게 사용할 수 있도록 제한하지 않습니다. 실제로, 블레이드 템플릿은 모두 일반 PHP 코드로 컴파일되어 수정될 때까지 캐싱됩니다. 따라서 블레이드가 애플리케이션에 거의 성능 오버헤드를 발생시키지 않습니다. 블레이드 템플릿 파일의 확장자는 `.blade.php`이며, 보통 `resources/views` 디렉터리에 저장됩니다.

<!-- Blade views may be returned from routes or controller using the global `view` helper. Of course, as mentioned in the documentation on [views](/docs/8.x/views), data may be passed to the Blade view using the `view` helper's second argument: -->
블레이드 뷰는 라우트 또는 컨트롤러에서 전역 `view` 헬퍼를 사용해 반환할 수 있습니다. 물론, [views](/docs/8.x/views) 문서에서 언급한 것처럼, `view` 헬퍼의 두 번째 인수를 통해 데이터도 블레이드 뷰로 전달할 수 있습니다.

```
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

> [!TIP]
> 블레이드 템플릿으로 더욱 동적인 인터페이스를 쉽고 빠르게 만들고 싶으신가요? [Laravel Livewire](https://laravel-livewire.com)를 확인해보시기 바랍니다.

<a name="displaying-data"></a>
<!-- ## Displaying Data -->
## Displaying Data

<!-- You may display data that is passed to your Blade views by wrapping the variable in curly braces. For example, given the following route: -->
블레이드 뷰에 전달된 데이터를 중괄호로 감싸서 화면에 출력할 수 있습니다. 예를 들어, 다음과 같은 라우트가 있다고 가정해보겠습니다.

```
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

<!-- You may display the contents of the `name` variable like so: -->
이 예시에서 `name` 변수를 다음과 같이 표시할 수 있습니다.

```
Hello, {{ $name }}.
```

> [!TIP]
> 블레이드의 `{{ }}` 이코(출력) 문은 XSS 공격을 예방하기 위해 PHP의 `htmlspecialchars` 함수로 자동 처리됩니다.

<!-- You are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement: -->
뷰에 전달된 변수 값만 출력할 수 있는 것은 아닙니다. 어떠한 PHP 함수의 결과도 이코로 표시할 수 있습니다. 실제로 원하는 어떤 PHP 코드든 블레이드의 이코 문에 자유롭게 사용할 수 있습니다.

```
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
<!-- ### HTML Entity Encoding -->
### HTML Entity Encoding

<!-- By default, Blade (and the Laravel `e` helper) will double encode HTML entities. If you would like to disable double encoding, call the `Blade::withoutDoubleEncoding` method from the `boot` method of your `AppServiceProvider`: -->
기본적으로 블레이드(그리고 Laravel의 `e` 헬퍼)는 HTML 엔터티를 이중 인코딩합니다. 이중 인코딩을 사용하지 않으려면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출해주면 됩니다.

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
<!-- #### Displaying Unescaped Data -->
#### Displaying Unescaped Data

<!-- By default, Blade `{{ }}` statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax: -->
기본적으로 블레이드 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수를 거칩니다. 만약 데이터를 이스케이프하지 않고 그대로 출력하려면 다음과 같은 구문을 사용할 수 있습니다.

```
Hello, {!! $name !!}.
```

> [!NOTE]
> 애플리케이션 사용자가 제공한 콘텐츠를 출력할 때는 특히 주의해야 합니다. 사용자 제공 데이터는 항상 이스케이프되는 이중 중괄호 구문을 사용해 XSS 공격을 예방하는 것이 좋습니다.

<a name="blade-and-javascript-frameworks"></a>
<!-- ### Blade & JavaScript Frameworks -->
### Blade & JavaScript Frameworks

<!-- Since many JavaScript frameworks also use "curly" braces to indicate a given expression should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example: -->
많은 자바스크립트 프레임워크에서도 화면에 표현할 값을 "중괄호(curly)"로 감싸서 표시합니다. 이럴 때 블레이드는 `@` 기호를 사용하여 렌더링 엔진이 해당 표현식을 건드리지 않도록 할 수 있습니다. 예를 들면 다음과 같습니다.

```
<h1>Laravel</h1>

Hello, @{{ name }}.
```

<!-- In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to be rendered by your JavaScript framework. -->
이 예시의 경우, 블레이드는 `@` 기호를 제거하지만, `{{ name }}` 표현식 자체는 변경하지 않습니다. 따라서 자바스크립트 프레임워크가 해당 내용을 제대로 렌더링할 수 있습니다.

<!-- The `@` symbol may also be used to escape Blade directives: -->
또한, `@` 기호를 사용해 블레이드 디렉티브를 이스케이프(출력 자체는 그대로)할 수도 있습니다.

```
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
<!-- #### Rendering JSON -->
#### Rendering JSON

<!-- Sometimes you may pass an array to your view with the intention of rendering it as JSON in order to initialize a JavaScript variable. For example: -->
자바스크립트 변수를 초기화하기 위해 배열을 뷰로 전달하고, 이를 JSON 형식으로 출력하고 싶을 때가 있습니다. 예를 들어,

```
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

<!-- However, instead of manually calling `json_encode`, you may use the `Illuminate\Support\Js::from` method directive. The `from` method accepts the same arguments as PHP's `json_encode` function; however, it will ensure that the resulting JSON is properly escaped for inclusion within HTML quotes. The `from` method will return a string `JSON.parse` JavaScript statement that will convert the given object or array into a valid JavaScript object: -->
이렇게 직접 `json_encode`를 호출하지 않고, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용하는 것이 더 좋습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받으며, 결과 JSON이 HTML 속성 값 등에서 안전하게 사용될 수 있도록 적절히 이스케이프해줍니다. `from` 메서드는 주어진 객체나 배열을 올바른 자바스크립트 객체로 변환하는 `JSON.parse` 자바스크립트 구문 문자열을 반환합니다.

```
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

<!-- The latest versions of the Laravel application skeleton include a `Js` facade, which provides convenient access to this functionality within your Blade templates: -->
최신 버전의 Laravel 기본 코드에는 이 기능을 블레이드에서 더 편리하게 사용할 수 있도록 `Js` 파사드가 포함되어 있습니다.

```
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!NOTE]
> 이미 존재하는 변수만 `Js::from` 메서드로 JSON 처리해야 합니다. 블레이드 템플릿은 정규 표현식에 기반하고 있기 때문에 복잡한 식을 이 디렉티브에 전달하면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
<!-- #### The `@verbatim` Directive -->
#### The `@verbatim` Directive

<!-- If you are displaying JavaScript variables in a large portion of your template, you may wrap the HTML in the `@verbatim` directive so that you do not have to prefix each Blade echo statement with an `@` symbol: -->
템플릿의 넓은 영역에서 자바스크립트 변수를 표시해야 한다면, `@verbatim` 디렉티브로 해당 HTML 구역을 감싸서 각 Blade 출력 구문마다 `@` 기호를 붙이지 않아도 되도록 할 수 있습니다.

```
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
블레이드는 템플릿 상속과 데이터 표시 외에도, 조건문이나 반복문 등 PHP의 일반적인 제어문 구조에 대한 간편한 단축 구문을 제공합니다. 이를 통해 PHP의 원래 구조와 익숙하면서도, 훨씬 간결하고 보기 좋은 문법으로 사용할 수 있습니다.

<a name="if-statements"></a>
<!-- ### If Statements -->
### If Statements

<!-- You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts: -->
`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 사용해 `if`문을 만들 수 있습니다. 이 디렉티브들은 PHP의 원래 if문과 완전히 동일하게 동작합니다.

```
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

<!-- For convenience, Blade also provides an `@unless` directive: -->
편의상, 블레이드에는 `@unless` 디렉티브도 준비되어 있습니다.

```
@unless (Auth::check())
    You are not signed in.
@endunless
```

<!-- In addition to the conditional directives already discussed, the `@isset` and `@empty` directives may be used as convenient shortcuts for their respective PHP functions: -->
이미 설명한 조건문 외에도, `@isset` 및 `@empty` 디렉티브를 사용해 대응하는 PHP 함수처럼 간단히 활용할 수 있습니다.

```
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

<!-- The `@auth` and `@guest` directives may be used to quickly determine if the current user is [authenticated](/docs/8.x/authentication) or is a guest: -->
`@auth` 및 `@guest` 디렉티브를 사용하면 현재 사용자가 [authenticated](/docs/8.x/authentication)인지, 혹은 게스트(비로그인)인지 간단히 확인할 수 있습니다.

```
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

<!-- If needed, you may specify the authentication guard that should be checked when using the `@auth` and `@guest` directives: -->
필요하다면 `@auth`와 `@guest` 디렉티브에서 검사할 인증 가드를 지정할 수 있습니다.

```
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
`@production` 디렉티브로 애플리케이션이 운영 환경에서 실행 중인지 확인할 수 있습니다.

```
@production
    // Production specific content...
@endproduction
```

<!-- Or, you may determine if the application is running in a specific environment using the `@env` directive: -->
또한 `@env` 디렉티브를 써서, 애플리케이션이 특정 환경에서 실행 중인지 확인할 수 있습니다.

```
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
템플릿 상속의 섹션에 내용이 있는지 `@hasSection` 디렉티브로 확인할 수 있습니다.

```html
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

<!-- You may use the `sectionMissing` directive to determine if a section does not have content: -->
섹션에 내용이 없는 경우를 확인하려면 `sectionMissing` 디렉티브를 사용할 수 있습니다.

```html
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="switch-statements"></a>
<!-- ### Switch Statements -->
### Switch Statements

<!-- Switch statements can be constructed using the `@switch`, `@case`, `@break`, `@default` and `@endswitch` directives: -->
`@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 이용해 switch문을 만들 수 있습니다.

```
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
조건문 외에도, 블레이드는 PHP 반복문 구조를 위한 간단한 디렉티브를 제공합니다. 이들 디렉티브 역시 각각의 PHP 반복문과 정확히 같은 방식으로 동작합니다.

```
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

> [!TIP]
> `foreach` 반복문에서 반복에 대한 다양한 정보를 제공하는 [loop variable](#the-loop-variable)를 활용할 수 있습니다. 예를 들어, 루프의 첫 번째 또는 마지막 반복인지 확인할 수 있습니다.

<!-- When using loops you may also end the loop or skip the current iteration using the `@continue` and `@break` directives: -->
반복문 안에서 `@continue`와 `@break` 디렉티브를 사용해, 반복을 건너뛰거나 중단할 수도 있습니다.

```
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
이때, continue 또는 break 조건을 디렉티브 선언문 안에 바로 작성할 수도 있습니다.

```
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
`foreach` 반복문을 사용할 때, 반복문 내부에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수로 반복문의 현재 인덱스, 첫번째/마지막 반복 여부 등 다양한 정보를 얻을 수 있습니다.

```
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
중첩 반복문에서는 부모 반복문의 `$loop` 변수에 `parent` 속성을 통해 접근할 수 있습니다.

```
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

<!-- The `$loop` variable also contains a variety of other useful properties: -->
`$loop` 변수는 아래와 같은 다양한 유용한 속성을 제공합니다.

<!--
Property  | Description
------------- | -------------
`$loop->index`  |  The index of the current loop iteration (starts at 0).
`$loop->iteration`  |  The current loop iteration (starts at 1).
`$loop->remaining`  |  The iterations remaining in the loop.
`$loop->count`  |  The total number of items in the array being iterated.
`$loop->first`  |  Whether this is the first iteration through the loop.
`$loop->last`  |  Whether this is the last iteration through the loop.
`$loop->even`  |  Whether this is an even iteration through the loop.
`$loop->odd`  |  Whether this is an odd iteration through the loop.
`$loop->depth`  |  The nesting level of the current loop.
`$loop->parent`  |  When in a nested loop, the parent's loop variable.
-->
속성  | 설명
------------- | -------------
`$loop->index`  |  현재 반복 인덱스 (0부터 시작)
`$loop->iteration`  |  현재 반복 횟수 (1부터 시작)
`$loop->remaining`  |  반복이 남은 횟수
`$loop->count`  |  배열(컬렉션)의 전체 항목 수
`$loop->first`  |  첫 반복인지 여부
`$loop->last`  |  마지막 반복인지 여부
`$loop->even`  |  반복이 짝수번째인지 여부
`$loop->odd`  |  반복이 홀수번째인지 여부
`$loop->depth`  |  중첩 반복문의 깊이
`$loop->parent`  |  중첩 반복문 내에서 부모의 loop 변수

<a name="conditional-classes"></a>
<!-- ### Conditional Classes -->
### Conditional Classes

<!-- The `@class` directive conditionally compiles a CSS class string. The directive accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`@class` 디렉티브는 CSS 클래스 문자열을 조건부로 렌더링할 수 있게 해줍니다. 이 디렉티브는 클래스명과 조건이 쌍으로 이루어진 배열을 받습니다. 배열의 키는 적용할 클래스명, 값은 불리언(참/거짓) 표현식입니다. 만약 배열 요소의 키가 숫자라면, 해당 클래스는 항상 렌더링 결과에 포함됩니다.

```
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

<a name="including-subviews"></a>
<!-- ### Including Subviews -->
### Including Subviews

> [!TIP]
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, 블레이드의 [components](#components)는 데이터 및 속성 바인딩처럼 `@include` 디렉티브에는 없는 여러 이점을 제공하는 비슷한 기능을 제공합니다.

<!-- Blade's `@include` directive allows you to include a Blade view from within another view. All variables that are available to the parent view will be made available to the included view: -->
블레이드의 `@include` 디렉티브를 사용하면 한 뷰 파일 내에서 다른 블레이드 뷰를 쉽게 포함할 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수는 포함된 뷰에서도 그대로 사용할 수 있습니다.

```html
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

<!-- Even though the included view will inherit all data available in the parent view, you may also pass an array of additional data that should be made available to the included view: -->
포함된 뷰가 부모 뷰의 모든 데이터를 상속받지만, 추가적으로 더 전달할 데이터가 있다면 배열로 넘길 수도 있습니다.

```
@include('view.name', ['status' => 'complete'])
```

<!-- If you attempt to `@include` a view which does not exist, Laravel will throw an error. If you would like to include a view that may or may not be present, you should use the `@includeIf` directive: -->
존재하지 않는 뷰를 `@include`하려 하면 Laravel은 오류를 발생시킵니다. 포함할 뷰가 없을 수도 있는 경우에는 `@includeIf` 디렉티브를 사용하면 됩니다.

```
@includeIf('view.name', ['status' => 'complete'])
```

<!-- If you would like to `@include` a view if a given boolean expression evaluates to `true` or `false`, you may use the `@includeWhen` and `@includeUnless` directives: -->
특정 불리언 표현식이 `true` 또는 `false`로 평가될 때 뷰를 `@include`하려면, `@includeWhen` 및 `@includeUnless` 디렉티브를 사용하세요.

```
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

<!-- To include the first view that exists from a given array of views, you may use the `includeFirst` directive: -->
여러 뷰 중 처음으로 존재하는 뷰를 포함하고 싶을 때는 `includeFirst` 디렉티브를 사용할 수 있습니다.

```
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!NOTE]
> 블레이드 뷰에서 `__DIR__`와 `__FILE__` 상수는 피해서 사용하시기 바랍니다. 해당 상수들은 캐시된 컴파일 뷰의 경로를 가리키게 됩니다.

<a name="rendering-views-for-collections"></a>
<!-- #### Rendering Views For Collections -->
#### Rendering Views For Collections

<!-- You may combine loops and includes into one line with Blade's `@each` directive: -->
반복문과 뷰 포함을 한 줄로 결합하고 싶을 때는 블레이드의 `@each` 디렉티브를 사용할 수 있습니다.

```
@each('view.name', $jobs, 'job')
```

<!-- The `@each` directive's first argument is the view to render for each element in the array or collection. The second argument is the array or collection you wish to iterate over, while the third argument is the variable name that will be assigned to the current iteration within the view. So, for example, if you are iterating over an array of `jobs`, typically you will want to access each job as a `job` variable within the view. The array key for the current iteration will be available as the `key` variable within the view. -->
`@each`의 첫 번째 인수는 반복마다 렌더링할 뷰 이름이고, 두 번째는 반복할 배열(또는 컬렉션) 값, 세 번째는 현재 반복 항목을 뷰 안에서 사용할 때 쓸 변수명입니다. 예를 들어, `jobs` 배열을 반복한다면 자식 뷰에서 각 job을 `job` 변수로 사용할 수 있습니다. 이때 현재 반복의 배열 키는 `key` 변수로도 활용할 수 있습니다.

<!-- You may also pass a fourth argument to the `@each` directive. This argument determines the view that will be rendered if the given array is empty. -->
네 번째 인수를 `@each`에 추가로 넘기면, 배열이 비어 있을 때 렌더링할 뷰를 지정할 수 있습니다.

```
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!NOTE]
> `@each`로 렌더링된 뷰는 부모 뷰의 변수를 상속받지 않습니다. 자식 뷰에서 부모의 변수가 필요하다면 `@foreach`와 `@include`를 사용하는 것이 좋습니다.

<a name="the-once-directive"></a>
<!-- ### The `@once` Directive -->
### The `@once` Directive

<!-- The `@once` directive allows you to define a portion of the template that will only be evaluated once per rendering cycle. This may be useful for pushing a given piece of JavaScript into the page's header using [stacks](#stacks). For example, if you are rendering a given [component](#components) within a loop, you may wish to only push the JavaScript to the header the first time the component is rendered: -->
`@once` 디렉티브는 해당 부분의 템플릿을 한 번만 평가하도록 해줍니다. 예를 들어 [stacks](#stacks)을 활용해 특정 자바스크립트 코드를 한 번만 헤더에 삽입하고 싶을 때 유용하게 사용할 수 있습니다. 루프 내에서 [component](#components)를 여러 번 렌더링해도 한 번만 자바스크립트 코드를 출력하고 싶을 때 아래와 같이 사용할 수 있습니다.

```
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

<a name="raw-php"></a>
<!-- ### Raw PHP -->
### Raw PHP

<!-- In some situations, it's useful to embed PHP code into your views. You can use the Blade `@php` directive to execute a block of plain PHP within your template: -->
특정 상황에서는 뷰에서 간단히 PHP 코드를 실행해야 할 수도 있습니다. 블레이드의 `@php` 디렉티브를 사용해 원하는 만큼의 PHP 코드를 직접 실행할 수 있습니다.

```
@php
    $counter = 1;
@endphp
```

<a name="comments"></a>
<!-- ### Comments -->
### Comments

<!-- Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application: -->
블레이드는 뷰에 주석을 남길 수 있도록 지원합니다. HTML 주석과 달리, 블레이드 주석은 애플리케이션이 반환하는 HTML 코드에 포함되지 않습니다.

```
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
<!-- ## Components -->
## Components

<!-- Components and slots provide similar benefits to sections, layouts, and includes; however, some may find the mental model of components and slots easier to understand. There are two approaches to writing components: class based components and anonymous components. -->
컴포넌트와 슬롯(Slot)은 섹션, 레이아웃, include와 비슷한 이점을 제공합니다. 다만, 어떤 분들에게는 컴포넌트와 슬롯 개념이 더 이해하기 쉬울 수 있습니다. 컴포넌트는 클래스 기반 방식과 익명 방식, 두 가지로 작성할 수 있습니다.

<!-- To create a class based component, you may use the `make:component` Artisan command. To illustrate how to use components, we will create a simple `Alert` component. The `make:component` command will place the component in the `app/View/Components` directory: -->
클래스 기반 컴포넌트를 만들려면, `make:component` Artisan 명령어를 사용하면 됩니다. 예시로 간단한 `Alert` 컴포넌트를 만들어 보겠습니다. `make:component` 명령어는 컴포넌트를 `app/View/Components` 디렉터리에 생성합니다.

```
php artisan make:component Alert
```

<!-- The `make:component` command will also create a view template for the component. The view will be placed in the `resources/views/components` directory. When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory, so no further component registration is typically required. -->
`make:component` 명령어는 컴포넌트의 뷰(템플릿) 파일도 함께 만들어줍니다. 해당 뷰는 `resources/views/components` 디렉터리에 위치합니다. 애플리케이션 내에서 컴포넌트를 만들 때, 별도의 등록 작업 없이 `app/View/Components`와 `resources/views/components` 디렉터리 내의 컴포넌트는 자동으로 인식됩니다.

<!-- You may also create components within subdirectories: -->
컴포넌트를 하위 디렉터리에 생성할 수도 있습니다.

```
php artisan make:component Forms/Input
```

<!-- The command above will create an `Input` component in the `app/View/Components/Forms` directory and the view will be placed in the `resources/views/components/forms` directory. -->
위 명령어로 `Input` 컴포넌트는 `app/View/Components/Forms` 디렉터리에, 뷰 파일은 `resources/views/components/forms` 디렉터리에 생성됩니다.

<a name="manually-registering-package-components"></a>

<!-- #### Manually Registering Package Components -->
#### Manually Registering Package Components

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
애플리케이션 자체에서 컴포넌트를 작성할 때는 `app/View/Components` 디렉터리와 `resources/views/components` 디렉터리에 있는 컴포넌트가 자동으로 인식됩니다.

<!-- However, if you are building a package that utilizes Blade components, you will need to manually register your component class and its HTML tag alias. You should typically register your components in the `boot` method of your package's service provider: -->
그러나 만약 Blade 컴포넌트를 사용하는 패키지를 개발한다면, 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지의 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다.

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot()
{
    Blade::component('package-alert', Alert::class);
}
```

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
컴포넌트가 등록된 후에는 아래와 같이 태그 별칭을 사용해 렌더링할 수 있습니다.

```
<x-package-alert/>
```

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
또는 `componentNamespace` 메서드를 사용해 컴포넌트 클래스를 관례적으로 자동 로딩할 수도 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 있고, 이들이 `Package\Views\Components` 네임스페이스에 위치한다고 가정해 봅시다.

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
이렇게 하면 패키지 컴포넌트를 벤더 네임스페이스로 `package-name::` 구문을 사용해 접근할 수 있습니다.

```
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 케이스로 변환하여 해당 컴포넌트와 연결된 클래스를 자동으로 찾습니다. 또한, "점" 표기법을 사용해 하위 디렉터리도 지원됩니다.

<a name="rendering-components"></a>
<!-- ### Rendering Components -->
### Rendering Components

<!-- To display a component, you may use a Blade component tag within one of your Blade templates. Blade component tags start with the string `x-` followed by the kebab case name of the component class: -->
컴포넌트를 표시하려면 Blade 템플릿 내에서 Blade 컴포넌트 태그를 사용하면 됩니다. Blade 컴포넌트 태그는 `x-`로 시작하고 그 뒤에 컴포넌트 클래스 이름을 케밥 케이스로 표기합니다.

```
<x-alert/>

<x-user-profile/>
```

<!-- If the component class is nested deeper within the `app/View/Components` directory, you may use the `.` character to indicate directory nesting. For example, if we assume a component is located at `app/View/Components/Inputs/Button.php`, we may render it like so: -->
컴포넌트 클래스가 `app/View/Components` 디렉터리 내 하위 디렉터리에 위치한다면, `.`(점) 문자를 사용해 디렉터리 구조를 나타낼 수 있습니다. 예를 들어 `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다면 다음과 같이 렌더링할 수 있습니다.

<!--     <x-inputs.button/> -->
    <x-inputs.button/>

<a name="passing-data-to-components"></a>
<!-- ### Passing Data To Components -->
### Passing Data To Components

<!-- You may pass data to Blade components using HTML attributes. Hard-coded, primitive values may be passed to the component using simple HTML attribute strings. PHP expressions and variables should be passed to the component via attributes that use the `:` character as a prefix: -->
Blade 컴포넌트에 데이터를 전달하려면 HTML 속성을 사용할 수 있습니다. 하드코딩된 원시 값은 일반적인 HTML 속성 문자열로 전달합니다. PHP 표현식이나 변수는 속성 앞에 콜론(`:`)을 붙여서 전달해야 합니다.

```
<x-alert type="error" :message="$message"/>
```

<!-- You should define the component's required data in its class constructor. All public properties on a component will automatically be made available to the component's view. It is not necessary to pass the data to the view from the component's `render` method: -->
컴포넌트에 필요한 데이터는 컴포넌트 클래스의 생성자에서 정의합니다. 컴포넌트의 모든 public 속성은 자동으로 컴포넌트 뷰에서 사용할 수 있게 됩니다. 따라서 `render` 메서드에서 별도로 데이터를 뷰에 전달할 필요는 없습니다.

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The alert type.
     *
     * @var string
     */
    public $type;

    /**
     * The alert message.
     *
     * @var string
     */
    public $message;

    /**
     * Create the component instance.
     *
     * @param  string  $type
     * @param  string  $message
     * @return void
     */
    public function __construct($type, $message)
    {
        $this->type = $type;
        $this->message = $message;
    }

    /**
     * Get the view / contents that represent the component.
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return view('components.alert');
    }
}
```

<!-- When your component is rendered, you may display the contents of your component's public variables by echoing the variables by name: -->
컴포넌트가 렌더링될 때, 컴포넌트의 public 변수 값은 변수명을 이용해 출력할 수 있습니다.

```html
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
<!-- #### Casing -->
#### Casing

<!-- Component constructor arguments should be specified using `camelCase`, while `kebab-case` should be used when referencing the argument names in your HTML attributes. For example, given the following component constructor: -->
컴포넌트 생성자 인수는 `camelCase`로 지정해야 하고, HTML 속성을 이용해 인수 이름을 참조할 때는 `kebab-case`를 사용해야 합니다. 예를 들어 다음과 같은 컴포넌트 생성자가 있다면

```
/**
 * Create the component instance.
 *
 * @param  string  $alertType
 * @return void
 */
public function __construct($alertType)
{
    $this->alertType = $alertType;
}
```

<!-- The `$alertType` argument may be provided to the component like so: -->
`$alertType` 인수는 아래와 같이 컴포넌트에 제공할 수 있습니다.

```
<x-alert alert-type="danger" />
```

<a name="escaping-attribute-rendering"></a>
<!-- #### Escaping Attribute Rendering -->
#### Escaping Attribute Rendering

<!-- Since some JavaScript frameworks such as Alpine.js also use colon-prefixed attributes, you may use a double colon (`::`) prefix to inform Blade that the attribute is not a PHP expression. For example, given the following component: -->
Alpine.js와 같이 콜론 접두사를 속성에 사용하는 자바스크립트 프레임워크들이 있기 때문에, Blade가 해당 속성을 PHP 표현식으로 인식하지 않도록 하려면 더블 콜론(`::`)을 접두어로 사용합니다. 예를 들어 아래와 같은 컴포넌트가 있을 때,

```
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

<!-- The following HTML will be rendered by Blade: -->
Blade가 렌더링한 HTML은 다음과 같습니다.

```
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
<!-- #### Component Methods -->
#### Component Methods

<!-- In addition to public variables being available to your component template, any public methods on the component may be invoked. For example, imagine a component that has an `isSelected` method: -->
컴포넌트 템플릿에서는 public 변수를 사용할 수 있는 것뿐만 아니라, public 메서드도 호출할 수 있습니다. 예를 들어, 컴포넌트에 `isSelected`라는 메서드가 있다고 가정해 봅니다.

```
/**
 * Determine if the given option is the currently selected option.
 *
 * @param  string  $option
 * @return bool
 */
public function isSelected($option)
{
    return $option === $this->selected;
}
```

<!-- You may execute this method from your component template by invoking the variable matching the name of the method: -->
아래와 같이 메서드명과 같은 이름의 변수를 호출해 이 메서드를 컴포넌트 템플릿에서 사용할 수 있습니다.

```
<option {{ $isSelected($value) ? 'selected="selected"' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
<!-- #### Accessing Attributes & Slots Within Component Classes -->
#### Accessing Attributes & Slots Within Component Classes

<!-- Blade components also allow you to access the component name, attributes, and slot inside the class's render method. However, in order to access this data, you should return a closure from your component's `render` method. The closure will receive a `$data` array as its only argument. This array will contain several elements that provide information about the component: -->
Blade 컴포넌트는 클래스의 render 메서드 안에서 컴포넌트 이름, 속성, 슬롯 등에 접근할 수 있습니다. 이 때는 `render` 메서드에서 클로저를 반환해야 합니다. 이 클로저는 `$data` 배열을 인자로 받는데, 이 배열에는 컴포넌트에 대한 다양한 정보가 들어 있습니다.

```
/**
 * Get the view / contents that represent the component.
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
{
    return function (array $data) {
        // $data['componentName'];
        // $data['attributes'];
        // $data['slot'];

        return '<div>Components content</div>';
    };
}
```

<!-- The `componentName` is equal to the name used in the HTML tag after the `x-` prefix. So `<x-alert />`'s `componentName` will be `alert`. The `attributes` element will contain all of the attributes that were present on the HTML tag. The `slot` element is an `Illuminate\Support\HtmlString` instance with the contents of the component's slot. -->
`componentName` 값은 `x-` 접두어 이후 HTML 태그에 사용된 이름과 같습니다. 예를 들어 `<x-alert />`의 `componentName` 값은 `alert`이 됩니다. `attributes` 요소에는 해당 태그에 지정된 모든 속성이, `slot` 요소에는 슬롯의 내용이 `Illuminate\Support\HtmlString` 인스턴스로 담겨 있습니다.

<!-- The closure should return a string. If the returned string corresponds to an existing view, that view will be rendered; otherwise, the returned string will be evaluated as an inline Blade view. -->
이 클로저는 문자열을 반환해야 하며, 만약 이 문자열이 실제로 존재하는 Blade 뷰라면 해당 뷰가 렌더링됩니다. 만약 존재하지 않으면, 반환된 문자열이 인라인 Blade 뷰로 해석되어 렌더링됩니다.

<a name="additional-dependencies"></a>
<!-- #### Additional Dependencies -->
#### Additional Dependencies

<!-- If your component requires dependencies from Laravel's [service container](/docs/8.x/container), you may list them before any of the component's data attributes and they will automatically be injected by the container: -->
컴포넌트에서 Laravel의 [service container](/docs/8.x/container)에서 의존성을 주입받을 필요가 있을 경우, 컴포넌트의 데이터 속성들 앞에 의존성을 나열하면 컨테이너가 자동으로 주입해줍니다.

```
use App\Services\AlertCreator

/**
 * Create the component instance.
 *
 * @param  \App\Services\AlertCreator  $creator
 * @param  string  $type
 * @param  string  $message
 * @return void
 */
public function __construct(AlertCreator $creator, $type, $message)
{
    $this->creator = $creator;
    $this->type = $type;
    $this->message = $message;
}
```

<a name="hiding-attributes-and-methods"></a>
<!-- #### Hiding Attributes / Methods -->
#### Hiding Attributes / Methods

<!-- If you would like to prevent some public methods or properties from being exposed as variables to your component template, you may add them to an `$except` array property on your component: -->
컴포넌트 템플릿에 노출시키고 싶지 않은 public 메서드나 속성이 있다면, 해당 속성이나 메서드의 이름을 `$except` 배열 속성에 추가하면 됩니다.

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The alert type.
     *
     * @var string
     */
    public $type;

    /**
     * The properties / methods that should not be exposed to the component template.
     *
     * @var array
     */
    protected $except = ['type'];
}
```

<a name="component-attributes"></a>
<!-- ### Component Attributes -->
### Component Attributes

<!-- We've already examined how to pass data attributes to a component; however, sometimes you may need to specify additional HTML attributes, such as `class`, that are not part of the data required for a component to function. Typically, you want to pass these additional attributes down to the root element of the component template. For example, imagine we want to render an `alert` component like so: -->
이전에 컴포넌트에 데이터 속성을 전달하는 방법을 살펴보았습니다. 그러나 컴포넌트의 기능상 꼭 필요하지 않지만, 추가적인 HTML 속성(예: `class`)을 지정해야 하는 경우도 있습니다. 주로 이런 추가 속성들은 컴포넌트 템플릿의 루트 엘리먼트에 내려주고 싶을 때가 많습니다. 예를 들어 아래처럼 `alert` 컴포넌트를 렌더링하고 싶다고 가정해보겠습니다.

```
<x-alert type="error" :message="$message" class="mt-4"/>
```

<!-- All of the attributes that are not part of the component's constructor will automatically be added to the component's "attribute bag". This attribute bag is automatically made available to the component via the `$attributes` variable. All of the attributes may be rendered within the component by echoing this variable: -->
컴포넌트 생성자에 정의되지 않은 모든 속성은 자동으로 컴포넌트의 "속성 백(attribute bag)"에 들어갑니다. 이 속성 백은 `$attributes` 변수로 컴포넌트에 자동 제공됩니다. 컴포넌트에서는 이 변수를 출력함으로써 모든 속성을 렌더링할 수 있습니다.

```
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!NOTE]
> 현재 컴포넌트 태그에서 `@env` 같은 디렉티브를 사용하는 것은 지원되지 않습니다. 예를 들어 `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
<!-- #### Default / Merged Attributes -->
#### Default / Merged Attributes

<!-- Sometimes you may need to specify default values for attributes or merge additional values into some of the component's attributes. To accomplish this, you may use the attribute bag's `merge` method. This method is particularly useful for defining a set of default CSS classes that should always be applied to a component: -->
속성의 기본값을 지정하거나, 특정 속성에 추가적인 값을 병합해야 할 때가 있습니다. 이럴 때는 속성 백의 `merge` 메서드를 사용할 수 있습니다. 이 메서드는 컴포넌트에 항상 적용되어야 하는 기본 CSS 클래스를 정의할 때 특히 유용합니다.

```
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- If we assume this component is utilized like so: -->
이 컴포넌트를 다음처럼 사용한다고 가정해봅니다.

```
<x-alert type="error" :message="$message" class="mb-4"/>
```

<!-- The final, rendered HTML of the component will appear like the following: -->
최종적으로 렌더링되는 컴포넌트의 HTML은 아래와 같이 나옵니다.

```html
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
<!-- #### Conditionally Merge Classes -->
#### Conditionally Merge Classes

<!-- Sometimes you may wish to merge classes if a given condition is `true`. You can accomplish this via the `class` method, which accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
특정 조건이 `true`일 때만 클래스를 병합하고 싶을 때가 있습니다. `class` 메서드를 사용하면 배열을 넘겨서, 배열 키가 추가할 클래스(또는 여러 클래스), 값이 해당 클래스의 추가 여부를 결정할 불리언 표현식이 됩니다. 배열의 키가 숫자일 경우, 이 클래스는 항상 렌더링에 포함됩니다.

```
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

<!-- If you need to merge other attributes onto your component, you can chain the `merge` method onto the `class` method: -->
만약 다른 속성도 함께 병합하고 싶다면, `class` 메서드 뒤에 `merge` 메서드를 체이닝해서 사용할 수 있습니다.

```
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!TIP]
> 병합된 속성을 받지 않아야 하는 다른 HTML 엘리먼트에서 조건부 클래스를 컴파일하려면, [`@class` directive](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
<!-- #### Non-Class Attribute Merging -->
#### Non-Class Attribute Merging

<!-- When merging attributes that are not `class` attributes, the values provided to the `merge` method will be considered the "default" values of the attribute. However, unlike the `class` attribute, these attributes will not be merged with injected attribute values. Instead, they will be overwritten. For example, a `button` component's implementation may look like the following: -->
`class` 외의 다른 속성을 병합할 때, `merge` 메서드에 넘겨진 값은 해당 속성의 "기본값"으로 간주됩니다. 그러나 `class` 속성과 달리, 이 속성들은 삽입된 속성 값과 병합되지 않고, 삽입 값이 있다면 기본값 대신 덮어써집니다. 예를 들어, 아래와 같은 `button` 컴포넌트를 구현했다고 가정해봅시다.

```
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

<!-- To render the button component with a custom `type`, it may be specified when consuming the component. If no type is specified, the `button` type will be used: -->
버튼 컴포넌트를 사용할 때 `type`을 지정하려면, 아래처럼 사용할 수 있습니다. 만약 타입을 지정하지 않으면 기본값인 `button`이 사용됩니다.

```
<x-button type="submit">
    Submit
</x-button>
```

<!-- The rendered HTML of the `button` component in this example would be: -->
이 예시에서 `button` 컴포넌트가 렌더링하는 HTML은 다음과 같습니다.

```
<button type="submit">
    Submit
</button>
```

<!-- If you would like an attribute other than `class` to have its default value and injected values joined together, you may use the `prepends` method. In this example, the `data-controller` attribute will always begin with `profile-controller` and any additional injected `data-controller` values will be placed after this default value: -->
`class`가 아닌 속성에서도 기본값과 주입된 값을 모두 합치고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래 예제에서는 `data-controller` 속성이 항상 `profile-controller`로 시작되고, 추가로 주입된 `data-controller` 값이 뒤에 붙습니다.

```
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
<!-- #### Retrieving & Filtering Attributes -->
#### Retrieving & Filtering Attributes

<!-- You may filter attributes using the `filter` method. This method accepts a closure which should return `true` if you wish to retain the attribute in the attribute bag: -->
`filter` 메서드를 이용해 속성을 필터링할 수 있습니다. 이 메서드는 클로저를 인자로 받아, 클로저가 `true`를 반환하는 경우만 속성이 남게 됩니다.

```
{{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}
```

<!-- For convenience, you may use the `whereStartsWith` method to retrieve all attributes whose keys begin with a given string: -->
편의를 위해, `whereStartsWith` 메서드를 사용하면 키가 특정 문자열로 시작하는 모든 속성을 한 번에 가져올 수 있습니다.

```
{{ $attributes->whereStartsWith('wire:model') }}
```

<!-- Conversely, the `whereDoesntStartWith` method may be used to exclude all attributes whose keys begin with a given string: -->
반대로, `whereDoesntStartWith` 메서드를 이용하면 특정 문자열로 시작하는 모든 속성을 제외할 수 있습니다.

```
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

<!-- Using the `first` method, you may render the first attribute in a given attribute bag: -->
`first` 메서드를 사용하면, 속성 백에서 첫 번째 속성만 렌더링할 수 있습니다.

```
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

<!-- If you would like to check if an attribute is present on the component, you may use the `has` method. This method accepts the attribute name as its only argument and returns a boolean indicating whether or not the attribute is present: -->
컴포넌트에 특정 속성이 존재하는지 확인하고 싶다면, `has` 메서드를 이용합니다. 인자로 속성 이름만 전달하면, 해당 속성이 존재하는지 아닌지 불리언으로 반환합니다.

```
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

<!-- You may retrieve a specific attribute's value using the `get` method: -->
특정 속성의 값을 가져오려면 `get` 메서드를 사용합니다.

```
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
<!-- ### Reserved Keywords -->
### Reserved Keywords

<!-- By default, some keywords are reserved for Blade's internal use in order to render components. The following keywords cannot be defined as public properties or method names within your components: -->
기본적으로, Blade가 내부적으로 컴포넌트를 렌더링할 때 사용하기 위해 몇 가지 예약어를 정의하고 있습니다. 아래에 나열된 예약어는 컴포넌트 내 public 속성이나 메서드 이름으로 사용할 수 없습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`
-->
- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<!-- </div> -->
</div>

<a name="slots"></a>
<!-- ### Slots -->
### Slots

<!-- You will often need to pass additional content to your component via "slots". Component slots are rendered by echoing the `$slot` variable. To explore this concept, let's imagine that an `alert` component has the following markup: -->
컴포넌트에 "슬롯"을 통해 추가적인 콘텐츠를 전달할 필요가 있을 때가 많습니다. 컴포넌트 슬롯은 `$slot` 변수를 출력함으로써 렌더링됩니다. 개념을 살펴보기 위해, 다음과 같이 `alert` 컴포넌트의 마크업이 있다고 가정합시다.

```html
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- We may pass content to the `slot` by injecting content into the component: -->
이제 컴포넌트에 콘텐츠를 주입하여 `slot`에 값이 전달되도록 할 수 있습니다.

```html
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- Sometimes a component may need to render multiple different slots in different locations within the component. Let's modify our alert component to allow for the injection of a "title" slot: -->
컴포넌트 안에서 여러 위치에 다양한 슬롯을 전달해야 할 경우도 있습니다. 예를 들어 "title" 슬롯을 추가로 주입할 수 있도록 alert 컴포넌트를 수정해보겠습니다.

```html
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- You may define the content of the named slot using the `x-slot` tag. Any content not within an explicit `x-slot` tag will be passed to the component in the `$slot` variable: -->
명명된 슬롯의 내용을 정의하려면 `x-slot` 태그를 사용하면 됩니다. 명시적으로 `x-slot` 태그 내에 있지 않은 모든 내용은 기본적으로 `$slot` 변수에 전달됩니다.

```html
<x-alert>
    <x-slot name="title">
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="scoped-slots"></a>
<!-- #### Scoped Slots -->
#### Scoped Slots

<!-- If you have used a JavaScript framework such as Vue, you may be familiar with "scoped slots", which allow you to access data or methods from the component within your slot. You may achieve similar behavior in Laravel by defining public methods or properties on your component and accessing the component within your slot via the `$component` variable. In this example, we will assume that the `x-alert` component has a public `formatAlert` method defined on its component class: -->
Vue 등의 자바스크립트 프레임워크를 사용해 본 적이 있다면, 컴포넌트의 데이터나 메서드에 접근할 수 있는 "스코프 슬롯"에 익숙할 수 있습니다. Laravel에서도 컴포넌트의 public 메서드 또는 속성을 정의하고, 슬롯 내부에서 `$component` 변수로 컴포넌트에 접근함으로써 유사한 동작을 구현할 수 있습니다. 아래 예제에서는 `x-alert` 컴포넌트 클래스에 `formatAlert`라는 public 메서드가 정의되어 있다고 가정해 봅니다.

```html
<x-alert>
    <x-slot name="title">
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
<!-- #### Slot Attributes -->
#### Slot Attributes

<!-- Like Blade components, you may assign additional [attributes](#component-attributes) to slots such as CSS class names: -->
Blade 컴포넌트와 마찬가지로, CSS 클래스명과 같은 [attributes](#component-attributes)을 슬롯에 적용할 수 있습니다.

```html
<x-card class="shadow-sm">
    <x-slot name="heading" class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot name="footer" class="text-sm">
        Footer
    </x-slot>
</x-card>
```

<!-- To interact with slot attributes, you may access the `attributes` property of the slot's variable. For more information on how to interact with attributes, please consult the documentation on [component attributes](#component-attributes): -->
슬롯의 속성과 상호작용하려면, 슬롯 변수의 `attributes` 속성에 접근하면 됩니다. 속성에 어떻게 접근하는지에 대한 자세한 내용은 [component attributes](#component-attributes) 문서를 참고하세요.

```php
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
매우 간단한 컴포넌트의 경우 컴포넌트 클래스와 뷰 템플릿 파일을 따로 관리하는 것이 번거롭게 느껴질 수 있습니다. 이럴 때는 컴포넌트의 `render` 메서드에서 마크업을 직접 반환할 수 있습니다.

```
/**
 * Get the view / contents that represent the component.
 *
 * @return \Illuminate\View\View|\Closure|string
 */
public function render()
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
인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령어 실행 시 `inline` 옵션을 사용할 수 있습니다.

```
php artisan make:component Alert --inline
```

<a name="anonymous-components"></a>
<!-- ### Anonymous Components -->
### Anonymous Components

<!-- Similar to inline components, anonymous components provide a mechanism for managing a component via a single file. However, anonymous components utilize a single view file and have no associated class. To define an anonymous component, you only need to place a Blade template within your `resources/views/components` directory. For example, assuming you have defined a component at `resources/views/components/alert.blade.php`, you may simply render it like so: -->
인라인 컴포넌트와 유사하게, 익명(anonymous) 컴포넌트는 하나의 파일만으로 컴포넌트를 관리할 수 있는 방식을 제공합니다. 하지만 익명 컴포넌트는 하나의 뷰 파일만을 사용하며 별도의 클래스가 없습니다. 익명 컴포넌트를 정의하려면 단순히 Blade 템플릿을 `resources/views/components` 디렉터리에 추가하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 정의했다면, 다음과 같이 간단히 렌더링할 수 있습니다.

```
<x-alert/>
```

<!-- You may use the `.` character to indicate if a component is nested deeper inside the `components` directory. For example, assuming the component is defined at `resources/views/components/inputs/button.blade.php`, you may render it like so: -->
컴포넌트가 `components` 디렉터리 내에 더 깊이 중첩되어 있는 경우에는 `.`(점) 문자를 사용할 수 있습니다. 예를 들어, 컴포넌트가 `resources/views/components/inputs/button.blade.php`에 정의되어 있다면, 아래와 같이 렌더링할 수 있습니다.

<!--     <x-inputs.button/> -->
    <x-inputs.button/>

<a name="anonymous-index-components"></a>
<!-- #### Anonymous Index Components -->
#### Anonymous Index Components

<!-- Sometimes, when a component is made up of many Blade templates, you may wish to group the given component's templates within a single directory. For example, imagine an "accordion" component with the following directory structure: -->
때때로, 컴포넌트가 여러 Blade 템플릿으로 구성되어 있다면 하나의 디렉터리 안에 해당 컴포넌트의 템플릿들을 그룹화하고 싶을 수 있습니다. 예를 들어, "아코디언(accordion)" 컴포넌트가 아래와 같은 디렉터리 구조를 가진다고 가정해봅시다.

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<!-- This directory structure allows you to render the accordion component and its item like so: -->
이 구조를 사용하면 다음과 같이 아코디언 컴포넌트 및 아이템을 렌더링할 수 있습니다.

```html
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

<!-- However, in order to render the accordion component via `x-accordion`, we were forced to place the "index" accordion component template in the `resources/views/components` directory instead of nesting it within the `accordion` directory with the other accordion related templates. -->
하지만 위와 같이 `x-accordion`으로 아코디언 컴포넌트를 렌더링하려면, "index" 역할의 아코디언 컴포넌트 템플릿을 관련된 다른 템플릿들과 함께 `accordion` 디렉터리가 아닌, `resources/views/components` 디렉터리에 두어야만 했습니다.

<!-- Thankfully, Blade allows you to place an `index.blade.php` file within a component's template directory. When an `index.blade.php` template exists for the component, it will be rendered as the "root" node of the component. So, we can continue to use the same Blade syntax given in the example above; however, we will adjust our directory structure like so: -->
다행히도, Blade에서는 컴포넌트의 템플릿 디렉터리에 `index.blade.php` 파일을 둘 수 있습니다. 컴포넌트에 해당 `index.blade.php` 템플릿이 있으면, 컴포넌트의 "루트" 노드로서 렌더링됩니다. 즉, 앞서 보여준 Blade 문법을 그대로 사용할 수 있으면서, 디렉터리 구조는 아래처럼 정리할 수 있습니다.

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
<!-- #### Data Properties / Attributes -->
#### Data Properties / Attributes

<!-- Since anonymous components do not have any associated class, you may wonder how you may differentiate which data should be passed to the component as variables and which attributes should be placed in the component's [attribute bag](#component-attributes). -->
익명 컴포넌트에는 연결된 클래스가 없기 때문에, 어떤 데이터를 컴포넌트의 변수로 전달하고, 어떤 속성을 [attribute bag](#component-attributes)에 넣어야 할지 궁금할 수 있습니다.

<!-- You may specify which attributes should be considered data variables using the `@props` directive at the top of your component's Blade template. All other attributes on the component will be available via the component's attribute bag. If you wish to give a data variable a default value, you may specify the variable's name as the array key and the default value as the array value: -->
컴포넌트의 Blade 템플릿 맨 위에 `@props` 디렉티브를 사용하여 데이터 변수로 취급할 속성을 명시할 수 있습니다. 이외의 나머지 속성들은 모두 컴포넌트의 속성 가방에서 사용할 수 있습니다. 특정 데이터 변수에 기본값을 주고 싶다면 변수 이름을 배열의 키로, 기본값을 값으로 지정하면 됩니다.

```
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- Given the component definition above, we may render the component like so: -->
위와 같이 컴포넌트를 정의했다면, 아래와 같이 컴포넌트를 렌더링할 수 있습니다.

```
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
<!-- #### Accessing Parent Data -->
#### Accessing Parent Data

<!-- Sometimes you may want to access data from a parent component inside a child component. In these cases, you may use the `@aware` directive. For example, imagine we are building a complex menu component consisting of a parent `<x-menu>` and child `<x-menu.item>`: -->
때때로 자식 컴포넌트에서 부모 컴포넌트의 데이터를 사용하고 싶을 때가 있습니다. 이럴 때는 `@aware` 디렉티브를 사용할 수 있습니다. 예를 들어, 부모 `<x-menu>`와 자식 `<x-menu.item>`로 이루어진 복잡한 메뉴 컴포넌트를 만든다고 가정해봅시다.

```
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

<!-- The `<x-menu>` component may have an implementation like the following: -->
`<x-menu>` 컴포넌트는 아래와 같이 구현할 수 있습니다.

```
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

<!-- Because the `color` prop was only passed into the parent (`<x-menu>`), it won't be available inside `<x-menu.item>`. However, if we use the `@aware` directive, we can make it available inside `<x-menu.item>` as well: -->
`color` 속성이 부모(`<x-menu>`)에만 전달되었으므로, 기본적으로 `<x-menu.item>` 내부에서는 사용할 수 없습니다. 하지만, `@aware` 디렉티브를 사용하면 `<x-menu.item>` 내부에서도 해당 값을 사용할 수 있습니다.

```
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

<a name="dynamic-components"></a>
<!-- ### Dynamic Components -->
### Dynamic Components

<!-- Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable: -->
어떤 컴포넌트를 렌더링할지는 런타임 값에 따라 결정되어야 할 때가 있습니다. 이런 상황에서는 Laravel에 내장된 `dynamic-component` 컴포넌트를 활용해 런타임 값이나 변수에 따라 컴포넌트를 렌더링할 수 있습니다.

```
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
<!-- ### Manually Registering Components -->
### Manually Registering Components

> [!NOTE]
> 아래 문서의 컴포넌트 수동 등록 내용은 주로 뷰 컴포넌트를 포함하는 Laravel 패키지를 작성하는 사용자에게 유용합니다. 패키지를 작성하지 않는 경우, 이 부분은 필요하지 않을 수 있습니다.

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
자신의 애플리케이션에서 컴포넌트를 작성할 때는, `app/View/Components` 디렉터리와 `resources/views/components` 디렉터리에 있는 컴포넌트들이 자동으로 인식됩니다.

<!-- However, if you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider: -->
하지만, Blade 컴포넌트를 활용하는 패키지 개발 시나, 비표준(일반적이지 않은) 디렉터리에 컴포넌트를 둘 경우에는, Laravel이 해당 컴포넌트의 클래스를 찾을 수 있도록 컴포넌트 클래스와 HTML 태그 별칭(alias)을 직접 등록해야 합니다. 보통은 패키지의 서비스 프로바이더 `boot` 메서드에서 등록하게 됩니다.

```
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 *
 * @return void
 */
public function boot()
{
    Blade::component('package-alert', AlertComponent::class);
}
```

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
컴포넌트가 등록되고 나면, 태그 별칭(alias)을 사용해 다음과 같이 렌더링할 수 있습니다.

```
<x-package-alert/>
```

<!-- #### Autoloading Package Components -->
#### Autoloading Package Components

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
또는, `componentNamespace` 메서드를 사용해 컴포넌트 클래스를 컨벤션에 따라 자동으로 로드할 수도 있습니다. 예를 들어, `Nightshade`라는 패키지에 `Calendar`와 `ColorPicker` 컴포넌트가 있고, 이들이 `Package\Views\Components` 네임스페이스에 위치한다고 가정하면:

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 *
 * @return void
 */
public function boot()
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
위와 같이 등록해 주면, `package-name::` 형태의 벤더 네임스페이스로 패키지 컴포넌트를 사용할 수 있습니다.

```
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 표기법(PascalCase)으로 변환해 자동으로 관련된 클래스를 찾습니다. 하위 디렉터리 구조 역시 "점" 표기법(dot notation)으로 지원됩니다.

<a name="building-layouts"></a>
<!-- ## Building Layouts -->
## Building Layouts

<a name="layouts-using-components"></a>
<!-- ### Layouts Using Components -->
### Layouts Using Components

<!-- Most web applications maintain the same general layout across various pages. It would be incredibly cumbersome and hard to maintain our application if we had to repeat the entire layout HTML in every view we create. Thankfully, it's convenient to define this layout as a single [Blade component](#components) and then use it throughout our application. -->
대부분의 웹 애플리케이션은 여러 페이지에서 동일한 레이아웃 구조를 유지합니다. 만약 각 뷰마다 전체 레이아웃 HTML을 반복해서 작성해야 한다면 매우 번거롭고, 유지보수도 어렵게 됩니다. 다행히도, 이 레이아웃을 하나의 [Blade component](#components)로 정의해서 애플리케이션 전반에 걸쳐 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
<!-- #### Defining The Layout Component -->
#### Defining The Layout Component

<!-- For example, imagine we are building a "todo" list application. We might define a `layout` component that looks like the following: -->
예를 들어, "할 일(todo) 목록" 애플리케이션을 만든다고 가정합시다. 다음과 같은 `layout` 컴포넌트를 만들 수 있습니다.

```html
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
<!-- #### Applying The Layout Component -->
#### Applying The Layout Component

<!-- Once the `layout` component has been defined, we may create a Blade view that utilizes the component. In this example, we will define a simple view that displays our task list: -->
`layout` 컴포넌트를 정의한 후, 해당 컴포넌트를 사용하는 Blade 뷰를 만들 수 있습니다. 예제로, 아래와 같이 할 일 목록을 출력하는 간단한 뷰를 정의해 보겠습니다.

```html
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

<!-- Remember, content that is injected into a component will be supplied to the default `$slot` variable within our `layout` component. As you may have noticed, our `layout` also respects a `$title` slot if one is provided; otherwise, a default title is shown. We may inject a custom title from our task list view using the standard slot syntax discussed in the [component documentation](#components): -->
컴포넌트에 전달된 내부 콘텐츠는 `layout` 컴포넌트 내에서 기본적으로 `$slot` 변수로 전달됩니다. 또한, 위 `layout` 컴포넌트는 `$title` 슬롯이 제공될 경우 이를 사용하고, 제공되지 않으면 기본값을 표시하도록 되어 있습니다. [component documentation](#components)에서 소개한 표준 슬롯 문법을 사용해, 아래와 같이 커스텀 제목을 주입할 수 있습니다.

```html
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot name="title">
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

<!-- Now that we have defined our layout and task list views, we just need to return the `task` view from a route: -->
레이아웃과 할 일 목록 뷰를 정의했다면, 이제 단순히 라우트에서 `task` 뷰를 반환하면 됩니다.

```
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
<!-- ### Layouts Using Template Inheritance -->
### Layouts Using Template Inheritance

<a name="defining-a-layout"></a>
<!-- #### Defining A Layout -->
#### Defining A Layout

<!-- Layouts may also be created via "template inheritance". This was the primary way of building applications prior to the introduction of [components](#components). -->
레이아웃은 "템플릿 상속" 기능을 통해서도 만들 수 있습니다. 이 방식은 [components](#components)가 도입되기 전, 애플리케이션을 구성하는 주된 방법이었습니다.

<!-- To get started, let's take a look at a simple example. First, we will examine a page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view: -->
먼저, 간단한 예제를 살펴보겠습니다. 다음은 페이지 전체 레이아웃입니다. 일반적으로 여러 페이지에서 동일한 구조를 유지하기 때문에, 한 개의 Blade 뷰로 레이아웃을 정의하는 것이 편리합니다.

```html
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
이 파일에는 일반적인 HTML 마크업이 들어 있습니다. 하지만, `@section`과 `@yield` Blade 디렉티브에 주목해야 합니다. `@section` 디렉티브는 이름처럼 특정 콘텐츠 영역을 정의하며, `@yield` 디렉티브는 해당 영역의 내용을 출력하는 데 사용됩니다.

<!-- Now that we have defined a layout for our application, let's define a child page that inherits the layout. -->
이제 애플리케이션의 레이아웃이 정의되었으니, 이 레이아웃을 상속받는 자식 페이지를 만들어 보겠습니다.

<a name="extending-a-layout"></a>
<!-- #### Extending A Layout -->
#### Extending A Layout

<!-- When defining a child view, use the `@extends` Blade directive to specify which layout the child view should "inherit". Views which extend a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`: -->
자식 뷰를 정의할 때는, 어떤 레이아웃을 상속받을 것인지 `@extends` Blade 디렉티브로 명시해야 합니다. 레이아웃을 상속받는 뷰에서는 `@section` 디렉티브를 사용해 레이아웃의 각 영역에 콘텐츠를 주입할 수 있습니다. 상기 예제에서처럼, 이 영역의 내용들은 레이아웃 내 `@yield`를 통해 표시됩니다.

```html
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
여기서 `sidebar` 영역은 `@@parent` 디렉티브를 사용해, 레이아웃의 사이드바 내용에 새로운 콘텐츠를 덧붙이는 방식으로 동작합니다. `@@parent`는 뷰가 렌더링될 때 레이아웃의 기본 내용을 해당 위치에 삽입합니다.

> [!TIP]
> 앞선 예제와 달리, 이번 `sidebar` 영역은 `@show`가 아닌 `@endsection`으로 끝납니다. `@endsection`은 단순히 영역을 정의만 하고, `@show`는 정의와 동시에 해당 영역을 **즉시 출력**합니다.

<!-- The `@yield` directive also accepts a default value as its second parameter. This value will be rendered if the section being yielded is undefined: -->
`@yield` 디렉티브는 두 번째 인자로 기본값을 받을 수도 있습니다. 만약 해당 영역이 정의되지 않은 경우에는 이 값이 출력됩니다.

```
@yield('content', 'Default content')
```

<a name="forms"></a>
<!-- ## Forms -->
## Forms

<a name="csrf-field"></a>
<!-- ### CSRF Field -->
### CSRF Field

<!-- Anytime you define an HTML form in your application, you should include a hidden CSRF token field in the form so that [the CSRF protection](/docs/8.x/csrf) middleware can validate the request. You may use the `@csrf` Blade directive to generate the token field: -->
애플리케이션에서 HTML 폼을 정의할 때는, [the CSRF protection](/docs/8.x/csrf) 미들웨어가 요청을 검증할 수 있도록 폼 내에 숨겨진 CSRF 토큰 필드를 항상 포함해야 합니다. `@csrf` Blade 디렉티브를 사용해서 이 토큰 필드를 생성할 수 있습니다.

```html
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
<!-- ### Method Field -->
### Method Field

<!-- Since HTML forms can't make `PUT`, `PATCH`, or `DELETE` requests, you will need to add a hidden `_method` field to spoof these HTTP verbs. The `@method` Blade directive can create this field for you: -->
HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 보낼 수 없기 때문에, 이러한 HTTP 동사를 흉내내기 위해 숨겨진 `_method` 필드를 추가해야 합니다. Blade의 `@method` 디렉티브로 이 필드를 생성할 수 있습니다.

```html
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
<!-- ### Validation Errors -->
### Validation Errors

<!-- The `@error` directive may be used to quickly check if [validation error messages](/docs/8.x/validation#quick-displaying-the-validation-errors) exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
`@error` 디렉티브는 [validation error messages](/docs/8.x/validation#quick-displaying-the-validation-errors)가 특정 속성에 대해 존재하는지 빠르게 확인할 수 있습니다. `@error` 블록 내부에서는 `$message` 변수를 바로 출력해 에러 메시지를 표시할 수 있습니다.

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title" type="text" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- Since the `@error` directive compiles to an "if" statement, you may use the `@else` directive to render content when there is not an error for an attribute: -->
`@error` 디렉티브는 실제로 "if" 문으로 컴파일되므로, 에러가 없을 때 콘텐츠를 렌더링하려면 `@else` 디렉티브를 함께 사용할 수도 있습니다.

```html
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email" type="email" class="@error('email') is-invalid @else is-valid @enderror">
```

<!-- You may pass [the name of a specific error bag](/docs/8.x/validation#named-error-bags) as the second parameter to the `@error` directive to retrieve validation error messages on pages containing multiple forms: -->
여러 개의 폼이 있는 페이지에서 [the name of a specific error bag](/docs/8.x/validation#named-error-bags)을 `@error` 디렉티브의 두 번째 인자로 전달해, 해당 이름을 가진 에러 메시지를 얻을 수도 있습니다.

```html
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email" type="email" class="@error('email', 'login') is-invalid @enderror">

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
<!-- ## Stacks -->
## Stacks

<!-- Blade allows you to push to named stacks which can be rendered somewhere else in another view or layout. This can be particularly useful for specifying any JavaScript libraries required by your child views: -->
Blade에서는 명명된 스택에 콘텐츠를 추가(push)하고, 이 스택을 다른 뷰나 레이아웃에서 렌더링할 수 있습니다. 자식 뷰에서 필요한 JavaScript 라이브러리 등을 지정할 때 유용하게 쓸 수 있습니다.

```html
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

<!-- You may push to a stack as many times as needed. To render the complete stack contents, pass the name of the stack to the `@stack` directive: -->
스택에는 원하는 만큼 여러 번 push 할 수 있습니다. 전체 스택 내용을 렌더링하려면, `@stack` 디렉티브에 스택명을 전달합니다.

```html
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

<!-- If you would like to prepend content onto the beginning of a stack, you should use the `@prepend` directive: -->
스택 앞쪽에 내용을 추가(prepend)하고 싶다면, `@prepend` 디렉티브를 사용합니다.

```html
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
<!-- ## Service Injection -->
## Service Injection

<!-- The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/8.x/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class or interface name of the service you wish to resolve: -->
`@inject` 디렉티브를 사용해 Laravel의 [service container](/docs/8.x/container)에서 서비스를 내려받을 수 있습니다. `@inject`에 전달하는 첫 번째 인자는 서비스가 할당될 변수명이며, 두 번째 인자는 주입할 서비스의 클래스나 인터페이스 이름입니다.

```html
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="extending-blade"></a>
<!-- ## Extending Blade -->
## Extending Blade

<!-- Blade allows you to define your own custom directives using the `directive` method. When the Blade compiler encounters the custom directive, it will call the provided callback with the expression that the directive contains. -->
Blade는 `directive` 메서드를 이용해 사용자 정의 디렉티브를 직접 정의할 수 있습니다. Blade 컴파일러가 사용자 정의 디렉티브를 만나면, 디렉티브에 포함된 식(expression)을 전달하면서 지정한 콜백을 실행합니다.

<!-- The following example creates a `@datetime($var)` directive which formats a given `$var`, which should be an instance of `DateTime`: -->
아래 예제는 `@datetime($var)` 디렉티브를 만들고, 전달된 `$var`(`DateTime` 인스턴스여야 함)를 특정 포맷으로 출력합니다.

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::directive('datetime', function ($expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

<!-- As you can see, we will chain the `format` method onto whatever expression is passed into the directive. So, in this example, the final PHP generated by this directive will be: -->
위와 같이 하면, 디렉티브에 전달된 식에 대해 `format` 메서드를 체이닝합니다. 즉, 아래와 같이 작성한 Blade 템플릿이 실제로는 다음과 같이 컴파일됩니다.

```
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!NOTE]
> Blade 디렉티브의 로직을 변경한 뒤에는, 캐시된 Blade 뷰를 모두 삭제해야 합니다. `view:clear` 아티즌 명령어로 캐시된 Blade 뷰를 삭제할 수 있습니다.

<a name="custom-echo-handlers"></a>
<!-- ### Custom Echo Handlers -->
### Custom Echo Handlers

<!-- If you attempt to "echo" an object using Blade, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
Blade에서 오브젝트를 "echo"하면 그 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 하지만 사용 중인 클래스가 외부 라이브러리 소속이라서, `__toString` 메서드를 제어할 수 없는 상황도 있을 수 있습니다.

<!-- In these cases, Blade allows you to register a custom echo handler for that particular type of object. To accomplish this, you should invoke Blade's `stringable` method. The `stringable` method accepts a closure. This closure should type-hint the type of object that it is responsible for rendering. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이럴 때 Blade는 해당 타입의 오브젝트에 대해 사용자 정의 echo 핸들러를 등록할 수 있게 해줍니다. 이 기능은 Blade의 `stringable` 메서드를 통해 사용합니다. `stringable` 메서드는 클로저를 인자로 받는데, 여기서 책임지는 오브젝트의 타입을 타입힌트로 명확히 지정해야 합니다. 보통 `stringable` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다.

```
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<!-- Once your custom echo handler has been defined, you may simply echo the object in your Blade template: -->
이렇게 커스텀 echo 핸들러를 정의한 뒤에는, 해당 Blade 템플릿에서 객체를 바로 출력할 수 있습니다.

```html
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
<!-- ### Custom If Statements -->
### Custom If Statements

<!-- Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade provides a `Blade::if` method which allows you to quickly define custom conditional directives using closures. For example, let's define a custom conditional that checks the configured default "disk" for the application. We may do this in the `boot` method of our `AppServiceProvider`: -->
간단한 커스텀 조건문을 정의할 때 커스텀 디렉티브를 직접 프로그래밍하는 것은 필요 이상으로 복잡할 수 있습니다. 그래서 Blade는 클로저를 사용해 커스텀 조건문 디렉티브를 빠르게 정의할 수 있는 `Blade::if` 메서드를 제공합니다. 예를 들어, 애플리케이션의 기본 "디스크(disk)"를 체크하는 커스텀 조건문을 만들어 보겠습니다. 이 작업은 `AppServiceProvider`의 `boot` 메서드에서 할 수 있습니다.

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Blade::if('disk', function ($value) {
        return config('filesystems.default') === $value;
    });
}
```

<!-- Once the custom conditional has been defined, you can use it within your templates: -->
이 커스텀 조건문은 아래처럼 Blade 템플릿에서 사용할 수 있습니다.

```html
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