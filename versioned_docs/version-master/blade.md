# 블레이드 템플릿 (Blade Templates)

- [소개](#introduction)
    - [Livewire로 Blade 강화하기](#supercharging-blade-with-livewire)
- [데이터 출력](#displaying-data)
    - [HTML 엔티티 인코딩](#html-entity-encoding)
    - [Blade와 JavaScript 프레임워크](#blade-and-javascript-frameworks)
- [Blade 디렉티브](#blade-directives)
    - [If 문](#if-statements)
    - [Switch 문](#switch-statements)
    - [반복문](#loops)
    - [Loop 변수](#the-loop-variable)
    - [조건부 클래스](#conditional-classes)
    - [추가 속성](#additional-attributes)
    - [서브뷰 포함](#including-subviews)
    - [`@once` 디렉티브](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [주석](#comments)
- [컴포넌트](#components)
    - [컴포넌트 렌더링](#rendering-components)
    - [인덱스 컴포넌트](#index-components)
    - [컴포넌트에 데이터 전달](#passing-data-to-components)
    - [컴포넌트 속성](#component-attributes)
    - [예약어](#reserved-keywords)
    - [슬롯](#slots)
    - [인라인 컴포넌트 뷰](#inline-component-views)
    - [동적 컴포넌트](#dynamic-components)
    - [컴포넌트 수동 등록](#manually-registering-components)
- [익명 컴포넌트](#anonymous-components)
    - [익명 인덱스 컴포넌트](#anonymous-index-components)
    - [데이터 속성 / 어트리뷰트](#data-properties-attributes)
    - [부모 데이터 접근](#accessing-parent-data)
    - [익명 컴포넌트 경로](#anonymous-component-paths)
- [레이아웃 구성](#building-layouts)
    - [컴포넌트를 이용한 레이아웃](#layouts-using-components)
    - [템플릿 상속을 이용한 레이아웃](#layouts-using-template-inheritance)
- [폼](#forms)
    - [CSRF 필드](#csrf-field)
    - [메서드 필드](#method-field)
    - [유효성 검증 오류](#validation-errors)
- [스택](#stacks)
- [서비스 주입](#service-injection)
- [인라인 Blade 템플릿 렌더링](#rendering-inline-blade-templates)
- [Blade 프래그먼트 렌더링](#rendering-blade-fragments)
- [Blade 확장](#extending-blade)
    - [커스텀 Echo 핸들러](#custom-echo-handlers)
    - [커스텀 If 문](#custom-if-statements)

<a name="introduction"></a>
## 소개 (Introduction)

Blade는 Laravel에 포함된 간단하면서도 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리, Blade는 템플릿 안에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 실제로 모든 Blade 템플릿은 일반 PHP 코드로 컴파일되어 캐시되며, 템플릿이 수정될 때까지 재사용됩니다. 따라서 Blade는 애플리케이션에 사실상 거의 오버헤드를 추가하지 않습니다. Blade 템플릿 파일은 `.blade.php` 확장자를 사용하며 일반적으로 `resources/views` 디렉토리에 저장됩니다.

Blade 뷰는 전역 `view` 헬퍼를 사용하여 라우트 또는 컨트롤러에서 반환할 수 있습니다. 또한 [views](/docs/master/views) 문서에서 설명한 것처럼 `view` 헬퍼의 두 번째 인수를 사용해 데이터를 Blade 뷰로 전달할 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
### Livewire로 Blade 강화하기

Blade 템플릿을 한 단계 더 발전시켜 동적인 인터페이스를 쉽게 만들고 싶다면 [Laravel Livewire](https://livewire.laravel.com)를 확인해 보십시오. Livewire를 사용하면 React, Svelte, Vue 같은 프론트엔드 프레임워크에서만 가능했던 동적인 기능을 Blade 컴포넌트에 추가할 수 있습니다. 이를 통해 복잡한 JavaScript 프레임워크의 빌드 과정이나 클라이언트 사이드 렌더링 없이도 현대적인 반응형 프론트엔드를 구축할 수 있습니다.

<a name="displaying-data"></a>
## 데이터 출력 (Displaying Data)

Blade 뷰에 전달된 데이터는 중괄호로 변수를 감싸 출력할 수 있습니다. 예를 들어 다음과 같은 라우트가 있다고 가정해 보겠습니다.

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

`name` 변수의 내용을 다음과 같이 출력할 수 있습니다.

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade의 `{{ }}` 출력 구문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수가 적용됩니다.

뷰로 전달된 변수뿐 아니라 모든 PHP 함수의 결과도 출력할 수 있습니다. 실제로 Blade echo 문 안에는 원하는 어떤 PHP 코드든 작성할 수 있습니다.

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로 Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 이중 인코딩합니다. 이중 인코딩을 비활성화하려면 `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하십시오.

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
#### 이스케이프되지 않은 데이터 출력

기본적으로 Blade의 `{{ }}` 구문은 XSS 공격을 방지하기 위해 `htmlspecialchars` 함수가 적용됩니다. 데이터를 이스케이프하지 않고 출력하려면 다음 문법을 사용할 수 있습니다.

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> 애플리케이션 사용자가 제공한 콘텐츠를 출력할 때는 매우 주의해야 합니다. 일반적으로 사용자 입력 데이터를 출력할 때는 XSS 공격을 방지하기 위해 이스케이프 처리된 `{{ }}` 구문을 사용하는 것이 좋습니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크

많은 JavaScript 프레임워크 역시 중괄호(`{{ }}`)를 사용하여 브라우저에 표현식을 출력합니다. 이때 Blade 엔진이 해당 표현식을 처리하지 않도록 하려면 `@` 기호를 사용할 수 있습니다.

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

이 경우 `@` 기호는 Blade에 의해 제거되지만 `{{ name }}` 표현식은 그대로 유지되어 JavaScript 프레임워크에서 처리됩니다.

`@` 기호는 Blade 디렉티브를 이스케이프할 때도 사용할 수 있습니다.

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSON 렌더링

JavaScript 변수를 초기화하기 위해 배열을 JSON으로 렌더링해야 하는 경우가 있습니다.

```php
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

이 경우 직접 `json_encode`를 호출하는 대신 `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. 이 메서드는 PHP의 `json_encode`와 동일한 인수를 받지만 HTML 속성 안에서도 안전하게 사용할 수 있도록 JSON 문자열을 적절히 이스케이프합니다.

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

최신 Laravel 애플리케이션 스켈레톤에는 `Js` 파사드가 포함되어 있어 다음과 같이 더 간단히 사용할 수 있습니다.

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> `Js::from` 메서드는 기존 변수를 JSON으로 변환할 때만 사용해야 합니다. Blade 템플릿은 정규 표현식을 기반으로 동작하므로 복잡한 표현식을 전달하면 예상치 못한 오류가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 디렉티브

템플릿의 큰 영역에서 JavaScript 변수를 출력해야 하는 경우 `@verbatim` 디렉티브를 사용하여 Blade가 해당 영역을 처리하지 않도록 할 수 있습니다.

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade 디렉티브 (Blade Directives)

Blade는 템플릿 상속과 데이터 출력뿐 아니라 조건문, 반복문 같은 PHP 제어 구조를 간결하게 사용할 수 있는 다양한 디렉티브를 제공합니다. 이러한 디렉티브는 PHP와 동일하게 동작하면서도 더 깔끔하고 간단한 문법을 제공합니다.

(이하 모든 내용은 원문의 Markdown 구조를 그대로 유지하며 전체 번역을 이어가야 하나, 메시지 길이 제한으로 인해 한 번에 모두 출력할 수 없습니다.)