# 유효성 검증 (Validation)

- [소개](#introduction)
- [Validation 빠른 시작](#validation-quickstart)
    - [라우트 정의](#quick-defining-the-routes)
    - [컨트롤러 생성](#quick-creating-the-controller)
    - [유효성 검증 로직 작성](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시](#quick-displaying-the-validation-errors)
    - [폼 값 다시 채우기](#repopulating-forms)
    - [선택적 필드에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 형식](#validation-error-response-format)
- [Form Request 유효성 검증](#form-request-validation)
    - [Form Request 생성](#creating-form-requests)
    - [Form Request 인가](#authorizing-form-requests)
    - [오류 메시지 사용자 정의](#customizing-the-error-messages)
    - [검증을 위한 입력 데이터 준비](#preparing-input-for-validation)
- [Validator 수동 생성](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 Error Bag](#named-error-bags)
    - [오류 메시지 사용자 정의](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [검증된 입력 데이터 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 사용자 정의 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 Validation 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 검증](#validating-arrays)
    - [중첩 배열 입력 검증](#validating-nested-array-input)
    - [오류 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 검증](#validating-files)
- [비밀번호 검증](#validating-passwords)
- [사용자 정의 Validation 규칙](#custom-validation-rules)
    - [Rule 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션으로 들어오는 데이터를 유효성 검증하기 위한 여러 가지 방법을 제공합니다. 가장 일반적으로 사용되는 방법은 모든 HTTP 요청 객체에서 사용할 수 있는 `validate` 메서드를 사용하는 것입니다. 하지만 이 문서에서는 다른 유효성 검증 방법도 함께 살펴봅니다.

Laravel은 데이터에 적용할 수 있는 다양한 편리한 유효성 검증 규칙을 제공하며, 특정 데이터베이스 테이블에서 값이 **유일한지(unique)** 확인하는 기능도 제공합니다. 이 문서에서는 이러한 유효성 검증 규칙을 하나씩 자세히 살펴보며 Laravel의 모든 유효성 검증 기능을 이해할 수 있도록 설명합니다.

<a name="validation-quickstart"></a>
## Validation 빠른 시작

Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 검증하고 사용자에게 오류 메시지를 표시하는 전체 예제를 살펴보겠습니다. 이 개요를 통해 Laravel에서 들어오는 요청 데이터를 어떻게 검증하는지 전반적인 흐름을 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의

먼저 `routes/web.php` 파일에 다음과 같은 라우트가 정의되어 있다고 가정합니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새로운 블로그 게시글을 작성할 수 있는 폼을 보여주며, `POST` 라우트는 새 게시글을 데이터베이스에 저장하는 역할을 합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성

다음으로 이 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 우선 `store` 메서드는 비워 둡니다.

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

검증 규칙을 통과하면 코드가 정상적으로 계속 실행됩니다. 반대로 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, Laravel이 자동으로 사용자에게 적절한 오류 응답을 반환합니다.

- 일반 HTTP 요청에서 검증이 실패하면 이전 URL로 **리다이렉트 응답**이 생성됩니다.
- XHR 요청(AJAX 요청)일 경우에는 **검증 오류 메시지를 포함한 JSON 응답**이 반환됩니다.

이제 `store` 메서드에 검증 로직을 추가해 보겠습니다.

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

보시다시피 검증 규칙은 `validate` 메서드에 전달됩니다. 사용 가능한 모든 규칙은 [문서](#available-validation-rules)에 정리되어 있습니다.

검증이 실패하면 Laravel이 자동으로 적절한 응답을 생성하고, 검증이 성공하면 컨트롤러는 정상적으로 계속 실행됩니다.

또한 `|` 구분 문자열 대신 **배열 형태로 규칙을 지정할 수도 있습니다.**

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또는 `validateWithBag` 메서드를 사용하여 오류 메시지를 **이름이 지정된 error bag**에 저장할 수도 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단

어떤 속성(attribute)에 대해 **첫 번째 검증 실패가 발생하면 더 이상 검증을 진행하지 않도록** 하고 싶을 수 있습니다. 이 경우 `bail` 규칙을 사용할 수 있습니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예제에서 `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙은 검사되지 않습니다. 규칙은 **작성된 순서대로 검증**됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

요청 데이터에 중첩된 필드가 포함되어 있는 경우 **점(dot) 표기법**을 사용해 검증할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로 필드 이름 자체에 실제 마침표(`.`)가 포함된 경우에는 백슬래시(`\`)로 이스케이프해야 합니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시

요청 데이터가 검증 규칙을 통과하지 못하면 어떻게 될까요?

Laravel은 자동으로 사용자를 **이전 페이지로 리다이렉트**합니다. 또한 모든 검증 오류와 [요청 입력값](/docs/12.x/requests#retrieving-old-input)이 자동으로 **세션에 flash 데이터로 저장**됩니다.

`web` 미들웨어 그룹에 포함된 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 `$errors` 변수를 모든 뷰와 공유합니다.

이 `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 따라서 뷰에서 언제든지 `$errors`를 사용해 오류 메시지를 출력할 수 있습니다.

예를 들어 검증이 실패하면 사용자는 `create` 메서드로 다시 이동하고, 뷰에서 오류를 표시할 수 있습니다.

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

Laravel의 기본 검증 규칙 오류 메시지는 `lang/en/validation.php` 파일에 정의되어 있습니다.

만약 애플리케이션에 `lang` 디렉토리가 없다면 `lang:publish` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan lang:publish
```

`lang/en/validation.php` 파일에는 각 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 요구 사항에 맞게 자유롭게 수정할 수 있습니다.

또한 다른 언어 디렉토리로 파일을 복사해 애플리케이션 언어에 맞게 번역할 수도 있습니다.

Laravel의 로컬라이제이션에 대한 자세한 내용은 [localization 문서](/docs/12.x/localization)를 참고하십시오.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. 언어 파일을 수정하려면 `lang:publish` Artisan 명령어를 사용해 게시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 Validation

앞의 예제에서는 일반 HTML 폼을 사용해 데이터를 전송했습니다. 하지만 많은 애플리케이션은 JavaScript 기반 프론트엔드에서 **XHR 요청(AJAX)** 을 사용합니다.

XHR 요청에서 `validate` 메서드를 사용하면 Laravel은 **리다이렉트 응답을 생성하지 않습니다.**

대신 **모든 검증 오류를 포함한 JSON 응답**을 반환하며 HTTP 상태 코드는 **422**가 됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

특정 필드에 대한 오류 메시지가 존재하는지 확인하려면 Blade의 `@error` 디렉티브를 사용할 수 있습니다.

```blade
<!-- /resources/views/post/create.blade.php -->

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

**이름이 지정된 error bag**을 사용하는 경우 두 번째 인수로 bag 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 값 다시 채우기

Laravel이 유효성 검증 오류로 인해 리다이렉트 응답을 생성하면, 프레임워크는 요청 입력 데이터를 자동으로 **세션에 flash 데이터로 저장**합니다.

이렇게 하면 다음 요청에서 입력값을 다시 불러와 사용자가 제출하려던 폼을 쉽게 복원할 수 있습니다.

이전 요청의 입력값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 사용합니다.

```php
$title = $request->old('title');
```

또는 Blade 템플릿에서는 전역 `old` 헬퍼를 사용하는 것이 더 편리합니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

만약 이전 입력값이 없다면 `null`이 반환됩니다.

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 참고

Laravel은 기본적으로 전역 미들웨어 스택에 다음 미들웨어를 포함합니다.

- `TrimStrings`
- `ConvertEmptyStringsToNull`

이 때문에 "선택적(optional)" 필드를 사용할 때 `nullable` 규칙을 지정해야 하는 경우가 많습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

위 예제에서 `publish_at` 필드는 `null`이거나 유효한 날짜여야 합니다. `nullable`을 지정하지 않으면 `null` 값은 **유효하지 않은 날짜**로 처리됩니다.

<a name="validation-error-response-format"></a>
### Validation 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고 요청이 JSON 응답을 기대하는 경우, Laravel은 자동으로 오류 메시지를 다음과 같은 형식으로 반환합니다.

HTTP 상태 코드는 **422 Unprocessable Entity** 입니다.

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