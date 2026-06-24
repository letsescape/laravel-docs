<!-- # Blade Templates -->
# Blade Templates

- [Introduction](#introduction)
    - [Supercharging Blade With Livewire](#supercharging-blade-with-livewire)
- [Displaying Data](#displaying-data)
    - [HTML Entity Encoding](#html-entity-encoding)
    - [Blade & JavaScript Frameworks](#blade-and-javascript-frameworks)
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
    - [Comments](#comments)
- [Components](#components)
    - [Rendering Components](#rendering-components)
    - [Passing Data To Components](#passing-data-to-components)
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
    - [Anonymous Components Paths](#anonymous-component-paths)
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
블레이드(Blade)는 Laravel에 기본으로 포함된, 단순하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, 블레이드는 템플릿에 순수 PHP 코드를 자유롭게 사용할 수 있도록 제한을 두지 않습니다. 실제로, 모든 블레이드 템플릿은 순수 PHP 코드로 컴파일되어, 수정되기 전까지는 캐시되므로 애플리케이션에 사실상 부하를 거의 주지 않습니다. 블레이드 템플릿 파일은 `.blade.php` 확장자를 가지며 일반적으로 `resources/views` 디렉터리에 저장됩니다.

<!-- Blade views may be returned from routes or controllers using the global `view` helper. Of course, as mentioned in the documentation on [views](/docs/9.x/views), data may be passed to the Blade view using the `view` helper's second argument: -->
블레이드 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용하여 반환할 수 있습니다. [views](/docs/9.x/views) 문서에서 안내된 것처럼, `view` 헬퍼의 두 번째 인수를 통해 데이터를 블레이드 뷰에 전달할 수 있습니다.

```
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>

<!-- ### Supercharging Blade With Livewire -->
### Supercharging Blade With Livewire

<!-- Want to take your Blade templates to the next level and build dynamic interfaces with ease? Check out [Laravel Livewire](https://laravel-livewire.com). Livewire allows you to write Blade components that are augmented with dynamic functionality that would typically only be possible via frontend frameworks like React or Vue, providing a great approach to building modern, reactive frontends without the complexities, client-side rendering, or build steps of many JavaScript frameworks. -->
블레이드 템플릿을 한 단계 더 발전시키고 손쉽게 동적인 인터페이스를 만들고 싶으신가요? [Laravel Livewire](https://laravel-livewire.com)를 살펴보세요. 라이브와이어를 사용하면, 보통 React나 Vue 같은 프론트엔드 프레임워크에서만 가능했던 동적인 기능을 블레이드 컴포넌트에 바로 추가할 수 있습니다. 덕분에 복잡한 자바스크립트 빌드나 클라이언트 렌더링 과정 없이, 현대적이고 반응적인 프론트엔드를 쉽게 구축할 수 있습니다.

<a name="displaying-data"></a>

<!-- ## Displaying Data -->
## Displaying Data

<!-- You may display data that is passed to your Blade views by wrapping the variable in curly braces. For example, given the following route: -->
블레이드 뷰에 전달된 데이터를 출력하려면 해당 변수를 중괄호로 감싸면 됩니다. 예를 들어 아래와 같은 라우트가 있다고 가정해봅시다.

```
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

<!-- You may display the contents of the `name` variable like so: -->
이 경우, `name` 변수의 내용을 아래와 같이 출력할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> 블레이드의 `{{ }}` 에코 구문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수를 통과합니다.

<!-- You are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement: -->
뷰에 전달된 변수 값만 출력하는 데 제한되지 않습니다. 어떤 PHP 함수의 결과도 그대로 블레이드 에코 구문에서 출력할 수 있습니다. 즉, 블레이드 에코 구문 내에 원하는 모든 PHP 코드를 사용할 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>

<!-- ### HTML Entity Encoding -->
### HTML Entity Encoding

<!-- By default, Blade (and the Laravel `e` helper) will double encode HTML entities. If you would like to disable double encoding, call the `Blade::withoutDoubleEncoding` method from the `boot` method of your `AppServiceProvider`: -->
기본적으로, 블레이드(그리고 Laravel의 `e` 헬퍼)는 HTML 엔터티를 이중 인코딩(double encoding)합니다. 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다.

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
기본적으로 블레이드의 `{{ }}` 구문은 XSS 공격 방지를 위해 PHP의 `htmlspecialchars` 함수를 통해 자동으로 이스케이프됩니다. 만약 데이터 이스케이프를 원하지 않는 경우, 아래와 같이 출력할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 입력받은 데이터를 그대로 출력할 때는 항상 주의를 기울이세요. 일반적으로는 XSS 공격을 방지하기 위해 이스케이프되는 이중 중괄호 구문을 사용해야 합니다.

<a name="blade-and-javascript-frameworks"></a>

<!-- ### Blade & JavaScript Frameworks -->
### Blade & JavaScript Frameworks

<!-- Since many JavaScript frameworks also use "curly" braces to indicate a given expression should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example: -->
많은 자바스크립트 프레임워크 역시 브라우저에 출력을 표시할 식을 중괄호로 감싸서 표현합니다. 이런 경우, 블레이드 렌더링 엔진에게 해당 표현식을 건드리지 말라고 알릴 때 `@` 기호를 사용할 수 있습니다. 예:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

<!-- In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to be rendered by your JavaScript framework. -->
이 예시에서, 블레이드는 `@` 심볼만 제거하고 `{{ name }}` 자체는 그대로 남겨두어, 자바스크립트 프레임워크가 렌더링하도록 처리합니다.

<!-- The `@` symbol may also be used to escape Blade directives: -->
또한 `@` 기호를 사용해 블레이드 디렉티브 자체를 이스케이프할 수 있습니다.

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
때로는 뷰에 배열을 전달해, 해당 데이터를 JSON으로 변환하여 자바스크립트 변수로 초기화해야 할 수도 있습니다. 예를 들면:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

<!-- However, instead of manually calling `json_encode`, you may use the `Illuminate\Support\Js::from` method directive. The `from` method accepts the same arguments as PHP's `json_encode` function; however, it will ensure that the resulting JSON is properly escaped for inclusion within HTML quotes. The `from` method will return a string `JSON.parse` JavaScript statement that will convert the given object or array into a valid JavaScript object: -->
하지만 직접 `json_encode`를 호출하는 대신, `Illuminate\Support\Js::from` 메서드 디렉티브를 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받지만, 결과 JSON이 HTML 따옴표 내부에 안전하게 포함될 수 있도록 이스케이프 처리를 보장합니다. `from` 메서드는 주어진 객체나 배열을 유효한 자바스크립트 객체로 변환하는 `JSON.parse` 자바스크립트 구문 문자열을 반환합니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

<!-- The latest versions of the Laravel application skeleton include a `Js` facade, which provides convenient access to this functionality within your Blade templates: -->
최근 Laravel 기본 스캐폴딩에는 이 기능을 블레이드 템플릿 내에서 손쉽게 사용할 수 있도록 `Js` 파사드가 포함되어 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 이미 존재하는 변수를 JSON으로 렌더링할 때만 사용해야 합니다. 블레이드 템플릿 엔진은 정규표현식을 기반으로 동작하기 때문에, 복잡한 식을 디렉티브에 넘기면 예기치 않은 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>

<!-- #### The `@verbatim` Directive -->
#### The `@verbatim` Directive

<!-- If you are displaying JavaScript variables in a large portion of your template, you may wrap the HTML in the `@verbatim` directive so that you do not have to prefix each Blade echo statement with an `@` symbol: -->
템플릿에서 자바스크립트 변수를 대량으로 출력해야 하는 경우, 에코 구문마다 일일이 `@` 기호를 붙이지 않고, 해당 영역 전체를 `@verbatim` 디렉티브로 감쌀 수 있습니다.

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
템플릿 상속과 데이터 표시 기능 외에도, 블레이드는 조건문이나 반복문과 같은 일반 PHP 제어 구조를 위한 간편한 단축 구문(디렉티브)도 제공합니다. 이런 디렉티브는 PHP 코드와 동일하게 동작하면서도 더 간결하고 읽기 좋은 문법을 제공합니다.

<a name="if-statements"></a>

<!-- ### If Statements -->
### If Statements

<!-- You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts: -->
`@if`, `@elseif`, `@else`, `@endif` 디렉티브를 이용해 `if` 문을 작성할 수 있습니다. 이 디렉티브는 PHP의 기본 if 문과 동일하게 동작합니다.

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
또한, 편의를 위해 `@unless` 디렉티브도 제공됩니다.

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

<!-- In addition to the conditional directives already discussed, the `@isset` and `@empty` directives may be used as convenient shortcuts for their respective PHP functions: -->
앞서 소개한 조건문 디렉티브 외에도 `@isset`과 `@empty` 디렉티브를 각 함수의 단축 구문으로 사용할 수 있습니다.

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

<!-- The `@auth` and `@guest` directives may be used to quickly determine if the current user is [authenticated](/docs/9.x/authentication) or is a guest: -->
`@auth`와 `@guest` 디렉티브를 사용하면 현재 사용자가 [authenticated](/docs/9.x/authentication)된 유저인지, 아니면 게스트인지 빠르게 검사할 수 있습니다.

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

<!-- If needed, you may specify the authentication guard that should be checked when using the `@auth` and `@guest` directives: -->
필요하다면 `@auth`와 `@guest` 디렉티브를 사용할 때 확인할 인증 가드를 지정할 수도 있습니다.

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
애플리케이션이 프로덕션 환경에서 동작 중인지 확인하려면 `@production` 디렉티브를 사용할 수 있습니다.

```blade
@production
    // Production specific content...
@endproduction
```

<!-- Or, you may determine if the application is running in a specific environment using the `@env` directive: -->
또는, `@env` 디렉티브를 사용해 특정 환경에서만 렌더링되도록 할 수 있습니다.

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
템플릿 상속의 특정 섹션에 컨텐츠가 존재하는지 확인할 때는 `@hasSection` 디렉티브를 사용할 수 있습니다.

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

<!-- You may use the `@sectionMissing` directive to determine if a section does not have content: -->
섹션에 내용이 없는 경우를 확인할 때는 `@sectionMissing` 디렉티브를 사용할 수 있습니다.

```blade
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
스위치 문은 `@switch`, `@case`, `@break`, `@default`, `@endswitch` 디렉티브를 사용해 작성할 수 있습니다.

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
조건문 이외에도, 블레이드는 PHP의 반복문 구조를 위한 간단한 디렉티브를 제공합니다. 이 디렉티브 역시 PHP 원본과 동일하게 동작합니다.

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
> `foreach` 반복문 안에서는 [loop variable](#the-loop-variable)를 사용해 현재 반복이 첫 번째인지 마지막 반복인지 등, 반복문에 대한 다양한 정보를 얻을 수 있습니다.

<!-- When using loops you may also skip the current iteration or end the loop using the `@continue` and `@break` directives: -->
반복문 내부에서 특정 반복을 건너뛰거나(`@continue`), 반복문 자체를 중단할 때(`@break`)는 아래와 같이 사용할 수 있습니다.

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
또한, 해당 조건을 디렉티브 선언부에 바로 포함시켜 더 간결하게 쓸 수도 있습니다.

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
`foreach` 반복문을 사용할 때, 반복문 내부에서는 `$loop` 변수를 사용할 수 있습니다. 이 변수는 현재 반복의 인덱스나, 반복문의 첫 번째/마지막 순회 여부 등 다양한 정보를 제공합니다.

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
중첩 루프의 경우, 상위 루프의 `$loop` 변수에 `parent` 속성을 통해 접근할 수 있습니다.

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
`$loop` 변수에는 다음과 같은 다양한 유용한 속성이 포함되어 있습니다.

| 속성               | 설명                                                      |
|--------------------|---------------------------------------------------------|
| `$loop->index`     | 현재 반복문의 인덱스(0부터 시작)                         |
| `$loop->iteration` | 현재 반복 순번(1부터 시작)                               |
| `$loop->remaining` | 반복문에서 남은 반복 횟수                                |
| `$loop->count`     | 반복 중인 배열의 전체 아이템 개수                        |
| `$loop->first`     | 이번 반복이 첫 번째인지 여부                              |
| `$loop->last`      | 이번 반복이 마지막인지 여부                               |
| `$loop->even`      | 이번 반복이 짝수인지 여부                                 |
| `$loop->odd`       | 이번 반복이 홀수인지 여부                                 |
| `$loop->depth`     | 현재 반복의 중첩 수준                                     |
| `$loop->parent`    | 중첩 루프일 때, 상위 반복문의 loop 변수                |

<a name="conditional-classes"></a>

<!-- ### Conditional Classes & Styles -->
### Conditional Classes & Styles

<!-- The `@class` directive conditionally compiles a CSS class string. The directive accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`@class` 디렉티브를 사용하면 조건에 따라 CSS 클래스 문자열을 만들어줄 수 있습니다. 이 디렉티브는 클래스 이름(문자열 또는 배열의 키)과 해당 클래스가 적용될지 여부를 나타내는 불린 값을 배열로 전달받습니다. 키가 숫자인 요소는 조건과 상관없이 항상 렌더링되는 클래스 목록에 포함됩니다.

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
이와 마찬가지로, `@style` 디렉티브를 사용하면 html 요소에 조건부로 인라인 CSS 스타일을 적용할 수 있습니다.

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
편의상, 체크박스 input이 "checked" 상태인지 쉽게 표시하려면 `@checked` 디렉티브를 사용할 수 있습니다. 지정한 조건이 `true`일 경우 `checked`가 출력됩니다.

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

<!-- Likewise, the `@selected` directive may be used to indicate if a given select option should be "selected": -->
마찬가지로, 특정 select option이 "selected" 상태인지 표시하려면 `@selected` 디렉티브를 사용할 수 있습니다.

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
그리고, 해당 요소가 "disabled" 처리되어야 할 경우에는 `@disabled` 디렉티브를 사용할 수 있습니다.

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

<!-- Moreover, the `@readonly` directive may be used to indicate if a given element should be "readonly": -->
또한, 해당 요소가 "readonly" 상태여야 한다면 `@readonly` 디렉티브를 사용할 수 있습니다.

```blade
<input type="email"
        name="email"
        value="email@laravel.com"
        @readonly($user->isNotAdmin()) />
```

<!-- In addition, the `@required` directive may be used to indicate if a given element should be "required": -->
그리고, 입력란에 "required" 속성을 추가하려면 `@required` 디렉티브를 사용할 수 있습니다.

```blade
<input type="text"
        name="title"
        value="title"
        @required($user->isAdmin()) />
```

<a name="including-subviews"></a>

<!-- ### Including Subviews -->
### Including Subviews

> [!NOTE]
> `@include` 디렉티브를 자유롭게 사용할 수 있지만, 블레이드 [components](#components)는 데이터 및 속성 바인딩처럼 `@include` 디렉티브에는 없는 여러 이점을 제공하는 비슷한 기능을 제공합니다.

<!-- Blade's `@include` directive allows you to include a Blade view from within another view. All variables that are available to the parent view will be made available to the included view: -->
블레이드의 `@include` 디렉티브를 사용하면, 다른 블레이드 뷰를 현재 뷰에 포함시킬 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수도 포함된 뷰에서 사용할 수 있습니다.

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

<!-- Even though the included view will inherit all data available in the parent view, you may also pass an array of additional data that should be made available to the included view: -->
포함될 뷰는 부모의 모든 데이터를 상속받지만, 별도의 추가 데이터를 배열로 전달할 수도 있습니다.

```blade
@include('view.name', ['status' => 'complete'])
```

<!-- If you attempt to `@include` a view which does not exist, Laravel will throw an error. If you would like to include a view that may or may not be present, you should use the `@includeIf` directive: -->
만약 존재하지 않는 뷰를 `@include`하려고 시도하면, Laravel에서 오류가 발생합니다. 포함할 뷰의 존재 여부가 불확실하다면 `@includeIf` 디렉티브를 사용하세요.

```blade
@includeIf('view.name', ['status' => 'complete'])
```

<!-- If you would like to `@include` a view if a given boolean expression evaluates to `true` or `false`, you may use the `@includeWhen` and `@includeUnless` directives: -->
특정 불린 표현식이 `true` 혹은 `false`로 평가될 때 뷰를 `@include`하려면 `@includeWhen`, `@includeUnless` 디렉티브를 사용할 수 있습니다.

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

<!-- To include the first view that exists from a given array of views, you may use the `@includeFirst` directive: -->
지정된 뷰 배열 중 먼저 존재하는 뷰 하나만 포함하고 싶다면, `@includeFirst` 디렉티브를 사용하세요.

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> 블레이드 뷰에서 `__DIR__` 및 `__FILE__` 상수 사용은 피해야 합니다. 이 값들은 컴파일된 뷰의 캐시 파일 위치를 나타내기 때문입니다.

<a name="rendering-views-for-collections"></a>

<!-- #### Rendering Views For Collections -->
#### Rendering Views For Collections

<!-- You may combine loops and includes into one line with Blade's `@each` directive: -->
Blade의 `@each` 디렉티브를 사용하면 반복문과 include를 한 줄로 결합할 수 있습니다.

```blade
@each('view.name', $jobs, 'job')
```

<!-- The `@each` directive's first argument is the view to render for each element in the array or collection. The second argument is the array or collection you wish to iterate over, while the third argument is the variable name that will be assigned to the current iteration within the view. So, for example, if you are iterating over an array of `jobs`, typically you will want to access each job as a `job` variable within the view. The array key for the current iteration will be available as the `key` variable within the view. -->
`@each` 디렉티브의 첫 번째 인수는 배열 또는 컬렉션의 각 요소에 대해 렌더링할 뷰입니다. 두 번째 인수는 반복할 배열이나 컬렉션이며, 세 번째 인수는 해당 뷰 내에서 현재 반복 요소에 할당될 변수명을 지정합니다. 예를 들어, `jobs` 배열을 반복할 때, 각 job을 뷰에서 `job` 변수명으로 사용하고 싶을 때 적합합니다. 현재 반복의 배열 키는 뷰 안에서 `key` 변수로 접근할 수 있습니다.

<!-- You may also pass a fourth argument to the `@each` directive. This argument determines the view that will be rendered if the given array is empty. -->
또한 `@each` 디렉티브에는 네 번째 인수를 전달할 수 있습니다. 이 인수는 지정한 배열이 비어 있을 때 렌더링할 뷰를 결정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링되는 뷰는 부모 뷰의 변수를 상속받지 않습니다. 자식 뷰에서 이러한 변수가 필요하다면 `@foreach`와 `@include` 디렉티브를 대신 사용해야 합니다.

<a name="the-once-directive"></a>

<!-- ### The `@once` Directive -->
### The `@once` Directive

<!-- The `@once` directive allows you to define a portion of the template that will only be evaluated once per rendering cycle. This may be useful for pushing a given piece of JavaScript into the page's header using [stacks](#stacks). For example, if you are rendering a given [component](#components) within a loop, you may wish to only push the JavaScript to the header the first time the component is rendered: -->
`@once` 디렉티브는 템플릿의 특정 블록이 한 번의 렌더링 사이클에서 단 한 번만 평가되도록 할 수 있습니다. 예를 들어, [stacks](#stacks)을 사용해 특정 JavaScript 코드를 페이지의 header에 한 번만 삽입하고 싶은 경우에 유용합니다. 반복문 안에서 [component](#components)를 여러 번 렌더링해도, 처음 렌더링할 때만 JavaScript를 header에 넣고 싶을 때 이렇게 사용할 수 있습니다.

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
`@once` 디렉티브는 `@push`, `@prepend`와 함께 자주 사용되므로, 편의를 위해 `@pushOnce`와 `@prependOnce` 디렉티브도 제공됩니다.

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>

<!-- ### Raw PHP -->
### Raw PHP

<!-- In some situations, it's useful to embed PHP code into your views. You can use the Blade `@php` directive to execute a block of plain PHP within your template: -->
특정 상황에서는 뷰 내에 PHP 코드를 직접 삽입하는 것이 유용할 수 있습니다. Blade의 `@php` 디렉티브를 사용해 템플릿 내에서 순수 PHP 코드를 실행할 수 있습니다.

```blade
@php
    $counter = 1;
@endphp
```

<!-- If you only need to write a single PHP statement, you can include the statement within the `@php` directive: -->
한 줄짜리 PHP 구문만 작성할 때는 `@php` 디렉티브에 직접 넣어서 더 간단하게 사용할 수도 있습니다.

```blade
@php($counter = 1)
```

<a name="comments"></a>

<!-- ### Comments -->
### Comments

<!-- Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application: -->
Blade에서는 뷰 안에 별도의 주석을 정의할 수 있습니다. 이 주석은 HTML 주석과 달리, 실제 애플리케이션에서 반환되는 HTML 코드에는 포함되지 않습니다.

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>

<!-- ## Components -->
## Components

<!-- Components and slots provide similar benefits to sections, layouts, and includes; however, some may find the mental model of components and slots easier to understand. There are two approaches to writing components: class based components and anonymous components. -->
컴포넌트와 슬롯은 섹션, 레이아웃, include와 비슷한 장점을 제공하지만, 컴포넌트와 슬롯의 개념이 더 직관적으로 느껴지는 경우도 많습니다. 컴포넌트는 크게 클래스 기반 컴포넌트와 익명(anonymous) 컴포넌트, 두 가지 방식으로 작성할 수 있습니다.

<!-- To create a class based component, you may use the `make:component` Artisan command. To illustrate how to use components, we will create a simple `Alert` component. The `make:component` command will place the component in the `app/View/Components` directory: -->
클래스 기반 컴포넌트를 생성할 때는 `make:component` Artisan 명령어를 사용할 수 있습니다. 컴포넌트 사용법을 설명하기 위해 간단한 `Alert` 컴포넌트를 만들어보겠습니다. `make:component` 명령어를 실행하면 컴포넌트 파일이 `app/View/Components` 디렉토리에 생성됩니다.

```shell
php artisan make:component Alert
```

<!-- The `make:component` command will also create a view template for the component. The view will be placed in the `resources/views/components` directory. When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory, so no further component registration is typically required. -->
`make:component` 명령어는 컴포넌트 뷰 템플릿도 자동으로 생성합니다. 이 뷰 파일은 `resources/views/components` 디렉토리에 위치하게 됩니다. 자신의 애플리케이션에서 컴포넌트를 작성할 때는, 컴포넌트가 `app/View/Components`와 `resources/views/components` 디렉토리 안에 존재하기만 하면 Laravel이 이를 자동으로 인식하므로 별도의 등록 작업이 필요하지 않습니다.

<!-- You may also create components within subdirectories: -->
컴포넌트는 하위 디렉토리(서브디렉토리)에도 생성할 수 있습니다.

```shell
php artisan make:component Forms/Input
```

<!-- The command above will create an `Input` component in the `app/View/Components/Forms` directory and the view will be placed in the `resources/views/components/forms` directory. -->
위 명령은 `app/View/Components/Forms` 디렉토리에 `Input` 컴포넌트 파일을 만들고, 뷰는 `resources/views/components/forms` 디렉토리에 생성합니다.

<!-- If you would like to create an anonymous component (a component with only a Blade template and no class), you may use the `--view` flag when invoking the `make:component` command: -->
또한, 클래스 없이 Blade 템플릿 파일만으로 구성되는 익명(anonymous) 컴포넌트를 만들고 싶다면 `make:component` 명령어를 실행할 때 `--view` 플래그를 사용할 수 있습니다.

```shell
php artisan make:component forms.input --view
```

<!-- The command above will create a Blade file at `resources/views/components/forms/input.blade.php` which can be rendered as a component via `<x-forms.input />`. -->
위 명령어는 `resources/views/components/forms/input.blade.php`에 Blade 파일을 생성하며, `<x-forms.input />` 형태로 컴포넌트를 렌더링할 수 있습니다.

<a name="manually-registering-package-components"></a>

<!-- #### Manually Registering Package Components -->
#### Manually Registering Package Components

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
자신의 애플리케이션에서 컴포넌트를 작성할 때는, 컴포넌트가 `app/View/Components`와 `resources/views/components` 디렉토리에 있으면 Laravel이 자동으로 인식합니다.

<!-- However, if you are building a package that utilizes Blade components, you will need to manually register your component class and its HTML tag alias. You should typically register your components in the `boot` method of your package's service provider: -->
하지만 Blade 컴포넌트를 사용하는 패키지를 개발할 때는 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 일반적으로 패키지의 서비스 프로바이더 내 `boot` 메서드에서 컴포넌트를 등록합니다.

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
컴포넌트를 등록하면, 등록한 태그 별칭을 사용하여 다음과 같이 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
또는, `componentNamespace` 메서드를 사용해 컴포넌트 클래스를 규칙에 따라 자동 로드할 수도 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`, `ColorPicker` 컴포넌트가 있고, 이들이 `Package\Views\Components` 네임스페이스에 있을 때 다음과 같이 등록합니다.

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
이렇게 하면 vendor 네임스페이스를 활용해 `package-name::` 문법으로 컴포넌트를 사용할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 케이스(PascalCase)로 변환해 연결된 클래스를 자동으로 인식합니다. 서브디렉토리 구성도 "dot" 표기법으로 지정할 수 있습니다.

<a name="rendering-components"></a>

<!-- ### Rendering Components -->
### Rendering Components

<!-- To display a component, you may use a Blade component tag within one of your Blade templates. Blade component tags start with the string `x-` followed by the kebab case name of the component class: -->
컴포넌트를 뷰에서 출력하려면, Blade 컴포넌트 태그를 사용합니다. Blade 컴포넌트 태그는 `x-`로 시작하며, 이어서 컴포넌트 클래스명을 케밥 케이스(kebab-case)로 씁니다.

```blade
<x-alert/>

<x-user-profile/>
```

<!-- If the component class is nested deeper within the `app/View/Components` directory, you may use the `.` character to indicate directory nesting. For example, if we assume a component is located at `app/View/Components/Inputs/Button.php`, we may render it like so: -->
컴포넌트 클래스가 `app/View/Components` 디렉토리의 더 깊은 폴더에 있다면, `.` 문자로 디렉토리 구조를 표현할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다면 아래와 같이 렌더링할 수 있습니다.

```blade
<x-inputs.button/>
```

<a name="passing-data-to-components"></a>

<!-- ### Passing Data To Components -->
### Passing Data To Components

<!-- You may pass data to Blade components using HTML attributes. Hard-coded, primitive values may be passed to the component using simple HTML attribute strings. PHP expressions and variables should be passed to the component via attributes that use the `:` character as a prefix: -->
컴포넌트에 데이터를 전달할 때는 HTML 속성을 사용합니다. 상수 형태의 값은 HTML 속성처럼 문자열로, PHP 변수나 표현식은 속성 앞에 `:`를 붙여 전달합니다.

```blade
<x-alert type="error" :message="$message"/>
```

<!-- You should define all of the component's data attributes in its class constructor. All public properties on a component will automatically be made available to the component's view. It is not necessary to pass the data to the view from the component's `render` method: -->
컴포넌트의 데이터 속성들은 클래스의 생성자에 정의해 주어야 합니다. 컴포넌트의 모든 public 속성은 자동으로 컴포넌트 뷰에서 사용할 수 있게 됩니다. `render` 메서드 안에서 따로 데이터를 뷰로 전달할 필요는 없습니다.

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
컴포넌트가 렌더링될 때, public 변수의 내용을 이름 그대로 뷰에서 출력할 수 있습니다.

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>

<!-- #### Casing -->
#### Casing

<!-- Component constructor arguments should be specified using `camelCase`, while `kebab-case` should be used when referencing the argument names in your HTML attributes. For example, given the following component constructor: -->
컴포넌트의 생성자 인수는 `camelCase`(카멜 케이스)로 지정해야 하며, HTML 속성명에서는 `kebab-case`(케밥 케이스)를 사용합니다. 예를 들어, 아래와 같은 컴포넌트 생성자가 있을 때,

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
`$alertType` 인수는 다음과 같이 전달할 수 있습니다.

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>

<!-- #### Short Attribute Syntax -->
#### Short Attribute Syntax

<!-- When passing attributes to components, you may also use a "short attribute" syntax. This is often convenient since attribute names frequently match the variable names they correspond to: -->
컴포넌트에 속성을 전달할 때, "단축 속성" 문법도 사용할 수 있습니다. 변수명과 속성명이 일치하는 경우 사용하면 편리합니다.

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
Alpine.js 같은 일부 JavaScript 프레임워크는 속성명 앞에 콜론을 사용하는데, Blade에서도 동일 문법이 있기 때문에 Blade에게 이 속성이 PHP 표현식이 아니라는 것을 명시하려면, 접두사로 더블 콜론(`::`)을 붙입니다. 예를 들어 아래 컴포넌트의 경우를 살펴봅니다.

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

<!-- The following HTML will be rendered by Blade: -->
Blade가 렌더링한 최종 HTML은 다음과 같이 나옵니다.

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>

<!-- #### Component Methods -->
#### Component Methods

<!-- In addition to public variables being available to your component template, any public methods on the component may be invoked. For example, imagine a component that has an `isSelected` method: -->
컴포넌트 템플릿에서 public 변수 뿐만 아니라 public 메서드도 호출할 수 있습니다. 예를 들어, `isSelected` 메서드가 있는 컴포넌트를 가정해보겠습니다.

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
컴포넌트 템플릿 안에서 메서드명과 동일한 변수 형태로 메서드를 호출할 수 있습니다.

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>

<!-- #### Accessing Attributes & Slots Within Component Classes -->
#### Accessing Attributes & Slots Within Component Classes

<!-- Blade components also allow you to access the component name, attributes, and slot inside the class's render method. However, in order to access this data, you should return a closure from your component's `render` method. The closure will receive a `$data` array as its only argument. This array will contain several elements that provide information about the component: -->
Blade 컴포넌트는 컴포넌트 이름, 속성(attribute), 슬롯(slot)에 접근할 수 있는 기능도 제공합니다. 이 데이터를 접근하려면 컴포넌트의 `render` 메서드에서 클로저(익명 함수)를 반환해야 합니다. 클로저는 `$data` 배열을 인수로 받아, 컴포넌트와 관련된 여러 요소 정보를 제공합니다.

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
`componentName`은 HTML 태그에서 `x-` 다음에 오는 이름과 동일합니다. 즉, `<x-alert />`의 `componentName`은 `alert`이 됩니다. `attributes`에는 해당 태그에 지정한 모든 속성이 들어 있습니다. `slot`은 컴포넌트 슬롯의 내용을 가진 `Illuminate\Support\HtmlString` 인스턴스입니다.

<!-- The closure should return a string. If the returned string corresponds to an existing view, that view will be rendered; otherwise, the returned string will be evaluated as an inline Blade view. -->
클로저는 문자열을 반환해야 하며, 반환한 문자열이 존재하는 뷰 이름이면 해당 뷰가 렌더링되고, 그렇지 않은 경우에는 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>

<!-- #### Additional Dependencies -->
#### Additional Dependencies

<!-- If your component requires dependencies from Laravel's [service container](/docs/9.x/container), you may list them before any of the component's data attributes and they will automatically be injected by the container: -->
컴포넌트가 Laravel의 [service container](/docs/9.x/container)로부터 의존성을 필요로 할 경우, 컴포넌트의 데이터 속성 앞에 의존성 타입을 나열하면 컨테이너가 자동으로 주입해줍니다.

```php
use App\Services\AlertCreator;

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
컴포넌트 템플릿에 public 메서드나 속성들이 노출되지 않도록 하려면, 컴포넌트 클래스에서 `$except` 배열 속성에 해당 변수명을 추가하면 됩니다.

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
앞서 컴포넌트에 데이터 속성을 전달하는 방법을 살펴봤지만, `class`처럼 컴포넌트 동작과 직접 관련 없는 HTML 속성이 필요한 경우가 있습니다. 이런 추가적인 속성은 컴포넌트 템플릿의 최상위 요소에 전달되는 것이 일반적입니다. 예를 들어, 다음과 같이 `alert` 컴포넌트를 렌더링한다고 가정해 봅니다.

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

<!-- All of the attributes that are not part of the component's constructor will automatically be added to the component's "attribute bag". This attribute bag is automatically made available to the component via the `$attributes` variable. All of the attributes may be rendered within the component by echoing this variable: -->
컴포넌트 생성자에 명시되지 않은 속성들은 자동으로 "속성 가방(attribute bag)"에 들어가며, 이 가방은 `$attributes` 변수로 컴포넌트 뷰에서 바로 사용할 수 있습니다. 모든 속성은 이 변수를 출력하면 렌더링됩니다.

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 현 시점에서 `@env`와 같은 디렉티브는 컴포넌트 태그 내부에서 지원되지 않습니다. 예를 들어, `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>

<!-- #### Default / Merged Attributes -->
#### Default / Merged Attributes

<!-- Sometimes you may need to specify default values for attributes or merge additional values into some of the component's attributes. To accomplish this, you may use the attribute bag's `merge` method. This method is particularly useful for defining a set of default CSS classes that should always be applied to a component: -->
속성에 기본값을 지정하거나, 특정 속성에 값을 추가로 병합하고 싶은 경우 attribute bag의 `merge` 메서드를 사용할 수 있습니다. 예를 들어, 컴포넌트에 항상 적용될 기본 CSS 클래스를 정의할 때 유용합니다.

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- If we assume this component is utilized like so: -->
이 컴포넌트를 다음과 같이 사용했다면,

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<!-- The final, rendered HTML of the component will appear like the following: -->
최종적으로 렌더링되는 HTML은 아래와 같습니다.

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>

<!-- #### Conditionally Merge Classes -->
#### Conditionally Merge Classes

<!-- Sometimes you may wish to merge classes if a given condition is `true`. You can accomplish this via the `class` method, which accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
어떤 조건이 `true`인 경우에만 클래스를 병합하고 싶다면, `class` 메서드를 사용할 수 있습니다. 이 메서드는 클래스명(혹은 클래스들의 배열)과 불리언 조건을 key-value 배열로 받습니다. 배열 인덱스가 숫자인 요소는 항상 클래스 목록에 추가됩니다.

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

<!-- If you need to merge other attributes onto your component, you can chain the `merge` method onto the `class` method: -->
여러 속성을 병합하고자 할 때는 `class` 메서드에 `merge` 메서드를 체이닝해서 사용할 수 있습니다.

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합 속성을 받을 필요가 없는 기타 HTML 요소에서 클래스 조건부 처리가 필요하다면 [`@class` directive](#conditional-classes)를 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>

<!-- #### Non-Class Attribute Merging -->
#### Non-Class Attribute Merging

<!-- When merging attributes that are not `class` attributes, the values provided to the `merge` method will be considered the "default" values of the attribute. However, unlike the `class` attribute, these attributes will not be merged with injected attribute values. Instead, they will be overwritten. For example, a `button` component's implementation may look like the following: -->
`class` 속성이 아닌 속성을 병합할 때는, `merge` 메서드에 전달한 값이 해당 속성의 "기본값"이 됩니다. 하지만 `class` 속성과 달리, 이 속성들은 주입된 속성 값과 합쳐지지 않고, 대신 덮어써집니다. 예를 들어, `button` 컴포넌트의 구현이 아래와 같다고 가정해 보겠습니다.

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

<!-- To render the button component with a custom `type`, it may be specified when consuming the component. If no type is specified, the `button` type will be used: -->
이제 컴포넌트를 사용할 때 별도로 `type`을 지정하면 해당 값이 적용되고, 지정하지 않으면 기본값인 `button`이 쓰입니다.

```blade
<x-button type="submit">
    Submit
</x-button>
```

<!-- The rendered HTML of the `button` component in this example would be: -->
이 예시에서 `button` 컴포넌트가 렌더링하는 HTML은 아래와 같습니다.

```blade
<button type="submit">
    Submit
</button>
```

<!-- If you would like an attribute other than `class` to have its default value and injected values joined together, you may use the `prepends` method. In this example, the `data-controller` attribute will always begin with `profile-controller` and any additional injected `data-controller` values will be placed after this default value: -->
만약 `class`가 아닌 다른 속성에서도 기본값과 사용자 값이 모두 합쳐지게 만들고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래 예시에서 `data-controller` 속성은 항상 `profile-controller`로 시작하고, 추가로 주입된 `data-controller` 값이 그 뒤에 붙습니다.

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>

<!-- #### Retrieving & Filtering Attributes -->
#### Retrieving & Filtering Attributes

<!-- You may filter attributes using the `filter` method. This method accepts a closure which should return `true` if you wish to retain the attribute in the attribute bag: -->
속성(attribute)은 `filter` 메서드로 손쉽게 필터링할 수 있습니다. 이 메서드는 속성을 attribute bag에 남기고 싶을 때 `true`를 반환하는 클로저를 인수로 받습니다.

```blade
{{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}
```

<!-- For convenience, you may use the `whereStartsWith` method to retrieve all attributes whose keys begin with a given string: -->
편의상, 특정 문자열로 시작하는 속성만 손쉽게 뽑고 싶을 때는 `whereStartsWith` 메서드를 사용할 수 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

<!-- Conversely, the `whereDoesntStartWith` method may be used to exclude all attributes whose keys begin with a given string: -->
반대로, 특정 문자열로 시작하지 않는 속성만 제외하고 싶을 때는 `whereDoesntStartWith` 메서드가 유용합니다.

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

<!-- Using the `first` method, you may render the first attribute in a given attribute bag: -->
`first` 메서드를 사용하면 attribute bag에서 첫 번째 속성만 렌더링할 수도 있습니다.

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

<!-- If you would like to check if an attribute is present on the component, you may use the `has` method. This method accepts the attribute name as its only argument and returns a boolean indicating whether or not the attribute is present: -->
컴포넌트에 특정 속성이 있는지 확인하려면 `has` 메서드를 사용할 수 있습니다. 인수로 속성명을 주면, 해당 속성의 존재 여부를 불리언 값으로 반환합니다.

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

<!-- You may retrieve a specific attribute's value using the `get` method: -->
특정 속성의 값을 가져오려면 `get` 메서드를 사용할 수 있습니다.

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>

<!-- ### Reserved Keywords -->
### Reserved Keywords

<!-- By default, some keywords are reserved for Blade's internal use in order to render components. The following keywords cannot be defined as public properties or method names within your components: -->
Blade 내부적으로 컴포넌트 렌더링에 사용되는 몇몇 예약어는 컴포넌트의 public 속성이나 메서드명으로 사용할 수 없습니다.

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
컴포넌트에 추가적인 컨텐츠(내용물)를 전달할 때 "슬롯(slot)" 기능을 자주 사용하게 됩니다. 컴포넌트 슬롯은 `$slot` 변수를 출력함으로써 뷰에 렌더링됩니다. 예를 들어, `alert` 컴포넌트가 아래와 같은 마크업을 가지고 있다고 가정해보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- We may pass content to the `slot` by injecting content into the component: -->
컴포넌트에 내용을 삽입하면 다음과 같이 `slot`으로 전달할 수 있습니다.

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- Sometimes a component may need to render multiple different slots in different locations within the component. Let's modify our alert component to allow for the injection of a "title" slot: -->
때로는 하나의 컴포넌트에 여러 위치에 다른 슬롯 내용을 삽입해야 할 수도 있습니다. 예를 들어, 경고창 컴포넌트에서 "제목" 슬롯을 추가해 보겠습니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- You may define the content of the named slot using the `x-slot` tag. Any content not within an explicit `x-slot` tag will be passed to the component in the `$slot` variable: -->
`x-slot` 태그를 사용하여 이름 있는 슬롯의 내용을 정의할 수 있습니다. 명시적인 `x-slot` 태그 안에 포함되지 않은 컨텐츠는 모두 컴포넌트의 `$slot` 변수로 전달됩니다.

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="scoped-slots"></a>

<!-- #### Scoped Slots -->
#### Scoped Slots

<!-- If you have used a JavaScript framework such as Vue, you may be familiar with "scoped slots", which allow you to access data or methods from the component within your slot. You may achieve similar behavior in Laravel by defining public methods or properties on your component and accessing the component within your slot via the `$component` variable. In this example, we will assume that the `x-alert` component has a public `formatAlert` method defined on its component class: -->
Vue와 같은 자바스크립트 프레임워크를 사용해 본 적이 있다면, "스코프드 슬롯(Scoped Slot)" 개념에 익숙할 수 있습니다. 스코프드 슬롯을 활용하면 슬롯 내부에서 컴포넌트의 데이터나 메서드에 접근할 수 있습니다. Laravel에서는 컴포넌트에 public 메서드나 속성(property)을 정의하고, 슬롯 내부에서 `$component` 변수를 통해 컴포넌트에 접근함으로써 유사한 동작을 구현할 수 있습니다. 예를 들어, 아래 예시에서는 `x-alert` 컴포넌트 클래스에 public `formatAlert` 메서드가 정의되어 있다고 가정합니다.

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
Blade 컴포넌트와 마찬가지로, 슬롯에도 CSS 클래스명 등 [attributes](#component-attributes)을 추가로 지정할 수 있습니다.

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
슬롯 속성과 상호작용하려면, 해당 슬롯 변수의 `attributes` 속성에 접근하면 됩니다. 속성 조작과 관련된 자세한 내용은 [component attributes](#component-attributes) 문서를 참고하세요.

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
규모가 매우 작은 컴포넌트의 경우, 컴포넌트 클래스와 컴포넌트의 뷰 템플릿을 각각 따로 관리하는 것이 번거롭게 느껴질 수 있습니다. 이럴 때에는 `render` 메서드에서 컴포넌트의 마크업을 직접 반환하여 인라인 컴포넌트를 만들 수 있습니다.

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
인라인 뷰를 렌더링하는 컴포넌트를 생성하려면, `make:component` 명령 실행 시 `inline` 옵션을 사용하면 됩니다.

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>

<!-- ### Dynamic Components -->
### Dynamic Components

<!-- Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable: -->
런타임에 어떤 컴포넌트를 렌더링해야 할지 결정해야 하는 상황이 있을 수 있습니다. 이 경우, Laravel에서 제공하는 `dynamic-component` 컴포넌트를 사용해, 런타임 값이나 변수에 따라 동적으로 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>

<!-- ### Manually Registering Components -->
### Manually Registering Components

> [!WARNING]
> 아래 문서 내용은 주로 Blade 컴포넌트를 포함하는 Laravel 패키지를 작성하는 분들에게 해당됩니다. 패키지 개발이 목적이 아니라면, 컴포넌트 관련 문서 중 이 부분은 생략하셔도 무방합니다.

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
애플리케이션에서 자체적으로 작성하는 컴포넌트는 `app/View/Components` 디렉터리와 `resources/views/components` 디렉터리 내에서 자동으로 검색되어 등록됩니다.

<!-- However, if you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider: -->
하지만 패키지에서 Blade 컴포넌트를 활용하거나, 컴포넌트를 관례와 다른 디렉터리에 둘 경우, 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야만 Laravel이 컴포넌트를 올바르게 찾을 수 있습니다. 일반적으로 패키지의 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록합니다.

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
이렇게 컴포넌트가 등록된 후에는, 해당 태그 별칭을 활용하여 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-package-alert/>
```

<!-- #### Autoloading Package Components -->
#### Autoloading Package Components

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
또는 `componentNamespace` 메서드를 활용하여 컴포넌트 클래스를 규칙에 따라 자동 로딩할 수도 있습니다. 예를 들어, `Nightshade` 패키지 내에 `Package\Views\Components` 네임스페이스에 소속된 `Calendar`, `ColorPicker` 컴포넌트가 있다고 가정합니다.

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
이렇게 하면, 패키지 네임스페이스와 `package-name::` 구문을 사용하여 컴포넌트를 참조할 수 있습니다.

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade는 컴포넌트 이름을 파스칼 케이싱(PascalCase)으로 변환하여 적절한 클래스를 자동으로 연결합니다. 하위 디렉터리도 "dot" 표기법으로 지원됩니다.

<a name="anonymous-components"></a>

<!-- ## Anonymous Components -->
## Anonymous Components

<!-- Similar to inline components, anonymous components provide a mechanism for managing a component via a single file. However, anonymous components utilize a single view file and have no associated class. To define an anonymous component, you only need to place a Blade template within your `resources/views/components` directory. For example, assuming you have defined a component at `resources/views/components/alert.blade.php`, you may simply render it like so: -->
인라인 컴포넌트와 비슷하게, 익명 컴포넌트는 파일 하나로 컴포넌트를 관리하는 방식을 제공합니다. 그러나 익명 컴포넌트는 컴포넌트 전용 클래스가 없고 하나의 뷰 파일만 사용합니다. 익명 컴포넌트를 정의하려면, `resources/views/components` 디렉터리 내에 Blade 템플릿을 두기만 하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 정의한 경우 아래와 같이 간단히 렌더링할 수 있습니다.

```blade
<x-alert/>
```

<!-- You may use the `.` character to indicate if a component is nested deeper inside the `components` directory. For example, assuming the component is defined at `resources/views/components/inputs/button.blade.php`, you may render it like so: -->
컴포넌트가 `components` 디렉터리 내에서 더 깊게 중첩되어 있다면, 점(`.`) 표기법을 사용할 수 있습니다. 예를 들어, `resources/views/components/inputs/button.blade.php`에 컴포넌트를 정의했다면 아래와 같이 사용할 수 있습니다.

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>

<!-- ### Anonymous Index Components -->
### Anonymous Index Components

<!-- Sometimes, when a component is made up of many Blade templates, you may wish to group the given component's templates within a single directory. For example, imagine an "accordion" component with the following directory structure: -->
여러 Blade 템플릿으로 이루어진 복잡한 컴포넌트라면, 관련 템플릿을 하나의 디렉터리 안에 묶어 관리하고 싶을 때가 있습니다. 예를 들어, 다음과 같은 구조로 "아코디언(accordion)" 컴포넌트를 만든다고 가정해 봅시다.

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<!-- This directory structure allows you to render the accordion component and its item like so: -->
이러한 구조를 사용하면, 다음과 같이 아코디언 및 아코디언 아이템 컴포넌트를 렌더링할 수 있습니다.

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

<!-- However, in order to render the accordion component via `x-accordion`, we were forced to place the "index" accordion component template in the `resources/views/components` directory instead of nesting it within the `accordion` directory with the other accordion related templates. -->
그러나 위와 같이 `x-accordion`을 통해 아코디언 컴포넌트를 렌더링하려면, "index" 아코디언 컴포넌트 템플릿을 다른 아코디언 관련 템플릿들과 함께 `accordion` 디렉터리 안에 중첩하지 못하고 `resources/views/components` 디렉터리에 두어야 했습니다.

<!-- Thankfully, Blade allows you to place an `index.blade.php` file within a component's template directory. When an `index.blade.php` template exists for the component, it will be rendered as the "root" node of the component. So, we can continue to use the same Blade syntax given in the example above; however, we will adjust our directory structure like so: -->
다행히도, Blade에서는 컴포넌트 템플릿 디렉터리에 `index.blade.php` 파일을 두는 방식도 지원합니다. 컴포넌트에 `index.blade.php`가 있으면, 해당 컴포넌트의 "루트" 노드로 렌더링됩니다. 따라서 위 예시의 Blade 문법을 동일하게 사용할 수 있으며, 디렉터리 구조만 다음과 같이 변경하면 됩니다.

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>

<!-- ### Data Properties / Attributes -->
### Data Properties / Attributes

<!-- Since anonymous components do not have any associated class, you may wonder how you may differentiate which data should be passed to the component as variables and which attributes should be placed in the component's [attribute bag](#component-attributes). -->
익명 컴포넌트는 별도의 클래스가 존재하지 않기 때문에, 어떤 데이터가 컴포넌트의 변수(프로퍼티)로 전달되어야 하고, 어떤 값이 컴포넌트의 [attribute bag](#component-attributes)에 저장되는지 혼란스러울 수 있습니다.

<!-- You may specify which attributes should be considered data variables using the `@props` directive at the top of your component's Blade template. All other attributes on the component will be available via the component's attribute bag. If you wish to give a data variable a default value, you may specify the variable's name as the array key and the default value as the array value: -->
이 경우, Blade 템플릿 상단에서 `@props` 지시어를 사용하여 데이터 변수로 취급할 속성을 지정할 수 있습니다. 컴포넌트로 전달된 그 외의 모든 속성은 속성 bag으로 전달됩니다. 데이터 변수에 기본값을 지정하려면, 배열의 키로 변수명, 값으로 기본값을 작성하면 됩니다.

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- Given the component definition above, we may render the component like so: -->
위 컴포넌트 정의를 바탕으로 컴포넌트를 아래와 같이 렌더링할 수 있습니다.

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>

<!-- ### Accessing Parent Data -->
### Accessing Parent Data

<!-- Sometimes you may want to access data from a parent component inside a child component. In these cases, you may use the `@aware` directive. For example, imagine we are building a complex menu component consisting of a parent `<x-menu>` and child `<x-menu.item>`: -->
때때로 자식 컴포넌트에서 부모 컴포넌트가 전달한 데이터를 접근해야 할 때가 있습니다. 이럴 때는 `@aware` 지시어를 사용할 수 있습니다. 예를 들어, 부모 `<x-menu>`와 자식 `<x-menu.item>`으로 이루어진 복합적인 메뉴 컴포넌트를 만든다고 상상해봅시다.

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

<!-- The `<x-menu>` component may have an implementation like the following: -->
부모인 `<x-menu>` 컴포넌트는 다음과 같이 구현할 수 있습니다.

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

<!-- Because the `color` prop was only passed into the parent (`<x-menu>`), it won't be available inside `<x-menu.item>`. However, if we use the `@aware` directive, we can make it available inside `<x-menu.item>` as well: -->
`color` prop이 부모 컴포넌트(즉, `<x-menu>`)에만 전달되었기 때문에, 기본적으로는 `<x-menu.item>`에서는 접근할 수 없습니다. 하지만, `@aware` 지시어를 사용하면 `<x-menu.item>` 안에서도 해당 값을 사용할 수 있습니다.

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시어는 부모 컴포넌트로 HTML 속성(attribute) 형태로 명시적으로 전달된 데이터만 접근할 수 있습니다. 부모 컴포넌트에 명시적으로 전달되지 않은, `@props`의 기본값 등은 `@aware`로 접근이 불가능합니다.

<a name="anonymous-component-paths"></a>

<!-- ### Anonymous Component Paths -->
### Anonymous Component Paths

<!-- As previously discussed, anonymous components are typically defined by placing a Blade template within your `resources/views/components` directory. However, you may occasionally want to register other anonymous component paths with Laravel in addition to the default path. -->
앞서 설명한 것처럼, 익명 컴포넌트는 기본적으로 `resources/views/components` 디렉터리에 Blade 템플릿을 두어 정의합니다. 그러나, 필요에 따라 Laravel에 익명 컴포넌트 경로를 추가로 등록할 수도 있습니다.

<!-- The `anonymousComponentPath` method accepts the "path" to the anonymous component location as its first argument and an optional "namespace" that components should be placed under as its second argument. Typically, this method should be called from the `boot` method of one of your application's [service providers](/docs/9.x/providers): -->
`anonymousComponentPath` 메서드는 첫 번째 인자로 익명 컴포넌트 위치의 "경로"를, 두 번째 인자로 선택적으로 "네임스페이스"를 받습니다. 이 메서드는 애플리케이션의 [service providers](/docs/9.x/providers)의 `boot` 메서드에서 호출하는 것이 일반적입니다.

```
/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

<!-- When component paths are registered without a specified prefix as in the example above, they may be rendered in your Blade components without a corresponding prefix as well. For example, if a `panel.blade.php` component exists in the path registered above, it may be rendered like so: -->
이처럼 별도의 prefix(접두어)를 지정하지 않고 컴포넌트 경로를 등록했다면, Blade 컴포넌트에서 해당 prefix 없이도 컴포넌트를 사용할 수 있습니다. 위 경로 예시에서 `panel.blade.php` 컴포넌트가 존재한다면 아래처럼 사용할 수 있습니다.

```blade
<x-panel />
```

<!-- Prefix "namespaces" may be provided as the second argument to the `anonymousComponentPath` method: -->
`anonymousComponentPath`의 두 번째 인자로 prefix(네임스페이스)를 지정할 수도 있습니다.

```
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

<!-- When a prefix is provided, components within that "namespace" may be rendered by prefixing to the component's namespace to the component name when the component is rendered: -->
prefix가 지정된 경우, Blade에서 해당 네임스페이스와 컴포넌트명을 합쳐서 사용해야 컴포넌트가 렌더링됩니다.

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
대부분의 웹 애플리케이션은 다양한 페이지에서 동일한 레이아웃을 공유합니다. 만약 매번 모든 뷰마다 레이아웃 HTML을 반복해서 작성해야 한다면, 유지보수 측면에서 매우 번거롭고 비효율적일 것입니다. 다행히도, 하나의 [Blade component](#components)로 레이아웃을 정의하여 애플리케이션 전반에 걸쳐 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>

<!-- #### Defining The Layout Component -->
#### Defining The Layout Component

<!-- For example, imagine we are building a "todo" list application. We might define a `layout` component that looks like the following: -->
예를 들어, "할 일(todo)" 목록 애플리케이션을 만든다고 가정해 봅시다. 아래와 같이 `layout` 컴포넌트를 정의할 수 있습니다.

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

<!-- #### Applying The Layout Component -->
#### Applying The Layout Component

<!-- Once the `layout` component has been defined, we may create a Blade view that utilizes the component. In this example, we will define a simple view that displays our task list: -->
`layout` 컴포넌트를 정의한 후, 이 컴포넌트를 활용하는 Blade 뷰를 만들 수 있습니다. 아래는 간단한 작업 목록을 보여주는 뷰 예시입니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

<!-- Remember, content that is injected into a component will be supplied to the default `$slot` variable within our `layout` component. As you may have noticed, our `layout` also respects a `$title` slot if one is provided; otherwise, a default title is shown. We may inject a custom title from our task list view using the standard slot syntax discussed in the [component documentation](#components): -->
컴포넌트에 전달된 내용은 `layout` 컴포넌트 내의 기본 슬롯 변수인 `$slot`으로 주입됩니다. 또한, 위 예시의 `layout` 컴포넌트는 `$title` 슬롯이 존재한다면 해당 값을, 그렇지 않으면 기본 타이틀을 사용합니다. 작업 목록 뷰에서 아래와 같이 표준 슬롯 문법을 사용해 커스텀 타이틀을 주입할 수 있습니다. ([component documentation](#components)에서 설명한 슬롯 문법 참고)

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

<!-- Now that we have defined our layout and task list views, we just need to return the `task` view from a route: -->
이제 layout과 task list 뷰를 정의했다면, 라우트에서 `task` 뷰만 반환하면 됩니다.

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
레이아웃은 "템플릿 상속(template inheritance)" 방식으로도 만들 수 있습니다. [components](#components) 방식이 도입되기 전에는 이 뷰 상속 방식이 레이아웃을 만드는 주요 방식이었습니다.

<!-- To get started, let's take a look at a simple example. First, we will examine a page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view: -->
간단한 예제로 시작해봅시다. 먼저, 페이지 전체에 사용할 수 있는 레이아웃 파일을 살펴보겠습니다. 대부분의 웹 애플리케이션이 여러 페이지에서 동일한 레이아웃을 사용하므로, 단일 Blade 뷰로 레이아웃을 정의하는 것이 편리합니다.

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
위 파일은 일반적인 HTML 마크업 구조이지만, `@section`과 `@yield` 지시어에 주목해야 합니다. `@section`은 특정 영역(섹션)을 정의하고, `@yield`는 지정한 이름의 섹션 내용을 표시합니다.

<!-- Now that we have defined a layout for our application, let's define a child page that inherits the layout. -->
이제, 정의한 레이아웃을 상속받는 자식 페이지를 만들어보겠습니다.

<a name="extending-a-layout"></a>

<!-- #### Extending A Layout -->
#### Extending A Layout

<!-- When defining a child view, use the `@extends` Blade directive to specify which layout the child view should "inherit". Views which extend a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`: -->
자식 뷰를 정의할 때에는, `@extends` Blade 지시어를 사용해서 상속받을 레이아웃 뷰를 명시합니다. 레이아웃을 상속받은 뷰는 `@section` 지시어로 해당 레이아웃 내부의 섹션에 콘텐츠를 주입할 수 있습니다. 위에서 예시로 본 것처럼, 각 섹션의 내용은 레이아웃에 있는 `@yield`를 통해 표시됩니다.

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
위 예시에서, `sidebar` 섹션은 `@@parent` 지시어를 사용하여 레이아웃의 sidebar에 내용을 덧붙이고 있습니다(덮어쓰는 것이 아님). `@@parent`는 렌더링 시 레이아웃의 sidebar 내용으로 대체됩니다.

> [!NOTE]
> 이전 예시와 달리, 여기서는 `sidebar` 섹션의 끝에 `@show` 대신 `@endsection`을 사용합니다. `@endsection`은 섹션만 정의하지만, `@show`는 섹션을 정의함과 동시에 **즉시 해당 내용을 출력(yield)** 합니다.

<!-- The `@yield` directive also accepts a default value as its second parameter. This value will be rendered if the section being yielded is undefined: -->
`@yield` 지시어는 두 번째 인수로 기본값도 받을 수 있습니다. 지정한 섹션이 정의되지 않은 경우, 아래와 같이 기본값이 렌더링됩니다.

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>

<!-- ## Forms -->
## Forms

<a name="csrf-field"></a>

<!-- ### CSRF Field -->
### CSRF Field

<!-- Anytime you define an HTML form in your application, you should include a hidden CSRF token field in the form so that [the CSRF protection](/docs/9.x/csrf) middleware can validate the request. You may use the `@csrf` Blade directive to generate the token field: -->
애플리케이션에서 HTML 폼을 정의할 때는 [the CSRF protection](/docs/9.x/csrf) 미들웨어가 요청을 검증할 수 있도록, 폼에 반드시 hidden CSRF 토큰 필드가 포함되어야 합니다. Blade의 `@csrf` 지시어를 사용하면 이 토큰 필드를 쉽게 생성할 수 있습니다.

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
HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 직접 만들 수 없으므로, 이런 HTTP 메서드를 흉내내려면 숨겨진 `_method` 필드를 추가해야 합니다. Blade의 `@method` 지시어를 사용하면 해당 필드를 쉽게 생성할 수 있습니다.

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>

<!-- ### Validation Errors -->
### Validation Errors

<!-- The `@error` directive may be used to quickly check if [validation error messages](/docs/9.x/validation#quick-displaying-the-validation-errors) exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
`@error` 지시어를 사용하면, [validation error messages](/docs/9.x/validation#quick-displaying-the-validation-errors)가 특정 속성(attribute)에 존재하는지 손쉽게 확인할 수 있습니다. `@error` 블록 내에서 `$message` 변수를 출력하면 해당 오류 메시지를 표시할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title"
    type="text"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- Since the `@error` directive compiles to an "if" statement, you may use the `@else` directive to render content when there is not an error for an attribute: -->
`@error` 지시어는 결국 "if" 문으로 컴파일되므로, 어떤 속성에 오류가 없을 때는 `@else` 지시어로 다른 내용을 렌더링할 수도 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror">
```

<!-- You may pass [the name of a specific error bag](/docs/9.x/validation#named-error-bags) as the second parameter to the `@error` directive to retrieve validation error messages on pages containing multiple forms: -->
또한, [the name of a specific error bag](/docs/9.x/validation#named-error-bags)의 이름을 `@error` 지시어의 두 번째 인자로 전달해, 여러 폼이 있는 페이지에서 특정 오류 메시지 그룹을 가져올 수도 있습니다.

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror">

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>

<!-- ## Stacks -->
## Stacks

<!-- Blade allows you to push to named stacks which can be rendered somewhere else in another view or layout. This can be particularly useful for specifying any JavaScript libraries required by your child views: -->
Blade에서는 이름을 지정한 스택(stack)에 콘텐츠를 쌓아두고, 다른 뷰나 레이아웃 내 원하는 위치에서 한 번에 렌더링할 수 있습니다. 이는 자식 뷰에서 필요한 자바스크립트 라이브러리를 지정할 때 매우 유용하게 사용할 수 있습니다.

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

<!-- If you would like to `@push` content if a given boolean expression evaluates to `true`, you may use the `@pushIf` directive: -->
특정 불린(boolean) 표현식이 `true`로 평가될 때만 `@push` 하고자 한다면, `@pushIf` 지시어를 사용할 수 있습니다.

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

<!-- You may push to a stack as many times as needed. To render the complete stack contents, pass the name of the stack to the `@stack` directive: -->
스택에는 여러 번 내용을 쌓을 수 있습니다. 스택의 전체 내용을 렌더링하려면, `@stack` 지시어에 스택 이름을 전달하세요.

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

<!-- If you would like to prepend content onto the beginning of a stack, you should use the `@prepend` directive: -->
스택의 맨 앞에 내용을 추가(앞에 붙이기)하려면, `@prepend` 지시어를 사용하면 됩니다.

```blade
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

<!-- The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/9.x/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class or interface name of the service you wish to resolve: -->
`@inject` 지시어를 사용하면 Laravel의 [service container](/docs/9.x/container)에서 서비스를 가져올 수 있습니다. `@inject`에 전달하는 첫 번째 인자는 서비스를 할당받을 변수 이름이고, 두 번째 인자는 가져올 서비스의 클래스 또는 인터페이스명입니다.

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
때때로 Blade 템플릿 문자열을 바로 HTML로 변환해야 하는 경우가 있습니다. 이럴 때는 `Blade` 파사드가 제공하는 `render` 메서드를 사용할 수 있습니다. `render` 메서드에는 Blade 템플릿 문자열과, 템플릿에 전달할 데이터를 배열 형태로 선택적으로 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

<!-- Laravel renders inline Blade templates by writing them to the `storage/framework/views` directory. If you would like Laravel to remove these temporary files after rendering the Blade template, you may provide the `deleteCachedView` argument to the method: -->
Laravel은 인라인 Blade 템플릿을 `storage/framework/views` 디렉토리에 저장하면서 렌더링합니다. 만약 Blade 템플릿을 렌더링한 후 이 임시 파일을 Laravel이 자동으로 삭제하길 원한다면, 메서드에 `deleteCachedView` 인수를 전달하면 됩니다.

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
[Turbo](https://turbo.hotwired.dev/)나 [htmx](https://htmx.org/) 같은 프론트엔드 프레임워크를 사용할 때, Blade 템플릿의 일부분만 HTTP 응답으로 반환해야 하는 경우가 종종 있습니다. 이럴 때 Blade의 "프래그먼트(fragment)" 기능을 사용할 수 있습니다.
우선, Blade 템플릿의 특정 부분을 `@fragment`와 `@endfragment` 지시어로 감싸줍니다.

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
이제 이 템플릿을 사용하는 뷰를 렌더링할 때, `fragment` 메서드를 호출해 특정 프래그먼트만 응답에 포함하도록 지정할 수 있습니다.

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

<!-- The `fragmentIf` method allows you to conditionally return a fragment of a view based on a given condition. Otherwise, the entire view will be returned: -->
`fragmentIf` 메서드는 주어진 조건에 따라 뷰의 프래그먼트만 반환할지, 아니면 전체 뷰를 반환할지를 제어할 수 있습니다.

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

<!-- The `fragments` and `fragmentsIf` methods allow you to return multiple view fragments in the response. The fragments will be concatenated together: -->
`fragments`와 `fragmentsIf` 메서드를 사용하면 한 번에 여러 프래그먼트를 응답으로 반환할 수 있습니다. 지정한 프래그먼트들이 이어붙여져 반환됩니다.

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
Blade는 `directive` 메서드를 사용해 나만의 사용자 지정 디렉티브를 정의할 수 있습니다. Blade 컴파일러가 커스텀 디렉티브를 만나면, 그 디렉티브에 포함된 표현식을 인수로 제공하며 등록된 콜백을 호출합니다.

<!-- The following example creates a `@datetime($var)` directive which formats a given `$var`, which should be an instance of `DateTime`: -->
다음 예제에서는 전달받은 `$var`(반드시 `DateTime` 인스턴스여야 함)를 형식화해서 출력하는 `@datetime($var)` 지시어를 만들어봅니다.

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
보시다시피, 지시어에 인수로 전달된 표현식에 바로 `format` 메서드를 체이닝해서 사용합니다. 이 예제에서는, 디렉티브에 의해 실제로 생성되는 PHP 코드는 다음과 같습니다.

```
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade 디렉티브의 로직을 수정한 후에는, 반드시 캐시된 모든 Blade 뷰 파일을 삭제해야 합니다. 캐시된 Blade 뷰 파일은 `view:clear` 아티즌 명령어로 삭제할 수 있습니다.

<a name="custom-echo-handlers"></a>

<!-- ### Custom Echo Handlers -->
### Custom Echo Handlers

<!-- If you attempt to "echo" an object using Blade, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
Blade에서 객체를 "echo"로 출력하려고 하면, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 하지만, 사용 중인 클래스가 서드파티 라이브러리의 것이라서 `__toString` 메서드를 직접 수정할 수 없는 경우도 있습니다.

<!-- In these cases, Blade allows you to register a custom echo handler for that particular type of object. To accomplish this, you should invoke Blade's `stringable` method. The `stringable` method accepts a closure. This closure should type-hint the type of object that it is responsible for rendering. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이럴 때 Blade는 해당 타입의 객체를 위한 커스텀 echo 핸들러를 등록할 수 있습니다. 이를 위해서는 Blade의 `stringable` 메서드를 사용하면 됩니다. `stringable` 메서드는 클로저를 인수로 받으며, 이 클로저는 랜더링할 객체의 타입을 타입힌트로 지정할 수 있습니다. 일반적으로 `stringable` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 호출합니다.

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
커스텀 echo 핸들러를 정의하고 나면, Blade 템플릿에서 해당 객체를 그냥 출력하면 핸들러가 자동으로 사용됩니다.

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>

<!-- ### Custom If Statements -->
### Custom If Statements

<!-- Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade provides a `Blade::if` method which allows you to quickly define custom conditional directives using closures. For example, let's define a custom conditional that checks the configured default "disk" for the application. We may do this in the `boot` method of our `AppServiceProvider`: -->
간단한 커스텀 조건문을 추가할 경우, 지시어를 직접 프로그래밍하는 것은 오히려 복잡할 수 있습니다. 그래서 Blade는 `Blade::if` 메서드를 제공하여, 클로저를 이용해 간편하게 커스텀 조건식 디렉티브를 정의할 수 있게 했습니다.
예를 들어, 애플리케이션에 설정된 기본 "디스크"를 체크하는 커스텀 조건문을 정의해보겠습니다. 아래는 `AppServiceProvider`의 `boot` 메서드에 작성하는 방식입니다.

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
커스텀 조건문을 정의한 후에는 템플릿에서 다음처럼 사용할 수 있습니다.

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
