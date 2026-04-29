# 유효성 검증 (Validation)

- [소개](#introduction)
- [유효성 검증 빠른 시작](#validation-quickstart)
    - [라우트 정의](#quick-defining-the-routes)
    - [컨트롤러 생성](#quick-creating-the-controller)
    - [유효성 검증 로직 작성](#quick-writing-the-validation-logic)
    - [유효성 검증 오류 표시](#quick-displaying-the-validation-errors)
    - [폼 다시 채우기](#repopulating-forms)
    - [선택적 필드에 대한 참고](#a-note-on-optional-fields)
    - [유효성 검증 오류 응답 형식](#validation-error-response-format)
- [폼 요청 유효성 검증](#form-request-validation)
    - [폼 요청 생성](#creating-form-requests)
    - [폼 요청 인가](#authorizing-form-requests)
    - [오류 메시지 사용자 정의](#customizing-the-error-messages)
    - [유효성 검증을 위한 입력 준비](#preparing-input-for-validation)
- [Validator 수동 생성](#manually-creating-validators)
    - [자동 리다이렉션](#automatic-redirection)
    - [이름이 지정된 오류 백](#named-error-bags)
    - [오류 메시지 사용자 정의](#manual-customizing-the-error-messages)
    - [추가 유효성 검증 수행](#performing-additional-validation)
- [유효성 검증된 입력 다루기](#working-with-validated-input)
- [오류 메시지 다루기](#working-with-error-messages)
    - [언어 파일에서 사용자 정의 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일에서 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에서 값 지정](#specifying-values-in-language-files)
- [사용 가능한 유효성 검증 규칙](#available-validation-rules)
- [조건부로 규칙 추가](#conditionally-adding-rules)
- [배열 유효성 검증](#validating-arrays)
    - [중첩 배열 입력 유효성 검증](#validating-nested-array-input)
    - [오류 메시지 인덱스와 위치](#error-message-indexes-and-positions)
- [파일 유효성 검증](#validating-files)
- [비밀번호 유효성 검증](#validating-passwords)
- [사용자 정의 유효성 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암묵적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션으로 들어오는 데이터를 유효성 검증하기 위한 여러 가지 접근 방식을 제공합니다. 가장 일반적인 방법은 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용하는 것입니다. 하지만 이 외의 유효성 검증 접근 방식도 함께 살펴보겠습니다.

Laravel에는 데이터에 적용할 수 있는 편리한 유효성 검증 규칙이 매우 다양하게 포함되어 있으며, 특정 데이터베이스 테이블에서 값이 고유한지 검증하는 기능도 제공합니다. Laravel의 모든 유효성 검증 기능에 익숙해질 수 있도록 이러한 유효성 검증 규칙을 각각 자세히 다루겠습니다.

<a name="validation-quickstart"></a>
## 유효성 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검증 기능을 알아보기 위해, 폼을 유효성 검증하고 오류 메시지를 사용자에게 다시 표시하는 전체 예제를 살펴보겠습니다. 이 개괄적인 내용을 읽으면 Laravel을 사용해 들어오는 요청 데이터를 유효성 검증하는 방법을 전반적으로 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의

먼저 `routes/web.php` 파일에 다음 라우트가 정의되어 있다고 가정해 보겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 게시물을 작성할 수 있는 폼을 표시하고, `POST` 라우트는 새 블로그 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성

다음으로, 이 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 지금은 `store` 메서드를 비워 두겠습니다.

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

이제 새 블로그 게시물을 유효성 검증하는 로직으로 `store` 메서드를 채울 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드는 정상적으로 계속 실행됩니다. 하지만 유효성 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 오류 응답이 자동으로 사용자에게 다시 전송됩니다.

기존 HTTP 요청 중 유효성 검증에 실패하면 이전 URL로 리다이렉트 응답이 생성됩니다. 들어오는 요청이 XHR 요청이라면 [유효성 검증 오류 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 더 잘 이해하기 위해 `store` 메서드로 다시 돌아가 보겠습니다.

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

보시다시피 유효성 검증 규칙은 `validate` 메서드에 전달됩니다. 걱정하지 않아도 됩니다. 사용 가능한 모든 유효성 검증 규칙은 [문서화](#available-validation-rules)되어 있습니다. 다시 말해, 유효성 검증에 실패하면 적절한 응답이 자동으로 생성됩니다. 유효성 검증을 통과하면 컨트롤러는 정상적으로 계속 실행됩니다.

또는 유효성 검증 규칙을 하나의 `|` 구분 문자열 대신 규칙 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한 `validateWithBag` 메서드를 사용해 요청을 유효성 검증하고, 오류 메시지를 [이름이 지정된 오류 백](#named-error-bags)에 저장할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단

때로는 특정 속성에서 첫 번째 유효성 검증 실패가 발생한 뒤 해당 속성의 나머지 유효성 검증 규칙 실행을 멈추고 싶을 수 있습니다. 그렇게 하려면 해당 속성에 `bail` 규칙을 할당합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예제에서 `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙은 확인되지 않습니다. 규칙은 할당된 순서대로 유효성 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있다면, "점" 문법을 사용해 유효성 검증 규칙에서 해당 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반대로 필드 이름에 실제 마침표가 포함되어 있다면, 마침표 앞에 백슬래시를 붙여 이것이 "점" 문법으로 해석되지 않도록 명시적으로 막을 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 유효성 검증 오류 표시

그렇다면 들어오는 요청 필드가 주어진 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯이 Laravel은 사용자를 자동으로 이전 위치로 리다이렉트합니다. 또한 모든 유효성 검증 오류와 [요청 입력](/docs/13.x/requests#retrieving-old-input)이 자동으로 [세션에 플래시](/docs/13.x/session#flash-data)됩니다.

`$errors` 변수는 `web` 미들웨어 그룹에서 제공하는 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에 의해 애플리케이션의 모든 뷰와 공유됩니다. 이 미들웨어가 적용되면 `$errors` 변수는 항상 뷰에서 사용할 수 있으므로, `$errors` 변수가 항상 정의되어 있고 안전하게 사용할 수 있다고 간편하게 가정할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 방법에 대한 자세한 내용은 [해당 문서](#working-with-error-messages)를 확인하세요.

따라서 이 예제에서는 유효성 검증에 실패하면 사용자가 컨트롤러의 `create` 메서드로 리다이렉트되고, 뷰에서 오류 메시지를 표시할 수 있습니다.

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

Laravel에 내장된 각 유효성 검증 규칙에는 애플리케이션의 `lang/en/validation.php` 파일에 위치한 오류 메시지가 있습니다. 애플리케이션에 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어를 사용해 Laravel이 이 디렉터리를 생성하도록 지시할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이러한 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리로 복사해 애플리케이션 언어에 맞게 메시지를 번역할 수 있습니다. Laravel 현지화에 대해 더 알아보려면 전체 [현지화 문서](/docs/13.x/localization)를 확인하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청과 유효성 검증

이 예제에서는 기존 폼을 사용해 애플리케이션으로 데이터를 전송했습니다. 하지만 많은 애플리케이션은 JavaScript 기반 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 중에 `validate` 메서드를 사용하면 Laravel은 리다이렉트 응답을 생성하지 않습니다. 대신 Laravel은 [모든 유효성 검증 오류가 포함된 JSON 응답](#validation-error-response-format)을 생성합니다. 이 JSON 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 디렉티브

`@error` [Blade](/docs/13.x/blade) 디렉티브를 사용하면 특정 속성에 대한 유효성 검증 오류 메시지가 존재하는지 빠르게 확인할 수 있습니다. `@error` 디렉티브 안에서는 `$message` 변수를 출력해 오류 메시지를 표시할 수 있습니다.

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

[이름이 지정된 오류 백](#named-error-bags)을 사용한다면, 오류 백의 이름을 `@error` 디렉티브의 두 번째 인수로 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 폼 다시 채우기

Laravel이 유효성 검증 오류로 인해 리다이렉트 응답을 생성하면, 프레임워크는 자동으로 [요청의 모든 입력을 세션에 플래시](/docs/13.x/session#flash-data)합니다. 이는 다음 요청에서 입력값에 편리하게 접근하고, 사용자가 제출하려고 했던 폼을 다시 채울 수 있도록 하기 위한 것입니다.

이전 요청에서 플래시된 입력을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다. `old` 메서드는 이전에 플래시된 입력 데이터를 [세션](/docs/13.x/session)에서 가져옵니다.

```php
$title = $request->old('title');
```

Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/13.x/blade) 안에서 이전 입력을 표시한다면, `old` 헬퍼를 사용해 폼을 다시 채우는 것이 더 편리합니다. 지정한 필드에 대한 이전 입력이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 참고

기본적으로 Laravel은 애플리케이션의 전역 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 때문에 Validator가 `null` 값을 유효하지 않은 값으로 판단하지 않도록 하려면 "선택적" 요청 필드를 `nullable`로 표시해야 하는 경우가 많습니다. 예를 들어 다음과 같습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예제에서는 `publish_at` 필드가 `null`이거나 유효한 날짜 표현일 수 있다고 지정합니다. 규칙 정의에 `nullable` 수정자가 추가되지 않으면 Validator는 `null`을 유효하지 않은 날짜로 판단합니다.

<a name="validation-error-response-format"></a>
### 유효성 검증 오류 응답 형식

애플리케이션이 `Illuminate\Validation\ValidationException` 예외를 발생시키고 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 오류 메시지를 자동으로 형식화하고 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래에서 유효성 검증 오류에 대한 JSON 응답 형식 예제를 확인할 수 있습니다. 중첩된 오류 키는 "점" 표기법 형식으로 평탄화됩니다.

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

<a name="form-request-validation"></a>
## 폼 요청 유효성 검증 (Form Request Validation)

<a name="creating-form-requests"></a>
### 폼 요청 생성

더 복잡한 유효성 검증 시나리오에서는 "폼 요청"을 만들고 싶을 수 있습니다. 폼 요청은 자체 유효성 검증 및 인가 로직을 캡슐화하는 사용자 정의 요청 클래스입니다. 폼 요청 클래스를 만들려면 `make:request` Artisan CLI 명령어를 사용할 수 있습니다.

```shell
php artisan make:request StorePostRequest
```

생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 배치됩니다. 이 디렉터리가 존재하지 않으면 `make:request` 명령어를 실행할 때 생성됩니다. Laravel이 생성하는 각 폼 요청에는 `authorize`와 `rules`라는 두 메서드가 있습니다.

예상할 수 있듯이 `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 나타내는 작업을 수행할 수 있는지 판단하는 역할을 합니다. 반면 `rules` 메서드는 요청 데이터에 적용해야 하는 유효성 검증 규칙을 반환합니다.

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
 */
public function rules(): array
{
    return [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ];
}
```

> [!NOTE]
> `rules` 메서드 시그니처 안에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다. 해당 의존성은 Laravel [서비스 컨테이너](/docs/13.x/container)를 통해 자동으로 해결됩니다.

그렇다면 유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 요청을 타입 힌트로 지정하기만 하면 됩니다. 들어오는 폼 요청은 컨트롤러 메서드가 호출되기 전에 유효성 검증됩니다. 즉, 컨트롤러에 유효성 검증 로직을 어지럽게 넣을 필요가 없습니다.

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // Store the blog post...

    return redirect('/posts');
}
```

유효성 검증에 실패하면 사용자를 이전 위치로 되돌려 보내는 리다이렉트 응답이 생성됩니다. 오류도 세션에 플래시되어 표시할 수 있게 됩니다. 요청이 XHR 요청이었다면, [유효성 검증 오류의 JSON 표현](#validation-error-response-format)을 포함한 422 상태 코드의 HTTP 응답이 사용자에게 반환됩니다.

> [!NOTE]
> Inertia 기반 Laravel 프론트엔드에 실시간 폼 요청 유효성 검증을 추가해야 하나요? [Laravel Precognition](/docs/13.x/precognition)을 확인하세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 유효성 검증 수행

때로는 초기 유효성 검증이 완료된 후 추가 유효성 검증을 수행해야 합니다. 폼 요청의 `after` 메서드를 사용해 이를 처리할 수 있습니다.

`after` 메서드는 유효성 검증이 완료된 뒤 호출될 콜러블 또는 클로저의 배열을 반환해야 합니다. 전달된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받으므로, 필요하다면 추가 오류 메시지를 발생시킬 수 있습니다.

```php
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    'Something is wrong with this field!'
                );
            }
        }
    ];
}
```
앞서 설명한 것처럼, `after` 메서드가 반환하는 배열에는 invokable 클래스도 포함될 수 있습니다. 이러한 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다.

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        new ValidateUserStatus,
        new ValidateShippingTime,
        function (Validator $validator) {
            //
        }
    ];
}
```

<a name="request-stopping-on-first-validation-rule-failure"></a>
#### 첫 번째 유효성 검증 실패 시 중단하기

요청 클래스에 `StopOnFirstFailure` 속성을 추가하면, 하나의 유효성 검증 실패가 발생하는 즉시 모든 속성에 대한 유효성 검증을 중단하도록 validator에 알릴 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a name="request-failing-on-unknown-fields"></a>
#### 알 수 없는 필드에서 실패 처리하기

요청 클래스에 `FailOnUnknownFields` 속성을 추가하면, 요청의 유효성 검증 규칙에 정의되지 않은 모든 입력 필드를 Laravel이 거부하도록 지시할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\FailOnUnknownFields;
use Illuminate\Foundation\Http\FormRequest;

#[FailOnUnknownFields]
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string'],
            'body' => ['required', 'string'],
        ];
    }
}
```

`AppServiceProvider`에서 모든 form request에 대해 이 동작을 전역으로 활성화할 수도 있습니다.

```php
use Illuminate\Foundation\Http\FormRequest;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    FormRequest::failOnUnknownFields();
}
```

필요한 경우 속성에 `false`를 전달하여 특정 요청에 대해서는 이 동작을 비활성화할 수 있습니다.

```php
#[FailOnUnknownFields(false)]
class PublicWebhookRequest extends FormRequest
{
    // ...
}
```

알 수 없는 필드를 거부하면 예상하지 못한 입력 키가 애플리케이션 내부로 더 깊이 전달되는 것을 막아, mass-assignment 방식의 문제에 대한 추가적인 보호를 제공할 수 있습니다. 하지만 여전히 모델의 `$fillable` / `$guarded` 속성을 설정하고, 신뢰할 수 있으며 유효성 검증을 통과한 입력만 저장해야 합니다.

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 커스터마이징

Form request 유효성 검증이 실패하면 사용자를 이전 위치로 돌려보내기 위한 리디렉션 응답이 생성됩니다. 하지만 이 동작은 자유롭게 커스터마이징할 수 있습니다. 이를 위해 form request에서 `RedirectTo` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectTo;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectTo('/dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

또는 사용자를 이름이 지정된 route로 리디렉션하고 싶다면, 대신 `RedirectToRoute` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectToRoute;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectToRoute('dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a name="customizing-the-error-bag"></a>
#### 에러 백 커스터마이징

Form request 유효성 검증이 실패하면 에러가 `default` 에러 백에 flash됩니다. 에러를 다른 [이름이 지정된 에러 백](#named-error-bags)에 저장해야 한다면, form request에서 `ErrorBag` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\ErrorBag;
use Illuminate\Foundation\Http\FormRequest;

#[ErrorBag('login')]
class LoginRequest extends FormRequest
{
    // ...
}
```

<a name="authorizing-form-requests"></a>
### Form Request 인가하기

Form request 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 안에서 인증된 사용자가 특정 리소스를 업데이트할 권한을 실제로 가지고 있는지 판단할 수 있습니다. 예를 들어, 사용자가 업데이트하려는 블로그 댓글을 실제로 소유하고 있는지 확인할 수 있습니다. 대부분의 경우 이 메서드 안에서 [authorization gates and policies](/docs/13.x/authorization)를 사용하게 됩니다.

```php
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

모든 form request는 기본 Laravel request 클래스를 확장하므로, `user` 메서드를 사용하여 현재 인증된 사용자에 접근할 수 있습니다. 또한 위 예제에서 `route` 메서드를 호출하는 부분도 확인하세요. 이 메서드를 사용하면 아래 예제의 `{comment}` 매개변수처럼 호출된 route에 정의된 URI 매개변수에 접근할 수 있습니다.

```php
Route::post('/comment/{comment}');
```

따라서 애플리케이션에서 [route model binding](/docs/13.x/routing#route-model-binding)을 활용하고 있다면, 해결된 모델을 request의 속성으로 접근하여 코드를 더 간결하게 만들 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하면 403 상태 코드를 가진 HTTP 응답이 자동으로 반환되며, 컨트롤러 메서드는 실행되지 않습니다.

요청에 대한 인가 로직을 애플리케이션의 다른 부분에서 처리할 계획이라면, `authorize` 메서드를 완전히 제거하거나 단순히 `true`를 반환하면 됩니다.

```php
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처 안에는 필요한 모든 의존성을 type-hint할 수 있습니다. 해당 의존성은 Laravel [service container](/docs/13.x/container)를 통해 자동으로 resolve됩니다.

<a name="customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

`messages` 메서드를 오버라이드하여 form request에서 사용하는 에러 메시지를 커스터마이징할 수 있습니다. 이 메서드는 속성 / 규칙 쌍과 그에 대응하는 에러 메시지의 배열을 반환해야 합니다.

```php
/**
 * Get the error messages for the defined validation rules.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
#### 유효성 검증 속성 커스터마이징

Laravel에 내장된 많은 유효성 검증 규칙 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 유효성 검증 메시지의 `:attribute` 플레이스홀더를 커스텀 속성 이름으로 대체하고 싶다면, `attributes` 메서드를 오버라이드하여 커스텀 이름을 지정할 수 있습니다. 이 메서드는 속성 / 이름 쌍의 배열을 반환해야 합니다.

```php
/**
 * Get custom attributes for validator errors.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => 'email address',
    ];
}
```

<a name="preparing-input-for-validation"></a>
### 유효성 검증을 위한 입력 준비하기

유효성 검증 규칙을 적용하기 전에 요청의 데이터를 준비하거나 정리해야 한다면, `prepareForValidation` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

마찬가지로, 유효성 검증이 완료된 뒤 요청 데이터를 정규화해야 한다면 `passedValidation` 메서드를 사용할 수 있습니다.

```php
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
## Validator 수동 생성하기 (Manually Creating Validators)

Request의 `validate` 메서드를 사용하고 싶지 않다면, `Validator` [facade](/docs/13.x/facades)를 사용하여 validator 인스턴스를 수동으로 생성할 수 있습니다. Facade의 `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        if ($validator->fails()) {
            return redirect('/post/create')
                ->withErrors($validator)
                ->withInput();
        }

        // Retrieve the validated input...
        $validated = $validator->validated();

        // Retrieve a portion of the validated input...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // Store the blog post...

        return redirect('/posts');
    }
}
```

`make` 메서드에 전달되는 첫 번째 인수는 유효성 검증 대상 데이터입니다. 두 번째 인수는 해당 데이터에 적용할 유효성 검증 규칙의 배열입니다.

요청 유효성 검증이 실패했는지 판단한 뒤에는 `withErrors` 메서드를 사용하여 에러 메시지를 세션에 flash할 수 있습니다. 이 메서드를 사용하면 리디렉션 후 `$errors` 변수가 view와 자동으로 공유되어, 사용자에게 에러 메시지를 쉽게 다시 표시할 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP `array`를 받을 수 있습니다.

#### 첫 번째 유효성 검증 실패 시 중단하기

`stopOnFirstFailure` 메서드는 하나의 유효성 검증 실패가 발생하는 즉시 모든 속성에 대한 유효성 검증을 중단해야 한다고 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

Validator 인스턴스를 수동으로 생성하면서도 HTTP request의 `validate` 메서드가 제공하는 자동 리디렉션을 활용하고 싶다면, 기존 validator 인스턴스에서 `validate` 메서드를 호출할 수 있습니다. 유효성 검증이 실패하면 사용자는 자동으로 리디렉션되며, XHR 요청의 경우 [JSON 응답이 반환됩니다](#validation-error-response-format).

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

유효성 검증이 실패했을 때 에러 메시지를 [이름이 지정된 에러 백](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 이름이 지정된 에러 백

한 페이지에 여러 form이 있다면, 유효성 검증 에러가 담긴 `MessageBag`에 이름을 붙여 특정 form의 에러 메시지만 가져오고 싶을 수 있습니다. 이를 위해 `withErrors`의 두 번째 인수로 이름을 전달합니다.

```php
return redirect('/register')->withErrors($validator, 'login');
```

그런 다음 `$errors` 변수에서 이름이 지정된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 에러 메시지 커스터마이징

필요한 경우 Laravel이 제공하는 기본 에러 메시지 대신 validator 인스턴스가 사용할 커스텀 에러 메시지를 제공할 수 있습니다. 커스텀 메시지를 지정하는 방법은 여러 가지입니다. 먼저 `Validator::make` 메서드의 세 번째 인수로 커스텀 메시지를 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예제에서 `:attribute` 플레이스홀더는 유효성 검증 중인 필드의 실제 이름으로 대체됩니다. 유효성 검증 메시지에서 다른 플레이스홀더도 사용할 수 있습니다. 예를 들면 다음과 같습니다.

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대한 커스텀 메시지 지정하기

때로는 특정 속성에 대해서만 커스텀 에러 메시지를 지정하고 싶을 수 있습니다. 이때는 "dot" 표기법을 사용할 수 있습니다. 먼저 속성 이름을 지정하고, 그 뒤에 규칙을 이어서 지정합니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 커스텀 속성 값 지정하기
Laravel의 내장 오류 메시지 중 다수는 유효성 검증 중인 필드 또는 속성 이름으로 대체되는 `:attribute` 플레이스홀더를 포함합니다. 특정 필드에서 이러한 플레이스홀더를 대체할 값을 사용자 정의하려면, `Validator::make` 메서드의 네 번째 인수로 사용자 정의 속성 배열을 전달할 수 있습니다:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 유효성 검증 수행

초기 유효성 검증이 완료된 후 추가 유효성 검증을 수행해야 할 때가 있습니다. 이는 validator의 `after` 메서드를 사용하여 처리할 수 있습니다. `after` 메서드는 유효성 검증이 완료된 후 호출될 클로저 또는 호출 가능한 항목의 배열을 받습니다. 전달된 호출 가능한 항목은 `Illuminate\Validation\Validator` 인스턴스를 받으므로, 필요한 경우 추가 오류 메시지를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

앞서 언급했듯이, `after` 메서드는 호출 가능한 항목의 배열도 받을 수 있습니다. 이는 "유효성 검증 이후" 로직이 호출 가능한 클래스에 캡슐화되어 있을 때 특히 편리합니다. 이 클래스들은 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받습니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;

$validator->after([
    new ValidateUserStatus,
    new ValidateShippingTime,
    function ($validator) {
        // ...
    },
]);
```

<a name="working-with-validated-input"></a>
## 유효성 검증된 입력 다루기 (Working With Validated Input)

form request 또는 수동으로 생성한 validator 인스턴스를 사용해 들어온 요청 데이터를 유효성 검증한 후, 실제로 유효성 검증을 거친 요청 데이터를 가져오고 싶을 수 있습니다. 이는 여러 방법으로 처리할 수 있습니다. 먼저 form request 또는 validator 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 유효성 검증된 데이터의 배열을 반환합니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는 form request나 validator 인스턴스에서 `safe` 메서드를 호출할 수 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체는 유효성 검증된 데이터의 일부 또는 전체 배열을 가져올 수 있도록 `only`, `except`, `all` 메서드를 제공합니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한 `Illuminate\Support\ValidatedInput` 인스턴스는 반복할 수 있으며 배열처럼 접근할 수 있습니다:

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

유효성 검증된 데이터에 추가 필드를 더하고 싶다면 `merge` 메서드를 호출할 수 있습니다:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

유효성 검증된 데이터를 [컬렉션](/docs/13.x/collections) 인스턴스로 가져오고 싶다면 `collect` 메서드를 호출할 수 있습니다:

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 다루기 (Working With Error Messages)

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. 이 인스턴스는 오류 메시지를 다루기 위한 다양한 편리한 메서드를 제공합니다. 모든 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 필드의 첫 번째 오류 메시지 가져오기

주어진 필드의 첫 번째 오류 메시지를 가져오려면 `first` 메서드를 사용합니다:

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 필드의 모든 오류 메시지 가져오기

주어진 필드에 대한 모든 메시지 배열을 가져와야 한다면 `get` 메서드를 사용합니다:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 form 필드를 유효성 검증하는 경우, `*` 문자를 사용해 각 배열 요소에 대한 모든 메시지를 가져올 수 있습니다:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드의 모든 오류 메시지 가져오기

모든 필드에 대한 모든 메시지 배열을 가져오려면 `all` 메서드를 사용합니다:

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 필드에 메시지가 있는지 확인하기

`has` 메서드는 주어진 필드에 오류 메시지가 있는지 확인하는 데 사용할 수 있습니다:

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에서 사용자 정의 메시지 지정하기

Laravel의 각 내장 validation rule에는 애플리케이션의 `lang/en/validation.php` 파일에 위치한 오류 메시지가 있습니다. 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어를 사용해 Laravel이 해당 디렉터리를 생성하도록 지시할 수 있습니다.

`lang/en/validation.php` 파일 안에는 각 validation rule에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지들을 자유롭게 변경하거나 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리로 복사하여 애플리케이션 언어에 맞게 메시지를 번역할 수 있습니다. Laravel 현지화에 대해 더 알아보려면 전체 [현지화 문서](/docs/13.x/localization)를 확인하십시오.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 사용자 정의 메시지

애플리케이션의 validation 언어 파일 안에서 지정된 속성과 rule 조합에 사용되는 오류 메시지를 사용자 정의할 수 있습니다. 이렇게 하려면 애플리케이션의 `lang/xx/validation.php` 언어 파일에 있는 `custom` 배열에 사용자 정의 메시지를 추가합니다:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

Laravel의 내장 오류 메시지 중 다수는 유효성 검증 중인 필드 또는 속성 이름으로 대체되는 `:attribute` 플레이스홀더를 포함합니다. validation 메시지의 `:attribute` 부분을 사용자 정의 값으로 대체하고 싶다면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 사용자 정의 속성 이름을 지정할 수 있습니다:

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

Laravel의 일부 내장 validation rule 오류 메시지는 요청 속성의 현재 값으로 대체되는 `:value` 플레이스홀더를 포함합니다. 하지만 때로는 validation 메시지의 `:value` 부분을 해당 값의 사용자 정의 표현으로 대체해야 할 수 있습니다. 예를 들어, `payment_type` 값이 `cc`일 때 신용카드 번호가 필요하다고 지정하는 다음 rule을 살펴보십시오:

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 validation rule이 실패하면 다음 오류 메시지가 생성됩니다:

```text
The credit card number field is required when payment type is cc.
```

결제 유형 값으로 `cc`를 표시하는 대신, `lang/xx/validation.php` 언어 파일에서 `values` 배열을 정의하여 더 사용자가 이해하기 쉬운 값 표현을 지정할 수 있습니다:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

이 값을 정의한 후에는 validation rule이 다음 오류 메시지를 생성합니다:

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용할 수 있는 Validation Rule (Available Validation Rules)

아래는 사용할 수 있는 모든 validation rule과 그 기능의 목록입니다:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

#### Boolean

<div class="collection-method-list" markdown="1">

[허용됨](#rule-accepted)
[조건부 허용됨](#rule-accepted-if)
[Boolean](#rule-boolean)
[거부됨](#rule-declined)
[조건부 거부됨](#rule-declined-if)

</div>

#### 문자열

<div class="collection-method-list" markdown="1">

[활성 URL](#rule-active-url)
[알파벳](#rule-alpha)
[알파벳 대시](#rule-alpha-dash)
[알파벳 숫자](#rule-alpha-num)
[ASCII](#rule-ascii)
[확인됨](#rule-confirmed)
[현재 비밀번호](#rule-current-password)
[서로 다름](#rule-different)
[다음으로 시작하지 않음](#rule-doesnt-start-with)
[다음으로 끝나지 않음](#rule-doesnt-end-with)
[이메일](#rule-email)
[다음으로 끝남](#rule-ends-with)
[Enum](#rule-enum)
[Hex 색상](#rule-hex-color)
[포함됨](#rule-in)
[IP 주소](#rule-ip)
[JSON](#rule-json)
[소문자](#rule-lowercase)
[MAC 주소](#rule-mac)
[최대](#rule-max)
[최소](#rule-min)
[포함되지 않음](#rule-not-in)
[정규 표현식](#rule-regex)
[정규 표현식 아님](#rule-not-regex)
[동일함](#rule-same)
[크기](#rule-size)
[다음으로 시작함](#rule-starts-with)
[문자열](#rule-string)
[대문자](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

#### 숫자

<div class="collection-method-list" markdown="1">

[사이](#rule-between)
[소수](#rule-decimal)
[서로 다름](#rule-different)
[자릿수](#rule-digits)
[자릿수 범위](#rule-digits-between)
[보다 큼](#rule-gt)
[보다 크거나 같음](#rule-gte)
[정수](#rule-integer)
[보다 작음](#rule-lt)
[보다 작거나 같음](#rule-lte)
[최대](#rule-max)
[최대 자릿수](#rule-max-digits)
[최소](#rule-min)
[최소 자릿수](#rule-min-digits)
[배수](#rule-multiple-of)
[숫자형](#rule-numeric)
[동일함](#rule-same)
[크기](#rule-size)

</div>

#### 배열

<div class="collection-method-list" markdown="1">

[배열](#rule-array)
[사이](#rule-between)
[포함](#rule-contains)
[포함하지 않음](#rule-doesnt-contain)
[고유함](#rule-distinct)
[배열 안에 있음](#rule-in-array)
[배열 키 안에 있음](#rule-in-array-keys)
[목록](#rule-list)
[최대](#rule-max)
[최소](#rule-min)
[크기](#rule-size)

</div>

#### 날짜

<div class="collection-method-list" markdown="1">

[이후](#rule-after)
[이후 또는 같음](#rule-after-or-equal)
[이전](#rule-before)
[이전 또는 같음](#rule-before-or-equal)
[날짜](#rule-date)
[날짜 같음](#rule-date-equals)
[날짜 형식](#rule-date-format)
[서로 다름](#rule-different)
[시간대](#rule-timezone)

</div>

#### 파일

<div class="collection-method-list" markdown="1">

[사이](#rule-between)
[크기 정보](#rule-dimensions)
[인코딩](#rule-encoding)
[확장자](#rule-extensions)
[파일](#rule-file)
[이미지](#rule-image)
[최대](#rule-max)
[MIME 유형](#rule-mimetypes)
[파일 확장자 기반 MIME 유형](#rule-mimes)
[크기](#rule-size)

</div>

#### 데이터베이스

<div class="collection-method-list" markdown="1">

[존재함](#rule-exists)
[고유함](#rule-unique)

</div>

#### 유틸리티

<div class="collection-method-list" markdown="1">

[다음 중 하나](#rule-anyof)
[Bail](#rule-bail)
[제외](#rule-exclude)
[조건부 제외](#rule-exclude-if)
[다음이 아닌 경우 제외](#rule-exclude-unless)
[함께 제외](#rule-exclude-with)
[없으면 제외](#rule-exclude-without)
[채워짐](#rule-filled)
[누락](#rule-missing)
[조건부 누락](#rule-missing-if)
[다음이 아닌 경우 누락](#rule-missing-unless)
[함께 누락](#rule-missing-with)
[모두 함께 누락](#rule-missing-with-all)
[Nullable](#rule-nullable)
[존재](#rule-present)
[조건부 존재](#rule-present-if)
[다음이 아닌 경우 존재](#rule-present-unless)
[함께 존재](#rule-present-with)
[모두 함께 존재](#rule-present-with-all)
[금지됨](#rule-prohibited)
[조건부 금지됨](#rule-prohibited-if)
[허용된 경우 금지됨](#rule-prohibited-if-accepted)
[거부된 경우 금지됨](#rule-prohibited-if-declined)
[다음이 아닌 경우 금지됨](#rule-prohibited-unless)
[금지함](#rule-prohibits)
[필수](#rule-required)
[조건부 필수](#rule-required-if)
[허용된 경우 필수](#rule-required-if-accepted)
[거부된 경우 필수](#rule-required-if-declined)
[다음이 아닌 경우 필수](#rule-required-unless)
[함께 필수](#rule-required-with)
[모두 함께 필수](#rule-required-with-all)
[없으면 필수](#rule-required-without)
[모두 없으면 필수](#rule-required-without-all)
[필수 배열 키](#rule-required-array-keys)
[때때로](#validating-when-present)
</div>

<a name="rule-accepted"></a>
#### accepted

유효성 검증 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`여야 합니다. 이는 "Terms of Service" 동의 여부나 이와 비슷한 필드를 검증할 때 유용합니다.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

유효성 검증 중인 다른 필드가 지정된 값과 같을 경우, 유효성 검증 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`여야 합니다. 이는 "Terms of Service" 동의 여부나 이와 비슷한 필드를 검증할 때 유용합니다.

<a name="rule-active-url"></a>
#### active_url

유효성 검증 중인 필드는 PHP `dns_get_record` 함수 기준으로 유효한 A 또는 AAAA 레코드를 가져야 합니다. 제공된 URL의 hostname은 `dns_get_record`에 전달되기 전에 PHP `parse_url` 함수를 사용해 추출됩니다.

<a name="rule-after"></a>
#### after:_date_

유효성 검증 중인 필드는 주어진 날짜 이후의 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 PHP `strtotime` 함수에 전달됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`으로 평가할 날짜 문자열을 전달하는 대신, 날짜와 비교할 다른 필드를 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

편의를 위해 날짜 기반 규칙은 fluent `date` rule builder를 사용해 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday`와 `todayOrAfter` 메서드를 사용하면 날짜가 각각 오늘 이후여야 하거나, 오늘 또는 그 이후여야 한다는 조건을 fluent하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

유효성 검증 중인 필드는 주어진 날짜 이후이거나 그 날짜와 같은 값이어야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하십시오.

편의를 위해 날짜 기반 규칙은 fluent `date` rule builder를 사용해 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 유효성 검증 규칙을 사용하면 유효성 검증 중인 필드가 주어진 유효성 검증 규칙 세트 중 하나를 만족해야 한다고 지정할 수 있습니다. 예를 들어 다음 규칙은 `username` 필드가 이메일 주소이거나, 대시를 포함할 수 있는 최소 6자 이상의 영숫자 문자열인지 검증합니다.

```php
use Illuminate\Validation\Rule;

'username' => [
    'required',
    Rule::anyOf([
        ['string', 'email'],
        ['string', 'alpha_dash', 'min:6'],
    ]),
],
```

<a name="rule-alpha"></a>
#### alpha

유효성 검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함되는 Unicode 알파벳 문자만으로 이루어져야 합니다.

이 유효성 검증 규칙을 ASCII 범위(`a-z` 및 `A-Z`)의 문자로 제한하려면 유효성 검증 규칙에 `ascii` 옵션을 제공하면 됩니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

유효성 검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함되는 Unicode 영숫자 문자와 ASCII 대시(`-`), ASCII 밑줄(`_`)만으로 이루어져야 합니다.

이 유효성 검증 규칙을 ASCII 범위(`a-z`, `A-Z`, `0-9`)의 문자로 제한하려면 유효성 검증 규칙에 `ascii` 옵션을 제공하면 됩니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

유효성 검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함되는 Unicode 영숫자 문자만으로 이루어져야 합니다.

이 유효성 검증 규칙을 ASCII 범위(`a-z`, `A-Z`, `0-9`)의 문자로 제한하려면 유효성 검증 규칙에 `ascii` 옵션을 제공하면 됩니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### array

유효성 검증 중인 필드는 PHP `array`여야 합니다.

`array` 규칙에 추가 값이 제공되면, 입력 배열의 각 키는 규칙에 제공된 값 목록 안에 있어야 합니다. 다음 예제에서 입력 배열의 `admin` 키는 `array` 규칙에 제공된 값 목록에 포함되어 있지 않으므로 유효하지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => 'array:name,username',
]);
```

일반적으로 배열 안에 존재해도 되는 배열 키를 항상 지정해야 합니다.

<a name="rule-ascii"></a>
#### ascii

유효성 검증 중인 필드는 7-bit ASCII 문자만으로 이루어져야 합니다.

<a name="rule-bail"></a>
#### bail

필드에서 첫 번째 유효성 검증 실패가 발생하면 해당 필드에 대한 유효성 검증 규칙 실행을 중단합니다.

`bail` 규칙은 유효성 검증 실패가 발생했을 때 특정 필드의 검증만 중단하지만, `stopOnFirstFailure` 메서드는 하나의 유효성 검증 실패가 발생하는 즉시 모든 속성의 검증을 중단해야 한다고 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### before:_date_

유효성 검증 중인 필드는 주어진 날짜보다 이전의 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 PHP `strtotime` 함수에 전달됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 유효성 검증 중인 다른 필드의 이름을 `date` 값으로 제공할 수도 있습니다.

편의를 위해 날짜 기반 규칙은 fluent `date` rule builder를 사용해 만들 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday`와 `todayOrBefore` 메서드를 사용하면 날짜가 각각 오늘 이전이어야 하거나, 오늘 또는 그 이전이어야 한다는 조건을 fluent하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

유효성 검증 중인 필드는 주어진 날짜보다 이전이거나 그 날짜와 같은 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 PHP `strtotime` 함수에 전달됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 유효성 검증 중인 다른 필드의 이름을 `date` 값으로 제공할 수도 있습니다.

편의를 위해 날짜 기반 규칙은 fluent `date` rule builder를 사용해 만들 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### between:_min_,_max_

유효성 검증 중인 필드는 주어진 _min_과 _max_ 사이의 크기여야 합니다. 이때 _min_과 _max_ 값도 포함됩니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-boolean"></a>
#### boolean

유효성 검증 중인 필드는 boolean으로 캐스팅될 수 있어야 합니다. 허용되는 입력값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

필드의 값이 `true` 또는 `false`일 때만 유효한 것으로 간주하려면 `strict` 매개변수를 사용할 수 있습니다.

```php
'foo' => 'boolean:strict'
```

<a name="rule-confirmed"></a>
#### confirmed

유효성 검증 중인 필드에는 `{field}_confirmation` 형식의 일치하는 필드가 있어야 합니다. 예를 들어 유효성 검증 중인 필드가 `password`라면, 입력값 안에 일치하는 `password_confirmation` 필드가 있어야 합니다.

사용자 지정 확인 필드 이름을 전달할 수도 있습니다. 예를 들어 `confirmed:repeat_username`은 `repeat_username` 필드가 유효성 검증 중인 필드와 일치할 것으로 기대합니다.

<a name="rule-contains"></a>
#### contains:_foo_,_bar_,...

유효성 검증 중인 필드는 주어진 모든 매개변수 값을 포함하는 배열이어야 합니다. 이 규칙은 배열을 `implode`해야 하는 경우가 많으므로, `Rule::contains` 메서드를 사용해 fluent하게 규칙을 만들 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::contains(['admin', 'editor']),
    ],
]);
```

<a name="rule-doesnt-contain"></a>
#### doesnt_contain:_foo_,_bar_,...

유효성 검증 중인 필드는 주어진 매개변수 값을 하나도 포함하지 않는 배열이어야 합니다. 이 규칙은 배열을 `implode`해야 하는 경우가 많으므로, `Rule::doesntContain` 메서드를 사용해 fluent하게 규칙을 만들 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::doesntContain(['admin', 'editor']),
    ],
]);
```

<a name="rule-current-password"></a>
#### current_password

유효성 검증 중인 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 매개변수를 사용해 [authentication guard](/docs/13.x/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### date

유효성 검증 중인 필드는 PHP `strtotime` 함수 기준으로 유효하며 상대 표현이 아닌 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

유효성 검증 중인 필드는 주어진 날짜와 같아야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 PHP `strtotime` 함수에 전달됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

유효성 검증 중인 필드는 주어진 _formats_ 중 하나와 일치해야 합니다. 필드를 검증할 때 `date` 또는 `date_format` 중 **하나만** 사용해야 하며, 둘을 함께 사용하면 안 됩니다. 이 유효성 검증 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 형식을 지원합니다.

편의를 위해 날짜 기반 규칙은 fluent `date` rule builder를 사용해 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### decimal:_min_,_max_

유효성 검증 중인 필드는 숫자여야 하며, 지정된 소수 자릿수를 포함해야 합니다.

```php
// Must have exactly two decimal places (9.99)...
'price' => 'decimal:2'

// Must have between 2 and 4 decimal places...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### declined

유효성 검증 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`여야 합니다.

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

유효성 검증 중인 다른 필드가 지정된 값과 같을 경우, 유효성 검증 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`여야 합니다.

<a name="rule-different"></a>
#### different:_field_

유효성 검증 중인 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

유효성 검증 중인 정수는 정확히 _value_ 길이를 가져야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

유효성 검증 중인 정수는 주어진 _min_과 _max_ 사이의 길이를 가져야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

유효성 검증 중인 파일은 규칙의 매개변수로 지정된 크기 제약 조건을 만족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건은 _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_, _min\_ratio_, _max\_ratio_입니다.

_ratio_ 제약 조건은 너비를 높이로 나눈 값으로 표현해야 합니다. 이는 `3/2`와 같은 분수나 `1.5`와 같은 float로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

_min\_ratio_와 _max\_ratio_ 제약 조건을 사용하여 허용 가능한 종횡비 범위를 정의할 수 있습니다.

```php
'avatar' => 'dimensions:min_ratio=1/2,max_ratio=3/2'
```

이 규칙은 여러 인수를 필요로 하므로, `Rule::dimensions` 메서드를 사용해 fluent하게 규칙을 만드는 것이 더 편리한 경우가 많습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()
            ->maxWidth(1000)
            ->maxHeight(500)
            ->ratio(3 / 2),
    ],
]);
```

`minRatio`, `maxRatio`, `ratioBetween` 메서드를 사용하여 종횡비 제약 조건을 fluent하게 정의할 수도 있습니다.

```php
Rule::dimensions()->ratioBetween(min: 1 / 2, max: 3 / 2)
```

<a name="rule-distinct"></a>
#### distinct

배열을 검증할 때, 유효성 검증 중인 필드는 중복 값을 가져서는 안 됩니다.

```php
'foo.*.id' => 'distinct'
```

`distinct`는 기본적으로 느슨한 변수 비교를 사용합니다. 엄격한 비교를 사용하려면 유효성 검증 규칙 정의에 `strict` 매개변수를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:strict'
```

대소문자 차이를 무시하도록 하려면 유효성 검증 규칙의 인수에 `ignore_case`를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### doesnt_start_with:_foo_,_bar_,...

유효성 검증 중인 필드는 주어진 값 중 하나로 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### doesnt_end_with:_foo_,_bar_,...

유효성 검증 중인 필드는 주어진 값 중 하나로 끝나서는 안 됩니다.

<a name="rule-email"></a>
#### email
유효성 검증 중인 필드는 이메일 주소 형식이어야 합니다. 이 유효성 검증 규칙은 이메일 주소를 검증하기 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` validator가 적용되지만, 다른 검증 방식도 함께 적용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위 예시는 `RFCValidation` 및 `DNSCheckValidation` 검증을 적용합니다. 적용할 수 있는 전체 검증 방식 목록은 다음과 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 주소를 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일을 검증하되, 경고가 발견되면 실패합니다(예: 끝에 붙은 마침표, 연속된 여러 마침표).
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 이메일 주소에 동형 문자나 오해를 유발하는 Unicode 문자가 포함되어 있지 않은지 확인합니다.
- `filter`: `FilterEmailValidation` - 이메일 주소가 PHP의 `filter_var` 함수 기준에 따라 유효한지 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - 일부 Unicode 문자를 허용하면서, 이메일 주소가 PHP의 `filter_var` 함수 기준에 따라 유효한지 확인합니다.

</div>

편의를 위해 이메일 유효성 검증 규칙은 fluent rule builder(체이닝 방식의 규칙 빌더)를 사용하여 만들 수 있습니다.

```php
use Illuminate\Validation\Rule;

$request->validate([
    'email' => [
        'required',
        Rule::email()
            ->rfcCompliant(strict: false)
            ->validateMxRecord()
            ->preventSpoofing()
    ],
]);
```

> [!WARNING]
> `dns` 및 `spoof` validator를 사용하려면 PHP `intl` 확장이 필요합니다.

<a name="rule-encoding"></a>
#### encoding:*encoding_type*

유효성 검증 중인 필드는 지정된 문자 인코딩과 일치해야 합니다. 이 규칙은 PHP의 `mb_check_encoding` 함수를 사용하여 주어진 파일 또는 문자열 값의 인코딩을 확인합니다. 편의를 위해 `encoding` 규칙은 Laravel의 fluent file rule builder를 사용하여 구성할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['csv'])
            ->encoding('utf-8'),
    ],
]);
```

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

유효성 검증 중인 필드는 주어진 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### enum

`Enum` 규칙은 유효성 검증 중인 필드에 유효한 enum 값이 포함되어 있는지 검증하는 클래스 기반 규칙입니다. `Enum` 규칙은 생성자의 유일한 인수로 enum의 이름을 받습니다. 원시 값을 검증할 때는 backed Enum을 `Enum` 규칙에 제공해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only` 및 `except` 메서드를 사용하여 어떤 enum case를 유효한 값으로 볼지 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메서드를 사용하여 조건에 따라 `Enum` 규칙을 수정할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

Rule::enum(ServerStatus::class)
    ->when(
        Auth::user()->isAdmin(),
        fn ($rule) => $rule->only(...),
        fn ($rule) => $rule->only(...),
    );
```

<a name="rule-exclude"></a>
#### exclude

유효성 검증 중인 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

유효성 검증 중인 필드는 _anotherfield_ 필드가 _value_와 같을 경우 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

복잡한 조건부 제외 로직이 필요한 경우 `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 boolean 또는 closure를 받습니다. closure가 주어지면, 해당 closure는 유효성 검증 중인 필드를 제외해야 하는지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::excludeIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::excludeIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_

유효성 검증 중인 필드는 _anotherfield_ 필드가 _value_와 같지 않은 한 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`)이면, 비교 대상 필드가 `null`이거나 요청 데이터에 비교 대상 필드가 없는 경우를 제외하고 유효성 검증 중인 필드는 제외됩니다.

복잡한 조건부 제외 로직이 필요한 경우 `Rule::excludeUnless` 메서드를 사용할 수 있습니다. 이 메서드는 boolean 또는 closure를 받습니다. closure가 주어지면, 해당 closure는 유효성 검증 중인 필드를 제외하지 않아야 하는지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::excludeUnless($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::excludeUnless(fn () => $request->user()->is_admin),
]);
```

<a name="rule-exclude-with"></a>
#### exclude_with:_anotherfield_

유효성 검증 중인 필드는 _anotherfield_ 필드가 존재할 경우 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

유효성 검증 중인 필드는 _anotherfield_ 필드가 존재하지 않을 경우 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### exists:_table_,_column_

유효성 검증 중인 필드는 주어진 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션이 지정되지 않으면 필드명이 사용됩니다. 따라서 이 경우 이 규칙은 `states` 데이터베이스 테이블에 요청의 `state` 속성 값과 일치하는 `state` 컬럼 값을 가진 레코드가 있는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 지정 컬럼명 지정하기

유효성 검증 규칙에서 사용할 데이터베이스 컬럼명을 데이터베이스 테이블명 뒤에 배치하여 명시적으로 지정할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

때로는 `exists` 쿼리에 사용할 특정 데이터베이스 연결을 지정해야 할 수 있습니다. 테이블명 앞에 연결명을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블명을 직접 지정하는 대신, 테이블명을 결정하는 데 사용할 Eloquent 모델을 지정할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

유효성 검증 규칙이 실행하는 쿼리를 사용자 지정하려면 `Rule` 클래스를 사용하여 규칙을 fluent하게 정의할 수 있습니다. 이 예시에서는 `|` 문자를 구분자로 사용하는 대신 유효성 검증 규칙을 배열로 지정합니다.

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            $query->where('account_id', 1);
        }),
    ],
]);
```

`Rule::exists` 메서드가 생성하는 `exists` 규칙에서 사용할 데이터베이스 컬럼명은 `exists` 메서드의 두 번째 인수로 컬럼명을 전달하여 명시적으로 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

때로는 값 배열이 데이터베이스에 존재하는지 검증하고 싶을 수 있습니다. 검증할 필드에 `exists` 규칙과 [array](#rule-array) 규칙을 함께 추가하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이 두 규칙이 하나의 필드에 함께 지정되면, Laravel은 주어진 모든 값이 지정된 테이블에 존재하는지 확인하기 위해 단일 쿼리를 자동으로 구성합니다.

<a name="rule-extensions"></a>
#### extensions:_foo_,_bar_,...

유효성 검증 중인 파일은 나열된 확장자 중 하나에 해당하는, 사용자가 지정한 확장자를 가져야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 파일을 사용자가 지정한 확장자만으로 검증하는 방식에 절대 의존해서는 안 됩니다. 이 규칙은 일반적으로 항상 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 함께 사용해야 합니다.

<a name="rule-file"></a>
#### file

유효성 검증 중인 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### filled

유효성 검증 중인 필드는 존재할 경우 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

유효성 검증 중인 필드는 주어진 _field_ 또는 _value_보다 커야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 기준으로 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

유효성 검증 중인 필드는 주어진 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 기준으로 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

유효성 검증 중인 필드는 [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값이어야 합니다.

<a name="rule-image"></a>
#### image

유효성 검증 중인 파일은 이미지(jpg, jpeg, png, bmp, gif 또는 webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 취약점 가능성 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 하는 경우 `image` 규칙에 `allow_svg` 지시어를 제공할 수 있습니다(`image:allow_svg`).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

유효성 검증 중인 필드는 주어진 값 목록에 포함되어야 합니다. 이 규칙은 배열을 `implode`해야 하는 경우가 많으므로, `Rule::in` 메서드를 사용하여 규칙을 fluent하게 구성할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

`in` 규칙이 `array` 규칙과 함께 사용되면, 입력 배열의 각 값은 `in` 규칙에 제공된 값 목록 안에 있어야 합니다. 다음 예시에서 입력 배열의 `LAS` 공항 코드는 `in` 규칙에 제공된 공항 목록에 포함되어 있지 않으므로 유효하지 않습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

유효성 검증 중인 필드는 _anotherfield_의 값 안에 존재해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

유효성 검증 중인 필드는 배열이어야 하며, 주어진 _values_ 중 적어도 하나를 배열의 키로 가지고 있어야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### integer

유효성 검증 중인 필드는 정수여야 합니다.

필드의 타입이 `integer`인 경우에만 유효한 것으로 간주하려면 `strict` 매개변수를 사용할 수 있습니다. 정수 값을 가진 문자열은 유효하지 않은 것으로 간주됩니다.

```php
'age' => 'integer:strict'
```

> [!WARNING]
> 이 유효성 검증 규칙은 입력값이 "integer" 변수 타입인지 확인하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙이 허용하는 타입인지 여부만 확인합니다. 입력값이 숫자인지 검증해야 한다면 이 규칙을 [the `numeric` validation rule](#rule-numeric)과 함께 사용하십시오.

<a name="rule-ip"></a>
#### ip

유효성 검증 중인 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### ipv4

유효성 검증 중인 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### ipv6

유효성 검증 중인 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### json

유효성 검증 중인 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

유효성 검증 중인 필드는 주어진 _field_보다 작아야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 기준으로 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

유효성 검증 중인 필드는 주어진 _field_보다 작거나 같아야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 기준으로 평가됩니다.

<a name="rule-lowercase"></a>
#### lowercase

유효성 검증 중인 필드는 소문자여야 합니다.

<a name="rule-list"></a>
#### list

유효성 검증 중인 필드는 list인 배열이어야 합니다. 배열의 키가 0부터 `count($array) - 1`까지 연속된 숫자로 구성되어 있으면 list로 간주됩니다.

<a name="rule-mac"></a>
#### mac_address

유효성 검증 중인 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

유효성 검증 중인 필드는 최대 _value_보다 작거나 같아야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

유효성 검증 중인 정수는 최대 길이가 _value_여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

유효성 검증 중인 파일은 주어진 MIME 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime',

'media' => 'mimetypes:image/*,video/*',
```

업로드된 파일의 MIME 타입을 확인하기 위해 파일 내용을 읽고 프레임워크가 MIME 타입을 추측합니다. 이 값은 클라이언트가 제공한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...
유효성 검증 대상 파일은 나열된 확장자 중 하나에 해당하는 MIME 타입이어야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하면 되지만, 이 규칙은 실제로 파일의 내용을 읽고 MIME 타입을 추측하여 파일의 MIME 타입을 검증합니다. MIME 타입과 해당 확장자의 전체 목록은 다음 위치에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 타입과 확장자

이 유효성 검증 규칙은 MIME 타입과 사용자가 파일에 지정한 확장자가 일치하는지 확인하지 않습니다. 예를 들어 `mimes:png` 유효성 검증 규칙은 파일 이름이 `photo.txt`이더라도, 파일 내용이 유효한 PNG 콘텐츠라면 유효한 PNG 이미지로 간주합니다. 사용자가 지정한 파일 확장자를 검증하려면 [extensions](#rule-extensions) 규칙을 사용할 수 있습니다.

<a name="rule-min"></a>
#### min:_value_

유효성 검증 대상 필드는 최소 _value_ 값을 가져야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

유효성 검증 대상 정수는 최소 길이가 _value_여야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

유효성 검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### missing

유효성 검증 대상 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

_anotherfield_ 필드가 임의의 _value_와 같으면 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

_anotherfield_ 필드가 임의의 _value_와 같은 경우가 아니라면 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

지정된 다른 필드 중 하나라도 존재하는 경우에만 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

지정된 다른 필드가 모두 존재하는 경우에만 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

유효성 검증 대상 필드는 주어진 값 목록에 포함되면 안 됩니다. `Rule::notIn` 메서드를 사용하여 유창한 방식으로 규칙을 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a name="rule-not-regex"></a>
#### not_regex:_pattern_

유효성 검증 대상 필드는 주어진 정규 표현식과 일치하지 않아야 합니다.

내부적으로 이 규칙은 PHP `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 것과 같은 형식을 따라야 하며, 따라서 유효한 구분자도 포함해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 특히 정규 표현식에 `|` 문자가 포함된 경우에는 `|` 구분자를 사용하는 대신 배열로 유효성 검증 규칙을 지정해야 할 수 있습니다.

<a name="rule-nullable"></a>
#### nullable

유효성 검증 대상 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

유효성 검증 대상 필드는 [numeric](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

`strict` 매개변수를 사용하면 필드 값이 정수 또는 부동소수점 타입일 때만 유효한 것으로 간주할 수 있습니다. 숫자 문자열은 유효하지 않은 것으로 간주됩니다.

```php
'amount' => 'numeric:strict'
```

<a name="rule-present"></a>
#### present

유효성 검증 대상 필드는 입력 데이터에 존재해야 합니다.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

_anotherfield_ 필드가 임의의 _value_와 같으면 유효성 검증 대상 필드는 존재해야 합니다.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

_anotherfield_ 필드가 임의의 _value_와 같은 경우가 아니라면 유효성 검증 대상 필드는 존재해야 합니다.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

지정된 다른 필드 중 하나라도 존재하는 경우에만 유효성 검증 대상 필드는 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

지정된 다른 필드가 모두 존재하는 경우에만 유효성 검증 대상 필드는 존재해야 합니다.

<a name="rule-prohibited"></a>
#### prohibited

유효성 검증 대상 필드는 없거나 비어 있어야 합니다. 필드는 다음 조건 중 하나를 만족하면 "비어 있음"으로 간주됩니다.

<div class="content-list" markdown="1">

- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_anotherfield_ 필드가 임의의 _value_와 같으면 유효성 검증 대상 필드는 없거나 비어 있어야 합니다. 필드는 다음 조건 중 하나를 만족하면 "비어 있음"으로 간주됩니다.

<div class="content-list" markdown="1">

- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

</div>

복잡한 조건부 금지 로직이 필요한 경우 `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받습니다. 클로저가 주어지면, 해당 클로저는 유효성 검증 대상 필드를 금지해야 하는지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf(fn () => $request->user()->is_admin),
]);
```
<a name="rule-prohibited-if-accepted"></a>
#### prohibited_if_accepted:_anotherfield_,...

_anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`와 같으면 유효성 검증 대상 필드는 없거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

_anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`와 같으면 유효성 검증 대상 필드는 없거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_anotherfield_ 필드가 임의의 _value_와 같은 경우가 아니라면 유효성 검증 대상 필드는 없거나 비어 있어야 합니다. 필드는 다음 조건 중 하나를 만족하면 "비어 있음"으로 간주됩니다.

<div class="content-list" markdown="1">

- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

</div>

복잡한 조건부 금지 로직이 필요한 경우 `Rule::prohibitedUnless` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받습니다. 클로저가 주어지면, 해당 클로저는 유효성 검증 대상 필드를 금지하지 않아야 하는지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedUnless($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedUnless(fn () => $request->user()->is_admin),
]);
```

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

유효성 검증 대상 필드가 없거나 비어 있지 않다면, _anotherfield_의 모든 필드는 없거나 비어 있어야 합니다. 필드는 다음 조건 중 하나를 만족하면 "비어 있음"으로 간주됩니다.

<div class="content-list" markdown="1">

- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

유효성 검증 대상 필드는 주어진 정규 표현식과 일치해야 합니다.

내부적으로 이 규칙은 PHP `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 것과 같은 형식을 따라야 하며, 따라서 유효한 구분자도 포함해야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 특히 정규 표현식에 `|` 문자가 포함된 경우에는 `|` 구분자를 사용하는 대신 배열로 규칙을 지정해야 할 수 있습니다.

<a name="rule-required"></a>
#### required

유효성 검증 대상 필드는 입력 데이터에 존재하고 비어 있지 않아야 합니다. 필드는 다음 조건 중 하나를 만족하면 "비어 있음"으로 간주됩니다.

<div class="content-list" markdown="1">

- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 경로가 없는 업로드된 파일입니다.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_anotherfield_ 필드가 임의의 _value_와 같으면 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

`required_if` 규칙에 더 복잡한 조건을 구성하려면 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받습니다. 클로저가 전달되면, 해당 클로저는 유효성 검증 대상 필드가 필수인지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-required-if-accepted"></a>
#### required_if_accepted:_anotherfield_,...

_anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`와 같으면 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

_anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`와 같으면 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

_anotherfield_ 필드가 임의의 _value_와 같은 경우가 아니라면 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다. 이는 _value_가 `null`이 아닌 한 _anotherfield_도 요청 데이터에 존재해야 한다는 뜻입니다. _value_가 `null`인 경우(`required_unless:name,null`), 비교 필드가 `null`이거나 비교 필드가 요청 데이터에 없지 않은 한 유효성 검증 대상 필드는 필수입니다.

`required_unless` 규칙에 더 복잡한 조건을 구성하려면 `Rule::requiredUnless` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받습니다. 클로저가 전달되면, 해당 클로저는 유효성 검증 대상 필드가 필수가 아닌지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::requiredUnless($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::requiredUnless(fn () => $request->user()->is_admin),
]);
```

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

지정된 다른 필드 중 하나라도 존재하고 비어 있지 않은 경우에만 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

지정된 다른 필드가 모두 존재하고 비어 있지 않은 경우에만 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

지정된 다른 필드 중 하나라도 비어 있거나 존재하지 않는 경우에만 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

지정된 다른 필드가 모두 비어 있거나 존재하지 않는 경우에만 유효성 검증 대상 필드는 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

유효성 검증 대상 필드는 배열이어야 하며, 지정된 키를 최소한 포함해야 합니다.

<a name="rule-same"></a>
#### same:_field_

주어진 _field_는 유효성 검증 대상 필드와 일치해야 합니다.

<a name="rule-size"></a>
#### size:_value_

유효성 검증 대상 필드는 주어진 _value_와 일치하는 크기를 가져야 합니다. 문자열 데이터의 경우 _value_는 문자 수에 해당합니다. 숫자 데이터의 경우 _value_는 주어진 정수 값에 해당합니다. 이때 속성에는 `numeric` 또는 `integer` 규칙도 있어야 합니다. 배열의 경우 _size_는 배열의 `count`에 해당합니다. 파일의 경우 _size_는 파일 크기(킬로바이트)에 해당합니다. 몇 가지 예를 살펴보겠습니다.

```php
// Validate that a string is exactly 12 characters long...
'title' => 'size:12';

// Validate that a provided integer equals 10...
'seats' => 'integer|size:10';

// Validate that an array has exactly 5 elements...
'tags' => 'array|size:5';

// Validate that an uploaded file is exactly 512 kilobytes...
'image' => 'file|size:512';
```

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

유효성 검증 대상 필드는 주어진 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

유효성 검증 대상 필드는 문자열이어야 합니다. 필드가 `null`도 허용되도록 하려면 해당 필드에 `nullable` 규칙을 지정해야 합니다.

편의를 위해 문자열 유효성 검증 규칙은 유창한 `Rule::string()` 규칙 빌더를 사용하여 구성할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'title' => [
    'required',
    Rule::string()
        ->min(3)
        ->max(255)
        ->alphaDash(ascii: true),
],
```

문자열 규칙 빌더는 `alpha`, `alphaDash`, `alphaNumeric`, `ascii`, `between`, `doesntEndWith`, `doesntStartWith`, `endsWith`, `exactly`, `lowercase`, `max`, `min`, `startsWith`, `uppercase` 등 일반적인 문자열 제약을 위한 메서드를 제공합니다. 규칙 빌더는 조건 적용이 가능하므로, `when` 및 `unless` 메서드를 사용하여 조건부로 제약을 적용할 수도 있습니다.

<a name="rule-timezone"></a>
#### timezone

유효성 검증 대상 필드는 `DateTimeZone::listIdentifiers` 메서드 기준으로 유효한 시간대 식별자여야 합니다.

[`DateTimeZone::listIdentifiers` 메서드가 허용하는 인수](https://www.php.net/manual/en/datetimezone.listidentifiers.php)도 이 유효성 검증 규칙에 제공할 수 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### unique:_table_,_column_

유효성 검증 대상 필드는 주어진 데이터베이스 테이블 안에 존재하지 않아야 합니다.

**사용자 지정 테이블 / 컬럼 이름 지정:**

테이블 이름을 직접 지정하는 대신, 테이블 이름을 결정하는 데 사용할 Eloquent 모델을 지정할 수 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션을 사용하여 필드에 해당하는 데이터베이스 컬럼을 지정할 수 있습니다. `column` 옵션을 지정하지 않으면 유효성 검증 대상 필드의 이름이 사용됩니다.

```php
'email' => 'unique:users,email_address'
```
**사용자 지정 데이터베이스 연결 지정하기**

때로는 Validator가 수행하는 데이터베이스 쿼리에 사용자 지정 연결을 설정해야 할 수 있습니다. 이를 위해 테이블명 앞에 연결 이름을 붙일 수 있습니다.

```php
'email' => 'unique:connection.users,email_address'
```

**지정한 ID를 무시하도록 Unique 규칙 강제하기:**

때로는 unique 유효성 검증 중에 지정한 ID를 무시하고 싶을 수 있습니다. 예를 들어 사용자의 이름, 이메일 주소, 위치를 포함하는 "프로필 수정" 화면을 생각해 보겠습니다. 일반적으로 이메일 주소가 고유한지 확인하고 싶을 것입니다. 하지만 사용자가 이메일 필드는 그대로 두고 이름 필드만 변경했다면, 해당 사용자가 이미 그 이메일 주소의 소유자이므로 유효성 검증 오류가 발생해서는 안 됩니다.

Validator가 사용자의 ID를 무시하도록 지시하려면 `Rule` 클래스를 사용해 규칙을 유연하게 정의합니다. 이 예제에서는 `|` 문자로 규칙을 구분하는 대신, 유효성 검증 규칙을 배열로 지정합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```

> [!WARNING]
> 사용자가 제어할 수 있는 요청 입력값을 `ignore` 메서드에 절대 전달해서는 안 됩니다. 대신 Eloquent 모델 인스턴스에서 가져온 자동 증가 ID나 UUID처럼 시스템에서 생성한 고유 ID만 전달해야 합니다. 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해집니다.

모델 키의 값을 `ignore` 메서드에 전달하는 대신, 전체 모델 인스턴스를 전달할 수도 있습니다. Laravel은 모델에서 키를 자동으로 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

테이블에서 `id`가 아닌 다른 기본 키 컬럼 이름을 사용하는 경우, `ignore` 메서드를 호출할 때 컬럼 이름을 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 유효성 검증 중인 속성 이름과 일치하는 컬럼의 고유성을 확인합니다. 하지만 `unique` 메서드의 두 번째 인수로 다른 컬럼 이름을 전달할 수 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 Where 절 추가하기:**

`where` 메서드를 사용해 쿼리를 사용자 지정하여 추가 쿼리 조건을 지정할 수 있습니다. 예를 들어 `account_id` 컬럼 값이 `1`인 레코드만 검색하도록 쿼리 범위를 제한하는 조건을 추가해 보겠습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**Unique 검사에서 Soft Delete된 레코드 무시하기:**

기본적으로 unique 규칙은 고유성을 판단할 때 soft delete된 레코드도 포함합니다. 고유성 검사에서 soft delete된 레코드를 제외하려면 `withoutTrashed` 메서드를 호출하면 됩니다.

```php
Rule::unique('users')->withoutTrashed();
```

모델이 soft delete된 레코드에 대해 `deleted_at`이 아닌 다른 컬럼 이름을 사용하는 경우, `withoutTrashed` 메서드를 호출할 때 컬럼 이름을 제공할 수 있습니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### uppercase

유효성 검증 중인 필드는 대문자여야 합니다.

<a name="rule-url"></a>
#### url

유효성 검증 중인 필드는 유효한 URL이어야 합니다.

유효한 것으로 간주할 URL 프로토콜을 지정하고 싶다면, 프로토콜을 유효성 검증 규칙 매개변수로 전달할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### ulid

유효성 검증 중인 필드는 유효한 [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID)여야 합니다.

<a name="rule-uuid"></a>
#### uuid

유효성 검증 중인 필드는 유효한 RFC 9562(version 1, 3, 4, 5, 6, 7 또는 8) 범용 고유 식별자(UUID)여야 합니다.

주어진 UUID가 특정 버전의 UUID 명세와 일치하는지도 검증할 수 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부로 규칙 추가하기 (Conditionally Adding Rules)

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 필드가 특정 값을 가질 때 유효성 검증 건너뛰기

다른 필드가 특정 값을 가질 때 주어진 필드를 검증하지 않고 싶을 수 있습니다. 이 작업은 `exclude_if` 유효성 검증 규칙을 사용해 수행할 수 있습니다. 이 예제에서는 `has_appointment` 필드의 값이 `false`인 경우 `appointment_date`와 `doctor_name` 필드는 유효성 검증되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

또는 `exclude_unless` 규칙을 사용해, 다른 필드가 특정 값을 가지지 않는 한 주어진 필드를 검증하지 않도록 할 수 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 존재할 때만 유효성 검증하기

어떤 상황에서는 유효성 검증 대상 데이터에 필드가 존재하는 경우에만 해당 필드에 대해 유효성 검증 검사를 실행하고 싶을 수 있습니다. 이를 빠르게 수행하려면 규칙 목록에 `sometimes` 규칙을 추가합니다.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위 예제에서 `email` 필드는 `$data` 배열에 존재하는 경우에만 유효성 검증됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드를 검증하려는 경우, [선택적 필드에 대한 이 참고 사항](#a-note-on-optional-fields)을 확인하십시오.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 유효성 검증

때로는 더 복잡한 조건부 로직에 따라 유효성 검증 규칙을 추가하고 싶을 수 있습니다. 예를 들어 다른 필드의 값이 100보다 클 때만 특정 필드를 필수로 요구하고 싶을 수 있습니다. 또는 다른 필드가 존재할 때만 두 필드가 특정 값을 가져야 할 수도 있습니다. 이러한 유효성 검증 규칙을 추가하는 작업은 어렵지 않습니다. 먼저 절대 변경되지 않는 _정적 규칙_ 으로 `Validator` 인스턴스를 생성합니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

우리 웹 애플리케이션이 게임 수집가를 위한 것이라고 가정해 보겠습니다. 게임 수집가가 애플리케이션에 가입하면서 100개가 넘는 게임을 가지고 있다면, 왜 그렇게 많은 게임을 가지고 있는지 설명하도록 요구하고 싶습니다. 예를 들어 게임 재판매 상점을 운영할 수도 있고, 단순히 게임 수집을 즐길 수도 있습니다. 이 요구 사항을 조건부로 추가하기 위해 `Validator` 인스턴스의 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메서드에 전달되는 첫 번째 인수는 조건부로 유효성 검증할 필드의 이름입니다. 두 번째 인수는 추가하려는 규칙 목록입니다. 세 번째 인수로 전달된 클로저가 `true`를 반환하면 규칙이 추가됩니다. 이 메서드를 사용하면 복잡한 조건부 유효성 검증을 쉽게 구성할 수 있습니다. 여러 필드에 대해 한 번에 조건부 유효성 검증을 추가할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 매개변수는 `Illuminate\Support\Fluent`의 인스턴스이며, 유효성 검증 중인 입력값과 파일에 접근하는 데 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 유효성 검증

때로는 같은 중첩 배열 안에 있지만 인덱스를 알 수 없는 다른 필드를 기준으로 특정 필드를 검증하고 싶을 수 있습니다. 이런 상황에서는 클로저가 두 번째 인수를 받을 수 있도록 할 수 있으며, 이 인수는 유효성 검증 중인 배열의 현재 개별 항목입니다.

```php
$input = [
    'channels' => [
        [
            'type' => 'email',
            'address' => 'abigail@example.com',
        ],
        [
            'type' => 'url',
            'address' => 'https://example.com',
        ],
    ],
];

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

클로저에 전달되는 `$input` 매개변수와 마찬가지로, 속성 데이터가 배열인 경우 `$item` 매개변수는 `Illuminate\Support\Fluent`의 인스턴스입니다. 그렇지 않으면 문자열입니다.

<a name="validating-arrays"></a>
## 배열 유효성 검증 (Validating Arrays)

[array 유효성 검증 규칙 문서](#rule-array)에서 설명했듯이, `array` 규칙은 허용할 배열 키 목록을 받습니다. 배열 안에 추가 키가 존재하면 유효성 검증은 실패합니다.

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => 'array:name,username',
]);
```

일반적으로 배열 안에 존재할 수 있는 키를 항상 지정해야 합니다. 그렇지 않으면 Validator의 `validate` 및 `validated` 메서드는 해당 키들이 다른 중첩 배열 유효성 검증 규칙으로 검증되지 않았더라도, 배열과 그 안의 모든 키를 포함한 전체 검증된 데이터를 반환합니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 유효성 검증

중첩 배열 기반 폼 입력 필드를 검증하는 작업은 어렵지 않습니다. 배열 안의 속성을 검증하려면 "점 표기법"을 사용할 수 있습니다. 예를 들어 들어오는 HTTP 요청에 `photos[profile]` 필드가 포함되어 있다면 다음과 같이 검증할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소도 검증할 수 있습니다. 예를 들어 주어진 배열 입력 필드의 각 이메일이 고유한지 검증하려면 다음과 같이 할 수 있습니다.

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

마찬가지로 [언어 파일에서 사용자 지정 유효성 검증 메시지를 지정할 때](#custom-messages-for-specific-attributes) `*` 문자를 사용할 수 있으므로, 배열 기반 필드에 대해 하나의 유효성 검증 메시지를 쉽게 사용할 수 있습니다.

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터에 접근하기

때로는 속성에 유효성 검증 규칙을 할당할 때 주어진 중첩 배열 요소의 값에 접근해야 할 수 있습니다. 이는 `Rule::forEach` 메서드를 사용해 수행할 수 있습니다. `forEach` 메서드는 유효성 검증 중인 배열 속성의 각 반복마다 호출되는 클로저를 받으며, 속성의 값과 명시적으로 완전히 확장된 속성 이름을 전달받습니다. 클로저는 배열 요소에 할당할 규칙 배열을 반환해야 합니다.

```php
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="error-message-indexes-and-positions"></a>
### 오류 메시지 인덱스와 위치

배열을 검증할 때, 애플리케이션이 표시하는 오류 메시지 안에서 유효성 검증에 실패한 특정 항목의 인덱스나 위치를 참조하고 싶을 수 있습니다. 이를 위해 [사용자 지정 유효성 검증 메시지](#manual-customizing-the-error-messages)에 `:index`(`0`부터 시작), `:position`(`1`부터 시작), 또는 `:ordinal-position`(`1st`부터 시작) 플레이스홀더를 포함할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'photos' => [
        [
            'name' => 'BeachVacation.jpg',
            'description' => 'A photo of my beach vacation!',
        ],
        [
            'name' => 'GrandCanyon.jpg',
            'description' => '',
        ],
    ],
];

Validator::validate($input, [
    'photos.*.description' => 'required',
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

위 예제가 주어지면 유효성 검증은 실패하며, 사용자에게 _"Please describe photo #2."_ 오류가 표시됩니다.

필요하다면 `second-index`, `second-position`, `third-index`, `third-position` 등을 통해 더 깊게 중첩된 인덱스와 위치를 참조할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 유효성 검증 (Validating Files)

Laravel은 업로드된 파일을 검증하는 데 사용할 수 있는 `mimes`, `image`, `min`, `max`와 같은 다양한 유효성 검증 규칙을 제공합니다. 파일을 검증할 때 이러한 규칙을 개별적으로 지정해도 되지만, Laravel은 편리하게 사용할 수 있는 유연한 파일 유효성 검증 규칙 빌더도 제공합니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)
            ->max(12 * 1024),
    ],
]);
```

<a name="validating-files-file-types"></a>
#### 파일 유형 유효성 검증

`types` 메서드를 호출할 때는 확장자만 지정하면 되지만, 이 메서드는 실제로 파일 내용을 읽고 MIME 타입을 추정하여 파일의 MIME 타입을 검증합니다. MIME 타입과 해당 확장자의 전체 목록은 다음 위치에서 확인할 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 유효성 검증

편의를 위해 최소 및 최대 파일 크기는 파일 크기 단위를 나타내는 접미사가 붙은 문자열로 지정할 수 있습니다. `kb`, `mb`, `gb`, `tb` 접미사가 지원됩니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 유효성 검증

애플리케이션이 사용자가 업로드한 이미지를 받는 경우, `File` 규칙의 `image` 생성자 메서드를 사용해 유효성 검증 중인 파일이 이미지(jpg, jpeg, png, bmp, gif 또는 webp)인지 확인할 수 있습니다.

또한 `dimensions` 규칙을 사용해 이미지의 크기를 제한할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image()
            ->min(1024)
            ->max(12 * 1024)
            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),
    ],
]);
```

> [!NOTE]
> 이미지 크기 유효성 검증에 대한 자세한 정보는 [dimension 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약점 가능성 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 한다면 `image` 규칙에 `allowSvg: true`를 전달할 수 있습니다: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기 유효성 검증

이미지의 크기도 검증할 수 있습니다. 예를 들어 업로드된 이미지가 최소 너비 1000픽셀, 높이 500픽셀인지 검증하려면 `dimensions` 규칙을 사용할 수 있습니다.

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

File::image()->dimensions(
    Rule::dimensions()
        ->maxWidth(1000)
        ->maxHeight(500)
)
```
> [!NOTE]
> 이미지 크기 유효성 검증에 대한 자세한 내용은 [dimension 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

<a name="validating-passwords"></a>
## 비밀번호 유효성 검증 (Validating Passwords)

비밀번호가 충분한 수준의 복잡성을 갖추도록 하려면 Laravel의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체를 사용하면 비밀번호에 최소 하나의 문자, 숫자, 기호 또는 대소문자가 섞인 문자를 요구하는 등 애플리케이션의 비밀번호 복잡도 요구 사항을 쉽게 사용자 정의할 수 있습니다.

```php
// Require at least 8 characters...
Password::min(8)

// Require at least one letter...
Password::min(8)->letters()

// Require at least one uppercase and one lowercase letter...
Password::min(8)->mixedCase()

// Require at least one number...
Password::min(8)->numbers()

// Require at least one symbol...
Password::min(8)->symbols()
```

또한 `uncompromised` 메서드를 사용하여 공개 비밀번호 데이터 유출 사고에서 해당 비밀번호가 유출된 적이 없는지 확인할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로 `Password` 규칙 객체는 사용자의 개인정보나 보안을 해치지 않으면서 [k-Anonymity(k-익명성)](https://en.wikipedia.org/wiki/K-anonymity) 모델을 사용하여 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호가 유출되었는지 판단합니다.

기본적으로 비밀번호가 데이터 유출 목록에 한 번이라도 나타나면 유출된 것으로 간주됩니다. `uncompromised` 메서드의 첫 번째 인수를 사용하여 이 임계값을 사용자 정의할 수 있습니다.

```php
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

물론 위 예제의 모든 메서드를 체이닝할 수도 있습니다.

```php
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의

애플리케이션의 한 위치에서 비밀번호에 대한 기본 유효성 검증 규칙을 지정하면 편리할 수 있습니다. 클로저를 받는 `Password::defaults` 메서드를 사용하면 이를 쉽게 구현할 수 있습니다. `defaults` 메서드에 전달되는 클로저는 Password 규칙의 기본 구성을 반환해야 합니다. 일반적으로 `defaults` 규칙은 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 안에서 호출해야 합니다.

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
            ? $rule->mixedCase()->uncompromised()
            : $rule;
    });
}
```

그런 다음 유효성 검증 중인 특정 비밀번호에 기본 규칙을 적용하려면 인수 없이 `defaults` 메서드를 호출하면 됩니다.

```php
'password' => ['required', Password::defaults()],
```

때로는 기본 비밀번호 유효성 검증 규칙에 추가 유효성 검증 규칙을 붙이고 싶을 수 있습니다. 이를 위해 `rules` 메서드를 사용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 사용자 정의 유효성 검증 규칙 (Custom Validation Rules)

<a name="using-rule-objects"></a>
### 규칙 객체 사용

Laravel은 다양한 유용한 유효성 검증 규칙을 제공합니다. 하지만 직접 만든 규칙을 지정하고 싶을 수도 있습니다. 사용자 정의 유효성 검증 규칙을 등록하는 한 가지 방법은 규칙 객체를 사용하는 것입니다. 새 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용할 수 있습니다. 이 명령어로 문자열이 대문자인지 확인하는 규칙을 생성해 보겠습니다. Laravel은 새 규칙을 `app/Rules` 디렉터리에 배치합니다. 이 디렉터리가 없으면 규칙을 생성하는 Artisan 명령어를 실행할 때 Laravel이 해당 디렉터리를 생성합니다.

```shell
php artisan make:rule Uppercase
```

규칙이 생성되면 이제 동작을 정의할 준비가 된 것입니다. 규칙 객체에는 하나의 메서드, 즉 `validate`가 포함됩니다. 이 메서드는 속성 이름, 해당 값, 그리고 유효성 검증 실패 시 유효성 검증 오류 메시지와 함께 호출해야 하는 콜백을 받습니다.

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

규칙이 정의되면 다른 유효성 검증 규칙과 함께 규칙 객체의 인스턴스를 전달하여 validator에 붙일 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 유효성 검증 메시지 번역

`$fail` 클로저에 리터럴 오류 메시지를 제공하는 대신 [번역 문자열 키](/docs/13.x/localization)를 제공하고 Laravel이 오류 메시지를 번역하도록 지시할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요하다면 `translate` 메서드의 첫 번째와 두 번째 인수로 플레이스홀더 대체 값과 선호 언어를 제공할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터 접근

사용자 정의 유효성 검증 규칙 클래스가 유효성 검증 중인 다른 모든 데이터에 접근해야 한다면, 규칙 클래스는 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스는 클래스가 `setData` 메서드를 정의하도록 요구합니다. 이 메서드는 유효성 검증이 진행되기 전에 Laravel에 의해 자동으로 호출되며, 유효성 검증 대상의 모든 데이터를 전달받습니다.

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * All of the data under validation.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array<string, mixed>  $data
     */
    public function setData(array $data): static
    {
        $this->data = $data;

        return $this;
    }
}
```

또는 유효성 검증 규칙이 유효성 검증을 수행하는 validator 인스턴스에 접근해야 한다면 `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * The validator instance.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Set the current validator.
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a name="using-closures"></a>
### 클로저 사용

애플리케이션 전체에서 사용자 정의 규칙의 기능이 한 번만 필요하다면 규칙 객체 대신 클로저를 사용할 수 있습니다. 클로저는 속성 이름, 속성 값, 그리고 유효성 검증이 실패했을 때 호출해야 하는 `$fail` 콜백을 받습니다.

```php
use Illuminate\Support\Facades\Validator;
use Closure;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function (string $attribute, mixed $value, Closure $fail) {
            if ($value === 'foo') {
                $fail("The {$attribute} is invalid.");
            }
        },
    ],
]);
```

<a name="implicit-rules"></a>
### 암묵적 규칙

기본적으로 유효성 검증 중인 속성이 존재하지 않거나 빈 문자열을 포함하는 경우, 사용자 정의 규칙을 포함한 일반 유효성 검증 규칙은 실행되지 않습니다. 예를 들어 [unique](#rule-unique) 규칙은 빈 문자열에 대해 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

사용자 정의 규칙이 속성이 비어 있어도 실행되도록 하려면, 해당 규칙은 그 속성이 필수임을 암묵적으로 나타내야 합니다. 새 암묵적 규칙 객체를 빠르게 생성하려면 `--implicit` 옵션과 함께 `make:rule` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적" 규칙은 속성이 필수임을 _암시_할 뿐입니다. 누락되었거나 비어 있는 속성을 실제로 유효하지 않은 것으로 처리할지는 직접 결정해야 합니다.
