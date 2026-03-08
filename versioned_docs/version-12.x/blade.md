# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 블레이드 향상시키기](#supercharging-blade-with-livewire)
- [데이터 표시하기](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [블레이드와 자바스크립트 프레임워크](#blade-and-javascript-frameworks)
- [블레이드 지시어](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스 및 스타일](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함하기](#including-subviews)
    - [`@once` 지시어](#the-once-directive)
    - [원시 PHP 코드](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달하기](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 속성(attributes)](#data-properties-attributes)
    - [부모 데이터 접근하기](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성하기](#building-layouts)
    - [컴포넌트로 레이아웃 구성](#layouts-using-components)
    - [템플릿 상속으로 레이아웃 구성](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [Method 필드](#method-field)
    - [유효성 검증 에러](#validation-errors)
- [스택](#stacks)
- [서비스 의존성 주입](#service-injection)
- [인라인 블레이드 템플릿 렌더링](#rendering-inline-blade-templates)
- [블레이드 프래그먼트 렌더링](#rendering-blade-fragments)
- [블레이드 확장하기](#extending-blade)
    - [커스텀 에코 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 기본 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과는 달리, Blade는 템플릿 내에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 일반 PHP 코드로 컴파일되어 수정될 때까지 캐시되며, Blade는 애플리케이션에 사실상 성능 오버헤드를 거의 추가하지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 일반적으로 `resources/views` 디렉터리에 저장됩니다.

Blade 뷰는 라우트나 컨트롤러에서 전역 `view` 헬퍼를 사용하여 반환할 수 있습니다. 물론, [뷰](/docs/12.x/views) 문서에서 언급한 것처럼, `view` 헬퍼의 두 번째 인수를 통해 Blade 뷰에 데이터를 전달할 수 있습니다:

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 블레이드 향상시키기

Blade 템플릿을 한 단계 더 발전시키고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해 보세요. Livewire를 사용하면 Blade 컴포넌트에 React, Svelte, Vue와 같은 프론트엔드 프레임워크에서만 가능했던 동적 기능을 손쉽게 추가할 수 있습니다. 번거로운 빌드 과정, 복잡한 클라이언트 사이드 렌더링 없이도 현대적인 리액티브 프론트엔드를 쉽게 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 표시하기 (Displaying Data)

Blade 뷰에 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어, 아래와 같은 라우트가 있다고 가정해봅니다:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 이렇게 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 에코 구문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수로 처리됩니다.

뷰에 전달된 변수의 내용만 표시하는 데 제한되지 않습니다. 어떤 PHP 함수의 결과든 에코할 수 있습니다. 실제로 블레이드 에코 구문 내에는 원하는 어떤 PHP 코드든 작성할 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩 (HTML Entity Encoding)

기본적으로, Blade와 Laravel의 `e` 함수는 HTML 엔티티를 이중으로 인코딩합니다. 이중 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
#### 이스케이프되지 않은 데이터 표시하기

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 PHP의 `htmlspecialchars` 함수로 보내집니다. 데이터 이스케이프를 원하지 않을 경우, 아래 예시처럼 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 사용자로부터 받은 데이터를 이스케이프하지 않고 에코할 때는 매우 주의해야 합니다. 보통 사용자 입력 값을 표시할 때에는 XSS 공격을 방지하기 위해 이스케이프된 이중 중괄호 구문(`{{ }}`)을 사용하는 것이 안전합니다.

<a name="blade-and-javascript-frameworks"></a>
### 블레이드와 자바스크립트 프레임워크 (Blade and JavaScript Frameworks)

많은 JavaScript 프레임워크에서도 중괄호를 사용해 브라우저에 표현식을 표시합니다. 이럴 경우, Blade 렌더링 엔진이 해당 표현식을 건드리지 않도록 `@` 심볼을 사용할 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

위 예제에서 Blade는 `@` 심볼만 제거하며, `{{ name }}` 표현식은 그대로 남아 JavaScript 프레임워크에 의해 처리됩니다.

`@` 심볼은 Blade 지시어를 이스케이프할 때도 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

배열을 뷰에 전달해 JavaScript 변수 초기화를 위해 JSON으로 렌더링하고 싶을 수 있습니다. 예시:

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

직접 `json_encode`를 호출하는 대신 `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 `json_encode`와 동일한 인수를 받지만, HTML 인용부호 내에 포함될 때 올바르게 이스케이프된 JSON을 반환합니다. 반환 값은 유효한 JavaScript 객체로 변환되는 `JSON.parse` 구문 문자열입니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 버전의 Laravel 기본 스켈레톤에는 이를 Blade에서 간편하게 사용할 수 있도록 `Js` 파사드가 포함되어 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수만 JSON으로 렌더링할 때 사용해야 합니다. Blade 템플릿 처리에는 정규 표현식이 사용되어 복잡한 표현식 전달 시 예기치 못한 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시어

템플릿의 넓은 범위에서 JavaScript 변수를 표시해야 한다면, HTML을 `@verbatim` 지시어로 감싸 각각의 Blade 에코 구문 앞에 `@`를 붙일 필요 없이 사용할 수 있습니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## 블레이드 지시어 (Blade Directives)

템플릿 상속이나 데이터 표시 외에도, Blade는 조건문, 반복문 등 일반적인 PHP 제어 구조를 위한 편리한 단축 구문을 제공합니다. 이 단축 구문 덕분에 PHP 제어 구조와 거의 동일하면서도 더 간결하고 깔끔하게 뷰를 작성할 수 있습니다.

<a name="if-statements"></a>
### If 문

`@if`, `@elseif`, `@else`, `@endif` 지시어를 사용해 Blade의 `if` 문을 작성할 수 있습니다. 이 지시어들은 PHP의 원본 문법과 동일하게 동작합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

편의를 위해 Blade는 `@unless` 지시어도 제공합니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

조건 지시어 외에도, `@isset` 및 `@empty` 지시어로 각 PHP 함수의 단축 구문을 제공받을 수 있습니다:

```blade
@isset($records)
    // $records가 정의되어 있고 null이 아닙니다...
@endisset

@empty($records)
    // $records가 "비어" 있습니다...
@endempty
```

<a name="authentication-directives"></a>
#### 인증 지시어

`@auth` 및 `@guest` 지시어를 사용하면 현재 사용자가 [인증](/docs/12.x/authentication)되었는지 또는 게스트인지 빠르게 판별할 수 있습니다:

```blade
@auth
    // 사용자가 인증되었습니다...
@endauth

@guest
    // 사용자가 인증되지 않았습니다...
@endguest
```

필요하다면, `@auth` 및 `@guest` 지시어에 인증 가드를 명시할 수도 있습니다:

```blade
@auth('admin')
    // 사용자가 인증되었습니다...
@endauth

@guest('admin')
    // 사용자가 인증되지 않았습니다...
@endguest
```

<a name="environment-directives"></a>
#### 환경 지시어

`@production` 지시어를 사용해 애플리케이션이 프로덕션 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@production
    // 프로덕션 환경 전용 콘텐츠...
@endproduction
```

또는 `@env` 지시어로 특정 환경에서 애플리케이션이 실행되고 있는지 확인할 수 있습니다:

```blade
@env('staging')
    // 애플리케이션이 "staging" 환경에서 실행 중입니다...
@endenv

@env(['staging', 'production'])
    // 애플리케이션이 "staging" 또는 "production" 환경에서 실행 중입니다...
@endenv
```

<a name="section-directives"></a>
#### 섹션 지시어

템플릿 상속의 섹션에 콘텐츠가 있는지 `@hasSection` 지시어로 확인할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

`sectionMissing` 지시어로 섹션에 콘텐츠가 없는지 확인할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
#### 세션 지시어

`@session` 지시어로 [세션](/docs/12.x/session) 값의 존재 여부를 확인할 수 있습니다. 세션 값이 존재하면, `@session`과 `@endsession` 사이의 템플릿 내용이 평가됩니다. 이 안에서 `$value` 변수로 세션값을 표시할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="context-directives"></a>
#### 컨텍스트 지시어

`@context` 지시어로 [컨텍스트](/docs/12.x/context) 값의 존재 여부를 확인할 수 있습니다. 컨텍스트 값이 존재하면, `@context`와 `@endcontext` 사이의 템플릿 내용이 평가됩니다. 이 안에서 `$value` 변수로 해당 값을 표시할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```

<a name="switch-statements"></a>
### Switch 문

`@switch`, `@case`, `@break`, `@default`, `@endswitch` 지시어를 사용해 Switch 문을 작성할 수 있습니다:

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
### 반복문 (Loops)

조건문 외에도, Blade는 PHP 반복문을 위한 단순한 지시어를 제공합니다. 역시 각 지시어는 PHP 원본 구문과 동일하게 동작합니다:

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
> `foreach` 반복문 내에서는 [loop 변수](#the-loop-variable)를 활용해 반복과 관련된 다양한 정보를 확인할 수 있습니다. (예: 첫 번째/마지막 반복 여부 등)

반복문에서 현재 반복을 건너뛰거나 반복을 중단하고 싶을 때는 `@continue` 및 `@break` 지시어를 사용할 수 있습니다:

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

또한, 반복문 선언부에서 조건을 바로 명시할 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### Loop 변수

`foreach` 반복문 내에서는 `$loop` 변수가 자동으로 제공됩니다. 이 변수는 현재 반복의 인덱스(순번)나 반복의 첫/마지막 여부 등, 반복문과 관련된 다양한 정보를 편리하게 확인할 수 있습니다:

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

중첩 반복문에서는 부모 반복문의 `$loop` 변수에 `parent` 속성으로 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

`$loop` 변수에서 제공하는 기타 주요 속성:

<div class="overflow-auto">

| 속성                | 설명                                                      |
| ------------------- | ------------------------------------------------------- |
| `$loop->index`      | 현재 반복 순서(0부터 시작)                                |
| `$loop->iteration`  | 현재 반복 횟수(1부터 시작)                                |
| `$loop->remaining`  | 남은 반복 횟수                                           |
| `$loop->count`      | 전체 반복 대상 아이템 개수                                |
| `$loop->first`      | 반복문의 첫 번째 반복인지 여부                             |
| `$loop->last`       | 반복문의 마지막 반복인지 여부                             |
| `$loop->even`       | 반복 횟수가 짝수인지 여부                                 |
| `$loop->odd`        | 반복 횟수가 홀수인지 여부                                 |
| `$loop->depth`      | 현재 반복문의 중첩 깊이                                   |
| `$loop->parent`     | 중첩 반복문에서 부모의 loop 변수                          |

</div>

<a name="conditional-classes"></a>
### 조건부 클래스 및 스타일 (Conditional Classes & Styles)

`@class` 지시어는 조건에 따라 CSS 클래스를 동적으로 작성해줍니다. 배열을 전달할 때, 키는 추가할 클래스명이고 값은 조건을 판단합니다. 배열 키가 숫자라면 조건과 관계없이 항상 클래스 리스트에 포함됩니다:

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

마찬가지로 `@style` 지시어를 사용해 조건에 따라 인라인 CSS 스타일을 동적으로 추가할 수 있습니다:

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
### 추가 속성

체크박스 등의 HTML input 요소가 "checked" 상태인지 쉽게 표시하려면 `@checked` 지시어를 사용할 수 있습니다. 조건이 `true`이면 `checked`가 출력됩니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```

마찬가지로, select option이 "selected" 상태인지 표시하려면 `@selected` 지시어를 사용할 수 있습니다:

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

또한, 요소가 "disabled" 상태인지 나타내려면 `@disabled` 지시어를 사용할 수 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

"readonly" 상태인지 확인하려면 `@readonly` 지시어를 사용할 수 있습니다:

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```

또한, 입력란이 "required" 상태인지 표시하려면 `@required` 지시어를 사용할 수 있습니다:

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```

<a name="including-subviews"></a>
### 서브뷰 포함하기

> [!NOTE]
> `@include` 지시어를 자유롭게 사용할 수 있지만, Blade의 [컴포넌트](#components)는 데이터/속성 바인딩 등 추가적인 장점을 제공하므로 가능한 한 컴포넌트 사용을 권장합니다.

Blade의 `@include` 지시어는 다른 Blade 뷰 파일을 포함할 수 있도록 해줍니다. 부모 뷰의 모든 변수가 포함된 뷰에서도 그대로 사용 가능합니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- 폼 내용 -->
    </form>
</div>
```

포함되는 뷰에 부모 데이터 외에 추가 데이터를 전달하고 싶다면 배열 형태로 명시할 수 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```

존재하지 않는 뷰를 `@include` 하려고 하면 Laravel에서 에러가 발생합니다. 뷰의 존재 여부에 따라 조건부로 뷰를 포함하려면 `@includeIf` 지시어를 사용할 수 있습니다:

```blade
@includeIf('view.name', ['status' => 'complete'])
```

불린 조건에 따라 포함 여부를 결정하려면 `@includeWhen` 또는 `@includeUnless` 지시어를 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

여러 뷰 중에서 실제로 존재하는 첫 번째 뷰만 포함하려면 `includeFirst` 지시어를 사용합니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

부모 뷰의 변수를 상속하지 않고 뷰를 포함하고 싶다면, `@includeIsolated` 지시어를 사용할 수 있습니다. 이 경우 명시적으로 넘긴 변수만 뷰에서 사용할 수 있습니다:

```blade
@includeIsolated('view.name', ['user' => $user])
```

> [!WARNING]
> Blade 뷰 내에서 `__DIR__`와 `__FILE__` 상수를 사용하는 것은 피해야 합니다. 이 값들은 캐시된 컴파일 뷰의 위치를 참조하게 됩니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션 단위로 뷰 렌더링하기

Blade의 `@each` 지시어로 반복문과 include를 한 줄로 결합할 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```

첫 번째 인자는 반복마다 표시할 뷰 이름, 두 번째는 반복 대상 배열 또는 컬렉션, 세 번째는 뷰 내부에서 반복되는 단일 항목을 참조할 변수명입니다. `jobs` 배열을 반복할 경우 이 뷰 내에서 `job` 변수를 사용할 수 있습니다. 현재 반복의 배열 키는 `key` 변수로 접근 가능합니다.

네 번째 인자를 추가하면, 배열이 비어있을 때 표시할 뷰를 지정할 수 있습니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each`로 렌더링된 뷰는 부모 뷰의 변수를 상속받지 않습니다. 자식 뷰에서 부모의 변수가 필요하다면, `@foreach`와 `@include` 조합을 사용하세요.

<a name="the-once-directive"></a>
### `@once` 지시어

`@once` 지시어로 템플릿의 특정 부분을 한 번만 실행(렌더링)할 수 있습니다. 예를 들어, 반복 구조 내에서 [스택](#stacks)에 특정 JavaScript를 오직 한 번만 푸시하고 싶을 때 유용합니다:

```blade
@once
    @push('scripts')
        <script>
            // 사용자 정의 자바스크립트...
        </script>
    @endpush
@endonce
```

`@once` 지시어는 `@push`, `@prepend`와 자주 같이 쓰이므로, 간략하게 쓸 수 있는 `@pushOnce`, `@prependOnce` 지시어도 제공합니다:

```blade
@pushOnce('scripts')
    <script>
        // 사용자 정의 자바스크립트...
    </script>
@endPushOnce
```

여러 개의 뷰에서 동일한 내용을 중복 푸시하는 경우, 두 번째 인자로 고유 식별자를 지정해 중복 렌더링을 막을 수 있습니다:

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
### 원시 PHP 코드

상황에 따라 뷰 내부에서 원시 PHP 코드를 실행해야 할 때가 있습니다. 이 경우 Blade의 `@php` 지시어로 PHP 블록을 작성할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```

클래스 import만 필요하다면 `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```

두 번째 인자로 별칭(alias)을 지정할 수도 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```

같은 네임스페이스 내 여러 클래스를 동시에 import할 때는 중괄호로 묶어서 사용할 수 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```

`@use` 지시어는 함수와 상수 import도 지원합니다. 이 경우 `function` 또는 `const`를 path 앞에 붙여 사용하세요:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```

 함수·상수 import 역시 별칭 지정이 가능합니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```

함수·상수 import도 그룹 지정이 지원됩니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```

<a name="comments"></a>
### 주석

Blade에서는 주석을 뷰에 남길 수 있습니다. HTML 주석과 달리, Blade 주석은 최종 렌더된 HTML에 포함되지 않습니다:

```blade
{{-- 이 주석은 렌더된 HTML에 포함되지 않습니다 --}}
```

<a name="components"></a>
## 컴포넌트 (Components)

컴포넌트와 슬롯은 sections, layouts, includes와 비슷한 기능을 제공하지만, 일부 개발자에게는 더 직관적으로 이해할 수 있습니다. 컴포넌트는 클래스 기반과 익명 컴포넌트, 두 가지 방식으로 작성할 수 있습니다.

클래스 기반 컴포넌트를 생성하려면 `make:component` Artisan 명령어를 사용하세요. 예를 들어, 간단한 `Alert` 컴포넌트를 만들 때:

```shell
php artisan make:component Alert
```

이 명령을 실행하면 컴포넌트 클래스가 `app/View/Components` 디렉터리에, 뷰 템플릿은 `resources/views/components` 디렉터리에 생성됩니다. 일반적인 애플리케이션에서는 이 디렉터리에 있는 컴포넌트들이 자동으로 등록되어 별도의 추가 등록이 필요 없습니다.

서브디렉터리에 컴포넌트를 생성할 수도 있습니다:

```shell
php artisan make:component Forms/Input
```

위 명령은 `app/View/Components/Forms` 디렉터리 내에 `Input` 컴포넌트, `resources/views/components/forms` 디렉터리에 뷰를 생성합니다.

<a name="manually-registering-package-components"></a>
#### 패키지 컴포넌트 수동 등록

애플리케이션 내부에서는 컴포넌트가 특정 디렉터리에서 자동으로 감지됩니다. 하지만 패키지 개발 시에는 컴포넌트 클래스와 HTML 태그 별칭을 직접 등록해야 합니다. 보통 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

등록 후에는 해당 태그 별칭으로 컴포넌트를 사용할 수 있습니다:

```blade
<x-package-alert/>
```

또는 `componentNamespace` 메서드를 사용해 네이밍 규칙에 따라 컴포넌트 클래스를 오토로드할 수도 있습니다. 예를 들어, `Nightshade` 패키지에 `Calendar`, `ColorPicker` 라는 컴포넌트가 있고 네임스페이스가 `Package\Views\Components`인 경우:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 패키지 네임스페이스를 붙여서 컴포넌트를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 자동 매칭합니다. 서브디렉터리는 "dot" 표기법을 사용할 수 있습니다.

<a name="rendering-components"></a>
### 컴포넌트 렌더링

컴포넌트를 표시하려면, Blade 템플릿 내에 `x-`로 시작하는 컴포넌트 태그를 사용하세요. 컴포넌트 클래스명은 케밥 케이스로 사용합니다:

```blade
<x-alert/>

<x-user-profile/>
```

컴포넌트 클래스가 `app/View/Components`의 더 깊은 디렉터리에 위치한다면 `.`(점)으로 계층 구조를 표시할 수 있습니다. 예를 들어, `app/View/Components/Inputs/Button.php`에 컴포넌트가 있다면:

```blade
<x-inputs.button/>
```

컴포넌트를 조건부로 렌더링하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * 컴포넌트가 렌더링되어야 하는지 반환
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="index-components"></a>
### 인덱스 컴포넌트

컴포넌트가 여러 개의 관련 컴포넌트로 구성되어 단일 디렉터리에 모아두고 싶을 때 사용할 수 있습니다. 예를 들어, "card" 컴포넌트가 다음과 같은 구조라면:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```

최상위 `Card` 컴포넌트는 디렉터리와 동일한 이름이므로, `<x-card.card>` 대신 `<x-card>`로 바로 사용할 수 있습니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```

<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

Blade 컴포넌트에 데이터를 전달할 때는 HTML 속성 형태로 사용합니다. 고정 값(원시 데이터)은 일반 속성 문자열로, PHP 변수나 식은 속성명 앞에 `:`(콜론)을 붙여 전달합니다:

```blade
<x-alert type="error" :message="$message"/>
```

컴포넌트 클래스의 생성자에서 모든 데이터 속성을 선언해야 합니다. 컴포넌트의 public 속성은 자동으로 뷰에서 사용할 수 있으며, `render` 메서드에서 직접 뷰로 전달하지 않아도 됩니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * 컴포넌트 인스턴스 생성자.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * 컴포넌트의 뷰/콘텐츠를 반환.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

컴포넌트가 렌더링될 때, 컴포넌트의 public 변수를 변수명으로 에코해서 표시할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### 인자명 표기

컴포넌트 생성자의 인자는 `camelCase`로 선언하고, HTML 속성에서는 `kebab-case`로 참조해야 합니다. 예:

```php
/**
 * 컴포넌트 인스턴스 생성자.
 */
public function __construct(
    public string $alertType,
) {}
```

컴포넌트 사용 시에는 다음과 같이 전달합니다:

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 간단 속성 구문(Short Attribute Syntax)

속성명과 변수명이 같을 땐 간단 구문을 사용할 수 있습니다:

```blade
{{-- 간단 속성 구문 --}}
<x-profile :$userId :$name />

{{-- 아래와 동일합니다 --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js 등 일부 JS 프레임워크는 속성명 앞에 콜론(`:`)을 붙여 사용합니다. 이때 PHP 표현식이 아님을 명확히 하기 위해, 속성명 앞에 더블 콜론(`::`)을 붙여 사용할 수 있습니다:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

Blade는 아래처럼 렌더링합니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### 컴포넌트 메서드

public 변수뿐 아니라 public 메서드도 컴포넌트 템플릿에서 호출할 수 있습니다. 예를 들어, `isSelected`라는 메서드를 가진 컴포넌트가 있다면:

```php
/**
 * 현재 option이 선택된 것인지 반환.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

아래와 같이 템플릿에서 직접 사용할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스에서 속성 및 슬롯 접근

Blade 컴포넌트는 render 메서드에서 컴포넌트 이름, 속성, 슬롯을 접근할 수 있습니다. 이 데이터를 사용하려면 `render` 메서드에서 클로저를 반환해야 합니다:

```php
use Closure;

/**
 * 컴포넌트의 뷰/콘텐츠 반환.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```

반환되는 클로저는 `$data` 배열을 인자로 받을 수 있으며, 다음과 같은 정보를 제공합니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
}
```

> [!WARNING]
> `$data` 배열의 요소를 Blade 문자열에 직접 삽입하지 마세요. 악의적 속성을 통한 원격 코드 실행 위험이 있습니다.

`componentName`은 `x-` 접두사 이후의 태그 이름입니다. `<x-alert />`의 경우 `componentName`은 `alert`입니다. `attributes`는 태그에 전달된 모든 속성, `slot`은 슬롯에 전달된 내용을 담은 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저의 반환값이 실제로 존재하는 뷰 이름이라면 해당 뷰를 렌더링하고, 아니라면 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 의존성 주입

컴포넌트가 Laravel의 [서비스 컨테이너](/docs/12.x/container)에서 의존성을 필요로 한다면, 이 의존성을 생성자 데이터 속성들 앞에 나열하면 자동으로 주입됩니다:

```php
use App\Services\AlertCreator;

/**
 * 컴포넌트 인스턴스 생성자.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
#### 속성/메서드 노출 제한

일부 public 메서드나 속성을 컴포넌트 템플릿에서 노출하고 싶지 않다면, 컴포넌트의 `$except` 배열 프로퍼티에 포함시키세요:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * 템플릿에 노출되지 않을 속성/메서드.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * 컴포넌트 인스턴스 생성자.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
### 컴포넌트 속성

앞서 데이터 속성 전달법을 다뤘지만, `class`와 같이 컴포넌트 동작에 필요 없는 추가 HTML 속성을 명시해야 할 때가 있습니다. 이럴 경우, 이런 속성들은 자동으로 "attribute bag"에 추가되어 `$attributes` 변수로 뷰에서 접근 가능합니다:

```blade
<div {{ $attributes }}>
    <!-- 컴포넌트 내용 -->
</div>
```

> [!WARNING]
> 현 시점에서 컴포넌트 태그 내에서는 `@env` 같은 지시어 사용이 지원되지 않습니다. 예: `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본값/병합 속성

속성에 기본값을 지정하거나, 일부 속성에 추가 값을 병합하고 싶을 때는 attribute bag의 `merge` 메서드를 사용할 수 있습니다. CSS 클래스의 기본값을 지정하는 데 특히 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

컴포넌트를 이렇게 사용한다고 가정하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

최종 렌더되는 HTML:

```blade
<div class="alert alert-error mb-4">
    <!-- $message 변수의 내용 -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 조건부 클래스 병합

`class` 메서드로 조건부로 클래스를 병합할 수 있습니다. 배열 키는 클래스명, 값은 조건식이며, 숫자 키는 무조건 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

`merge` 메서드와 조합해 다른 속성도 병합할 수 있습니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> 병합된 속성 외 HTML 요소에 조건부 클래스를 붙이고 싶다면 [@class 지시어](#conditional-classes)를 사용하세요.

<a name="non-class-attribute-merging"></a>
#### class 외 속성 병합

`class`가 아닌 속성에 대해 `merge`를 사용할 경우, merge 메서드에 지정된 값이 "기본값"이 되며, 주입된 속성 값과 병합되지 않고 오버라이드됩니다. 예시:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

컴포넌트 사용 시:

```blade
<x-button type="submit">
    Submit
</x-button>
```

렌더 결과:

```blade
<button type="submit">
    Submit
</button>
```

`class` 외 속성에서도 기본값과 주입값을 합치고 싶다면, `prepends` 메서드를 사용할 수 있습니다. 아래와 같이 `data-controller`가 항상 `profile-controller`로 시작하게끔 할 수 있습니다:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 속성 필터링 및 추출

`filter` 메서드로 속성을 필터링할 수 있습니다. 이 메서드는 속성값과 속성명을 받아, 필터링 기준이 `true`인 것만 남깁니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

특정 접두사로 시작하는 속성만 추출하려면 `whereStartsWith` 메서드를 사용합니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

반대로 특정 접두사로 시작하지 않는 속성만 제외하려면 `whereDoesntStartWith`를 사용하세요:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` 메서드로 attribute bag에서 첫 번째 속성만 출력할 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

특정 속성의 존재 유무는 `has` 메서드로 확인할 수 있습니다(배열로 주면 모두 존재할 때만 true):

```blade
@if ($attributes->has('class'))
    <div>Class 속성이 있습니다</div>
@endif

@if ($attributes->has(['name', 'class']))
    <div>모든 속성이 있습니다</div>
@endif
```

`hasAny` 메서드는 여러 속성 중 하나라도 있으면 true를 반환합니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>속성 중 하나 이상이 존재합니다</div>
@endif
```

특정 속성 값을 가져오려면 `get` 메서드를 사용합니다:

```blade
{{ $attributes->get('class') }}
```

지정한 키만 추출하려면 `only`를, 특정 키를 제외하고 추출하려면 `except`를 사용하세요:

```blade
{{ $attributes->only(['class']) }}
{{ $attributes->except(['class']) }}
```

<a name="reserved-keywords"></a>
### 예약어

아래 키워드는 Blade 내부적으로 사용되므로, 컴포넌트 public 속성이나 메서드명으로 사용할 수 없습니다:

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
### 슬롯

컴포넌트에 추가적인 콘텐츠를 전달하려면 "슬롯"을 사용할 수 있습니다. 컴포넌트에는 `$slot` 변수를 에코해서 표시할 수 있습니다. 예시로, `alert` 컴포넌트가 아래와 같이 구현되어 있다고 가정합니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

슬롯에 내용 전달 예시:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

여러 개의 슬롯이 필요한 경우, 명시적으로 이름을 붙여서 여러 위치에 삽입할 수 있습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

명명된 슬롯 내용 전송 예시:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

슬롯이 비어있는지 확인하려면 `isEmpty` 메서드를 사용할 수 있습니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        이곳은 슬롯이 비어있을 경우의 기본 내용입니다.
    @else
        {{ $slot }}
    @endif
</div>
```

또한, 실제 HTML 주석 이외의 "진짜" 콘텐츠가 포함되어 있는지 `hasActualContent`로 확인할 수도 있습니다:

```blade
@if ($slot->hasActualContent())
    슬롯에 주석 외의 내용이 있습니다.
@endif
```

<a name="scoped-slots"></a>
#### 스코프 슬롯

Vue 등 프레임워크에서 익숙한 "스코프 슬롯"처럼, 슬롯 내부에서 컴포넌트의 데이터나 메서드에 접근하고 싶다면, public 메서드·속성을 정의한 후 슬롯에서 `$component` 변수로 접근할 수 있습니다:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
#### 슬롯 속성

Blade 컴포넌트처럼, 슬롯에도 [속성](#component-attributes)(예: CSS 클래스)을 부여할 수 있습니다:

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

슬롯 속성과 상호작용하고 싶을 때는 해당 슬롯 변수의 `attributes` 프로퍼티를 통해 접근합니다. 더 자세한 방법은 [컴포넌트 속성](#component-attributes) 문서를 참고하세요:

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
### 인라인 컴포넌트 뷰

아주 작은 규모의 컴포넌트라면, 컴포넌트 클래스와 뷰 템플릿을 별도로 관리하지 않고, `render` 메서드에서 바로 마크업을 반환할 수도 있습니다:

```php
/**
 * 컴포넌트의 뷰/콘텐츠 반환.
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
#### 인라인 뷰 컴포넌트 생성

인라인 뷰를 렌더링하는 컴포넌트를 Artisan으로 생성하려면 `inline` 옵션을 추가해 명령을 실행하세요:

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 동적 컴포넌트

런타임 때까지 렌더할 컴포넌트가 정해지지 않는 경우, Laravel의 내장 `dynamic-component`를 활용해 변수로 컴포넌트를 렌더할 수 있습니다:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 아래 컴포넌트 수동 등록 문서는 주로 Laravel 패키지를 직접 작성할 때 유효합니다. 일반 애플리케이션에서는 생략 가능합니다.

애플리케이션에서는 컴포넌트가 디렉터리 기준으로 자동 감지되나, 패키지나 관례와 다른 위치에 컴포넌트를 보관할 경우, 서비스 프로바이더의 `boot` 메서드에서 컴포넌트 클래스와 태그 별칭을 직접 등록해야 합니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

등록 후에는 태그 별칭을 사용해 아래처럼 사용할 수 있습니다:

```blade
<x-package-alert/>
```

#### 패키지 컴포넌트 오토로드

또한, `componentNamespace` 메서드로 패키지 내의 컴포넌트를 네임스페이스별로 오토로드할 수 있습니다. 예:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 패키지 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

이렇게 하면 아래와 같이 네임스페이스를 접두사로 써서 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade는 컴포넌트 이름을 파스칼 케이스로 맞춰 해당 클래스를 자동 탐지합니다. 서브디렉터리는 "dot" 표기법을 사용할 수 있습니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트 (Anonymous Components)

인라인 컴포넌트와 비슷하지만, 익명 컴포넌트는 단일 Blade 파일만으로 컴포넌트를 관리합니다(클래스 없음). 단순히 `resources/views/components` 디렉터리에 Blade 템플릿을 두고, 아래처럼 간단하게 사용할 수 있습니다:

```blade
<x-alert/>
```

더 깊은 디렉터리 구조에서는 `.`(점) 표기법으로 컴포넌트를 사용할 수 있습니다. 즉, `resources/views/components/inputs/button.blade.php`라면:

```blade
<x-inputs.button/>
```

Artisan을 사용할 때는 `--view` 플래그를 추가해 익명 컴포넌트를 생성합니다:

```shell
php artisan make:component forms.input --view
```

이 명령어는 `resources/views/components/forms/input.blade.php` 파일을 만들어 `<x-forms.input />` 식으로 사용할 수 있습니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

큰 컴포넌트가 여러 Blade 템플릿으로 구성된 경우, 해당 컴포넌트와 관련된 템플릿을 한 디렉터리에 모으고 싶을 수 있습니다. 예를 들어, "accordion" 컴포넌트 디렉터리 구조가:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

처럼 구성되어 있다면, 다음처럼 사용 가능합니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

하지만 `<x-accordion>`처럼 바로 사용하려면 인덱스("accordion.blade.php") 파일을 `components` 하위가 아니라 `accordion` 디렉터리 내부에 "accordion.blade.php"로 위치시켜야 더 직관적인 디렉터리 구성을 할 수 있습니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### 데이터 속성 / 속성(attributes)

익명 컴포넌트에는 연결된 클래스가 없으므로, 어떤 속성이 변수로 전달되어야 하는지 지정하려면 컴포넌트 Blade 템플릿 상단에 `@props` 지시어를 사용해야 합니다. 기본값이 필요하다면 배열 키에 변수명, 값에 기본값을 할당하세요:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

이런 컴포넌트를 아래처럼 사용할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 부모 데이터 접근하기

자식 컴포넌트에서 부모 컴포넌트의 데이터를 사용하고 싶을 때는 `@aware` 지시어를 쓸 수 있습니다. 예를 들어, `<x-menu>`와 `<x-menu.item>` 관계일 때:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

부모에서 색상 속성 정의:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

하지만 이 color 속성이 자식에서는 보이지 않기 때문에, 아래처럼 `@aware`로 color 값을 자식에 노출시킬 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` 지시어는 HTML 속성으로 부모에게 명시적으로 전달된 값만 접근할 수 있습니다. 부모의 `@props` 기본값 중 전달되지 않은 값에는 접근할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

기본적으로 익명 컴포넌트는 `resources/views/components` 디렉터리에 두지만, 원하는 위치에 다른 익명 컴포넌트 경로를 Laravel에 등록할 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인자로 경로, 두 번째 인자로 네임스페이스(옵션)를 받으며, 보통 애플리케이션 [서비스 프로바이더](/docs/12.x/providers)에서 호출합니다:

```php
/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

특정 프리픽스를 붙이지 않으면, 해당 경로 아래의 컴포넌트는 그대로 불러올 수 있습니다:

```blade
<x-panel />
```

두 번째 인자로 프리픽스 네임스페이스를 지정할 수도 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

이렇게 하면 해당 네임스페이스로 접두어를 붙여 사용할 수 있습니다:

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 레이아웃 구성하기 (Building Layouts)

<a name="layouts-using-components"></a>
### 컴포넌트로 레이아웃 구성

웹 애플리케이션은 여러 페이지에서 동일한 레이아웃을 사용하는 경우가 많습니다. 모든 뷰마다 동일한 레이아웃 HTML을 반복 작성하는 것은 상당히 비효율적이고 관리가 어렵습니다. 다행히 Blade에서는 [컴포넌트](#components)로 레이아웃을 손쉽게 지정하고 프로젝트 전반에서 재사용할 수 있습니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어 "todo" 리스트 애플리케이션을 만든다고 할 때, 다음과 같이 `layout` 컴포넌트를 정의할 수 있습니다:

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
#### 레이아웃 컴포넌트 적용

`layout` 컴포넌트가 완성되면, 아래처럼 이를 활용하는 Blade 뷰를 만들 수 있습니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```

컴포넌트로 주입된 콘텐츠는 `layout` 컴포넌트 내부의 기본 `$slot` 변수로 전달됩니다. 또한, 뷰에서 `$title` 슬롯을 지정하면 자체 제목을 적용할 수 있습니다. 슬롯 구문은 [컴포넌트 문서](#components)에서 언급한 형태를 따릅니다:

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

이제 라우트에서 `tasks` 뷰를 반환하면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속으로 레이아웃 구성

<a name="defining-a-layout"></a>
#### 레이아웃 정의

"템플릿 상속"으로도 레이아웃을 구성할 수 있습니다. 이는 [컴포넌트](#components) 도입 이전에 Laravel에서 주로 사용된 방식입니다.

예를 들어, 아래처럼 공통 레이아웃을 정의합니다:

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

이 레이아웃에는 자주 사용되는 HTML 코드와 함께 `@section`, `@yield` 지시어가 포함되어 있습니다. `@section`은 해당 내용을 정의하고, `@yield`는 섹션의 내용을 표시합니다.

자, 이제 이 레이아웃을 상속하는 자식 페이지를 정의해보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

자식 뷰에서는 `@extends` 지시어로 상속받을 레이아웃을 지정합니다. 그리고 `@section` 지시어를 활용해 부모 레이아웃의 각 섹션에 콘텐츠를 삽입할 수 있습니다:

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

이 예제에서 `sidebar` 섹션은 `@@parent` 지시어로 부모의 sidebar 내용 뒤에 추가됩니다. 뷰가 렌더링될 때, `@@parent` 자리가 레이아웃의 기존 sidebar 내용으로 대체됩니다.

> [!NOTE]
> 앞선 예시와 달리, 이 `sidebar` 섹션은 `@endsection`으로 끝나며, `@show`가 아닙니다. `@endsection`은 섹션만 정의하고, `@show`는 정의와 동시에 **즉시 표시**합니다.

`@yield` 지시어는 두 번째 인자로 기본값을 받을 수 있습니다. 해당 섹션이 정의되지 않았다면 기본값이 표시됩니다:

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## 폼 (Forms)

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때는 [CSRF 보호](/docs/12.x/csrf) 미들웨어가 요청을 검증할 수 있도록 숨겨진 CSRF 토큰 필드를 꼭 포함해야 합니다. `@csrf` Blade 지시어로 토큰 필드를 쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### Method 필드

HTML 폼은 `PUT`, `PATCH`, `DELETE` 요청을 보낼 수 없으므로, 해당 HTTP 동사를 흉내 내기 위해 숨겨진 `_method` 필드를 추가해야 합니다. `@method` Blade 지시어로 쉽게 생성할 수 있습니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 유효성 검증 에러

`@error` 지시어는 [유효성 검증 에러 메시지](/docs/12.x/validation#quick-displaying-the-validation-errors)가 특정 속성에 존재하는지 빠르게 확인할 수 있습니다. `@error` 지시어 블록 내에서 `$message` 변수를 사용해 에러 메시지를 표시할 수 있습니다:

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

`@error`는 내부적으로 "if"문으로 컴파일되기 때문에, `@else` 지시어로 에러가 없을 때의 처리를 할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```

여러 개의 폼이 있는 페이지 등에서 [특정 이름의 에러 bag](/docs/12.x/validation#named-error-bags)에 해당하는 유효성 검증 에러 메시지를 얻으려면 두 번째 인자로 에러 bag 이름을 넣습니다:

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
## 스택 (Stacks)

Blade에서는 명명된 "스택"에 콘텐츠를 푸시하고, 이를 다른 뷰나 레이아웃에서 어디든 렌더링할 수 있습니다. 주로 자식 뷰에서 필요한 JavaScript 라이브러리를 포함할 때 유용합니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

특정 조건이 참일 때만 `@push`하고 싶으면, `@pushIf`를 사용할 수 있습니다:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

하나의 스택에 여러 번 `@push`할 수 있습니다. 스택 전체 내용을 표시할 땐 `@stack` 지시어에 스택명을 넣으세요:

```blade
<head>
    <!-- Head 내용 -->

    @stack('scripts')
</head>
```

스택 맨 앞에 콘텐츠를 추가하려면 `@prepend`를 사용하세요:

```blade
@push('scripts')
    이것이 두 번째...
@endpush

// 이후에...

@prepend('scripts')
    이것이 첫 번째...
@endprepend
```

스택이 비어 있는지 확인하려면 `@hasstack` 지시어를 사용할 수 있습니다:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```

<a name="service-injection"></a>
## 서비스 의존성 주입 (Service Injection)

`@inject` 지시어로 Laravel의 [서비스 컨테이너](/docs/12.x/container)에서 서비스를 주입받을 수 있습니다. 첫 번째 인자는 변수명, 두 번째 인자는 주입할 클래스 또는 인터페이스입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## 인라인 블레이드 템플릿 렌더링

종종, Blade 템플릿 문자열을 HTML로 변환해야 할 수도 있습니다. 이때 `Blade` 파사드의 `render` 메서드를 활용할 수 있습니다. Blade 템플릿 문자열, 데이터 배열을 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel은 임시로 렌더링할 Blade 파일을 `storage/framework/views`에 저장합니다. 렌더 후 임시 파일을 삭제하려면 `deleteCachedView` 인수를 지정하세요:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## 블레이드 프래그먼트 렌더링

[Tubro](https://turbo.hotwired.dev/), [htmx](https://htmx.org/)와 같은 프론트엔드 프레임워크를 사용할 때, Blade 템플릿 일부만 HTTP 응답으로 반환하고 싶을 때가 있습니다. 이럴 때 "fragments" 기능을 사용할 수 있습니다. 템플릿에서 `@fragment`와 `@endfragment`로 영역을 감싸세요:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

이후, 해당 뷰를 렌더링할 때 `fragment` 메서드로 응답에 포함할 프래그먼트만 지정할 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

불린 조건에 따라 특정 프래그먼트만 반환하고 그렇지 않으면 전체 뷰를 출력하려면 `fragmentIf`를 사용하세요:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

`fragments` 및 `fragmentsIf` 메서드로 여러 개의 프래그먼트를 한 번에 반환할 수도 있습니다. 반환된 프래그먼트는 합쳐져서 출력됩니다:

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
## 블레이드 확장하기 (Extending Blade)

Blade에서는 `directive` 메서드로 커스텀 지시어를 정의할 수 있습니다. Blade 컴파일러가 커스텀 지시어를 만나면, 해당 지시어가 담고 있는 표현식을 콜백에 전달합니다.

아래는 `@datetime($var)`라는 지시어를 만드는 예시입니다. `$var`는 `DateTime` 인스턴스여야 하며, 지정된 형식대로 값을 표시합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

위 예시는 입력값에 `format` 메서드를 체이닝합니다. 실제로는 아래와 같은 PHP가 생성됩니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> 커스텀 Blade 지시어 로직을 수정한 뒤에는 모든 캐시된 Blade 뷰를 삭제해야 합니다. `view:clear` Artisan 명령어로 캐시를 삭제할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 커스텀 에코 핸들러

Blade에서 객체를 "에코"하면 해당 객체의 `__toString` 메서드가 호출됩니다. 하지만, 제어권이 없는(외부 라이브러리의) 클래스에서는 `__toString`을 수정할 수 없습니다.

이런 경우 Blade의 `stringable` 메서드로 객체 타입별 커스텀 에코 핸들러를 등록할 수 있습니다. 이 메서드는 클로저를 받으며, 처리할 객체 타입을 타입힌트로 명시하면 됩니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 사용합니다:

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

등록 후, Blade 템플릿에서는 해당 객체를 그냥 에코하면 됩니다:

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### 커스텀 If 문

간단한 조건문을 위해 복잡한 커스텀 지시어를 만드는 것이 부담스럽다면, Blade의 `Blade::if` 메서드로 클로저 기반의 조건식 지시어를 손쉽게 정의할 수 있습니다. 예를 들어, 애플리케이션의 기본 "disk"가 특정 값인지 확인하려면, `AppServiceProvider`에서 아래처럼 선언하세요:

```php
use Illuminate\Support\Facades\Blade;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

이제 아래처럼 커스텀 조건문을 템플릿에서 바로 사용할 수 있습니다:

```blade
@disk('local')
    <!-- 애플리케이션이 local 디스크 사용 중... -->
@elsedisk('s3')
    <!-- 애플리케이션이 s3 디스크 사용 중... -->
@else
    <!-- 애플리케이션이 다른 디스크 사용 중... -->
@enddisk

@unlessdisk('local')
    <!-- 애플리케이션이 local 디스크가 아님... -->
@enddisk
```