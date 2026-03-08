# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의](#quick-defining-the-routes)
    - [컨트롤러 생성](#quick-creating-the-controller)
    - [유효성 검증 로직 작성](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시](#quick-displaying-the-validation-errors)
    - [폼 입력 값 다시 채우기](#repopulating-forms)
    - [선택적 필드에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 형식](#validation-error-response-format)
- [Form Request 유효성 검증](#form-request-validation)
    - [Form Request 생성](#creating-form-requests)
    - [Form Request 인가](#authorizing-form-requests)
    - [오류 메시지 사용자 정의](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력 준비](#preparing-input-for-validation)
- [Validator 수동 생성](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 Error Bag](#named-error-bags)
    - [오류 메시지 사용자 정의](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [검증된 입력 데이터 사용](#working-with-validated-input)
- [오류 메시지 처리](#working-with-error-messages)
    - [언어 파일에서 사용자 정의 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 이름 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력 유효성 검증](#validating-nested-array-input)
    - [오류 메시지 인덱스 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [사용자 정의 유효성 검증 규칙](#custom-validation-rules)
    - [Rule 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터를 검증하기 위해 여러 가지 접근 방식을 제공합니다. 가장 일반적으로는 모든 HTTP 요청 객체에서 사용할 수 있는 `validate` 메서드를 사용하는 방식입니다. 하지만 이 문서에서는 다른 유효성 검증 방법들도 함께 살펴봅니다.

Laravel에는 데이터를 검증하기 위한 다양한 편리한 유효성 검증 규칙이 포함되어 있으며, 특정 데이터베이스 테이블에서 값이 **고유한지(unique)** 확인하는 기능도 제공합니다. 이 문서에서는 이러한 유효성 검증 규칙을 하나씩 자세히 살펴보며 Laravel의 유효성 검증 기능을 전반적으로 이해할 수 있도록 설명합니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼 데이터를 검증하고 오류 메시지를 사용자에게 표시하는 전체 예제를 살펴보겠습니다. 이 개요를 통해 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 전반적인 흐름을 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의

먼저 `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정해 보겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새로운 블로그 게시글을 작성할 수 있는 폼을 표시하고, `POST` 라우트는 새 블로그 게시글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성

다음으로 이 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 지금은 `store` 메서드를 비워 둡니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate and store the blog post...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
### 유효성 검증 로직 작성

이제 `store` 메서드에 새 블로그 게시글을 검증하는 로직을 추가해 보겠습니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다.

검증 규칙을 통과하면 코드가 정상적으로 계속 실행됩니다. 반대로 검증이 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청에서 검증이 실패하면 이전 URL로 리다이렉트됩니다. 요청이 XHR 요청이라면 [유효성 검증 오류 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

다음은 `store` 메서드에서 `validate` 메서드를 사용하는 예시입니다.

```php
/**
 * Store a new blog post.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // The blog post is valid...

    return redirect('/posts');
}
```

위 코드에서 볼 수 있듯이, 유효성 검증 규칙은 `validate` 메서드에 전달됩니다. 모든 유효성 검증 규칙은 [문서](#available-validation-rules)에 정리되어 있습니다.

검증이 실패하면 적절한 응답이 자동으로 생성됩니다. 검증이 성공하면 컨트롤러 로직이 정상적으로 계속 실행됩니다.

유효성 검증 규칙은 `|` 구분 문자열 대신 배열 형태로도 작성할 수 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한 `validateWithBag` 메서드를 사용하면 오류 메시지를 [이름이 지정된 error bag](#named-error-bags)에 저장할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단

특정 속성에 대해 첫 번째 검증 실패가 발생하면 이후 규칙 검사를 중단하고 싶을 때가 있습니다. 이 경우 `bail` 규칙을 사용합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예제에서는 `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙은 검사되지 않습니다. 규칙은 지정된 순서대로 실행됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성(Nested Attributes)에 대한 참고

HTTP 요청 데이터에 중첩된 필드가 포함되어 있다면, 유효성 검증 규칙에서 **점 표기법(dot syntax)** 을 사용할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

필드 이름 자체에 실제 점(`.`) 문자가 포함되어 있다면, 백슬래시로 이스케이프하여 점 표기법으로 해석되지 않도록 할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시

요청 데이터가 검증 규칙을 통과하지 못하면 어떻게 될까요?

앞서 설명한 것처럼 Laravel은 사용자를 자동으로 이전 페이지로 리다이렉트합니다. 또한 모든 유효성 검증 오류와 [요청 입력 값](/docs/master/requests#retrieving-old-input)이 자동으로 [세션에 flash](/docs/master/session#flash-data)됩니다.

`web` 미들웨어 그룹에 포함된 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 모든 뷰에서 사용할 수 있도록 `$errors` 변수를 공유합니다.

따라서 뷰에서는 `$errors` 변수가 항상 존재한다고 가정하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다.

다음은 오류 메시지를 표시하는 예시입니다.

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>Create Post</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```

<a name="quick-customizing-the-error-messages"></a>
#### 오류 메시지 사용자 정의

Laravel의 기본 유효성 검증 규칙은 각각 오류 메시지를 가지고 있으며, 이는 `lang/en/validation.php` 파일에 정의되어 있습니다.

애플리케이션에 `lang` 디렉토리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan lang:publish
```

`lang/en/validation.php` 파일에는 각 유효성 검증 규칙에 대한 번역 항목이 존재하며, 애플리케이션 요구사항에 맞게 자유롭게 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉토리로 복사하여 애플리케이션 언어에 맞게 번역할 수도 있습니다.

자세한 내용은 [Localization 문서](/docs/master/localization)를 참고하십시오.

> [!WARNING]
> 기본 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용하여 게시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

앞선 예제에서는 일반적인 HTML 폼을 사용했습니다. 하지만 많은 애플리케이션은 JavaScript 기반 프론트엔드에서 XHR 요청을 보냅니다.

XHR 요청에서 `validate` 메서드를 사용할 경우 Laravel은 리다이렉트 응답을 생성하지 않습니다. 대신 모든 유효성 검증 오류를 포함한 JSON 응답을 반환합니다.

이 응답은 HTTP 상태 코드 `422`와 함께 반환됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 필드에 대한 유효성 검증 오류가 있는지 빠르게 확인하려면 Blade의 `@error` 디렉티브를 사용할 수 있습니다.

```blade
<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

[named error bag](#named-error-bags)을 사용하는 경우 두 번째 인수로 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 입력 값 다시 채우기

유효성 검증 오류로 인해 리다이렉트가 발생하면 Laravel은 요청 입력 데이터를 자동으로 세션에 flash 합니다.

이를 통해 다음 요청에서 이전 입력 값을 쉽게 가져와 사용자가 입력했던 폼 값을 다시 채울 수 있습니다.

이전 요청의 입력 데이터를 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다.

```php
$title = $request->old('title');
```

Laravel은 전역 `old` 헬퍼도 제공합니다. Blade 템플릿에서 사용할 때 더 편리합니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

지정한 필드에 이전 입력 값이 없다면 `null`이 반환됩니다.

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 참고

Laravel은 기본적으로 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 글로벌 미들웨어 스택에 포함합니다.

따라서 선택적(optional) 필드는 `nullable` 규칙을 지정해야 하는 경우가 많습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예제에서는 `publish_at` 필드가 `null`이거나 유효한 날짜 형식이면 통과합니다. `nullable`을 지정하지 않으면 `null` 값은 유효하지 않은 날짜로 간주됩니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고 요청이 JSON 응답을 기대하는 경우, Laravel은 자동으로 오류 메시지를 포맷하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

다음은 유효성 검증 오류 JSON 응답의 예시입니다. 중첩된 키는 **점 표기법(dot notation)** 으로 평탄화됩니다.

```json
{
    "message": "The team name must be a string. (and 4 more errors)",
    "errors": {
        "team_name": [
            "The team name must be a string.",
            "The team name must be at least 1 characters."
        ],
        "authorization.role": [
            "The selected authorization.role is invalid."
        ],
        "users.0.email": [
            "The users.0.email field is required."
        ],
        "users.2.email": [
            "The users.2.email must be a valid email address."
        ]
    }
}
```