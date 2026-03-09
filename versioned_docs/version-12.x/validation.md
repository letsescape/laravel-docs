# 유효성 검증 (Validation)

- [소개](#introduction)
- [검증 빠른 시작](#validation-quickstart)
    - [라우트 정의](#quick-defining-the-routes)
    - [컨트롤러 생성](#quick-creating-the-controller)
    - [검증 로직 작성](#quick-writing-the-validation-logic)
    - [검증 오류 표시](#quick-displaying-the-validation-errors)
    - [양식 다시 채우기](#repopulating-forms)
    - [선택 항목에 대한 참고 사항](#a-note-on-optional-fields)
    - [검증 오류 응답 형식](#validation-error-response-format)
- [양식 요청 확인](#form-request-validation)
    - [양식 요청 작성](#creating-form-requests)
    - [양식 요청 승인](#authorizing-form-requests)
    - [오류 메시지 사용자 지정](#customizing-the-error-messages)
    - [검증을 위한 입력 준비 중](#preparing-input-for-validation)
- [수동으로 검증인 생성](#manually-creating-validators)
    - [자동 리디렉션](#automatic-redirection)
    - [명명된 오류 백](#named-error-bags)
    - [오류 메시지 사용자 지정](#manual-customizing-the-error-messages)
    - [추가 검증 수행 중](#performing-additional-validation)
- [검증된 입력 작업](#working-with-validated-input)
- [오류 메시지 작업](#working-with-error-messages)
    - [언어 파일에서 사용자 지정 메시지 지정](#specifying-custom-messages-in-language-files)
    - [언어 파일의 속성 지정](#specifying-attribute-in-language-files)
    - [언어 파일에 값 지정](#specifying-values-in-language-files)
- [사용 가능한 검증 규칙](#available-validation-rules)
- [조건부 규칙 추가](#conditionally-adding-rules)
- [배열 검증 중](#validating-arrays)
    - [중첩 배열 입력 검증](#validating-nested-array-input)
    - [오류 메시지 색인 및 위치](#error-message-indexes-and-positions)
- [파일 유효성 검사 중](#validating-files)
- [비밀번호 확인 중](#validating-passwords)
- [사용자 지정 검증 규칙](#custom-validation-rules)
    - [규칙 객체 사용](#using-rule-objects)
    - [클로저 사용](#using-closures)
    - [암시적 규칙](#implicit-rules)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel는 애플리케이션의 수신 데이터를 검증하기 위한 다양한 접근 방식을 제공합니다. 들어오는 모든 HTTP 요청에 사용할 수 있는 `validate` 메서드를 사용하는 것이 가장 일반적입니다. 그러나 검증에 대한 다른 접근 방식도 논의할 것입니다.

Laravel에는 데이터에 적용할 수 있는 다양하고 편리한 유효성 검사 규칙이 포함되어 있으며, 특정 데이터베이스 테이블에서 값이 고유한지 유효성을 검사하는 기능도 제공합니다. Laravel의 모든 유효성 검사 기능에 익숙해질 수 있도록 이러한 각 유효성 검사 규칙을 자세히 다룰 것입니다.

<a name="validation-quickstart"></a>
## 검증 빠른 시작 (Validation Quickstart)

Laravel의 강력한 유효성 검사 기능에 대해 알아보려면 양식의 유효성을 검사하고 사용자에게 오류 메시지를 표시하는 전체 예를 살펴보겠습니다. 이 높은 수준의 개요를 읽으면 Laravel을 사용하여 수신 요청 데이터의 유효성을 검사하는 방법에 대한 일반적인 이해를 얻을 수 있습니다.

<a name="quick-defining-the-routes"></a>
### 라우트 정의

먼저 `routes/web.php` 파일에 다음 라우트가 정의되어 있다고 가정해 보겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

`GET` 라우트는 사용자가 새 블로그 게시물을 만들 수 있는 양식을 표시하고, `POST` 라우트는 새 블로그 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성

다음으로 이러한 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 지금은 `store` 메서드를 비워 두겠습니다.

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
### 유효성 검사 논리 작성

이제 새 블로그 게시물의 유효성을 검사하는 논리로 `store` 메서드를 채울 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 개체에서 제공하는 `validate` 메서드를 사용합니다. 유효성 검사 규칙을 통과하면 코드가 정상적으로 계속 실행됩니다. 그러나 유효성 검사가 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고 적절한 오류 응답이 자동으로 사용자에게 다시 전송됩니다.

기존 HTTP 요청 중에 유효성 검사가 실패하면 이전 URL에 대한 리디렉션 응답이 생성됩니다. 들어오는 요청이 XHR 요청인 경우 [검증 오류 메시지가 포함된 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 방법을 더 잘 이해하기 위해 `store` 방법으로 다시 돌아가 보겠습니다.

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

보시다시피 유효성 검사 규칙은 `validate` 메서드로 전달됩니다. 걱정하지 마세요. 사용 가능한 모든 유효성 검사 규칙은 [문서화](#available-validation-rules)되어 있습니다. 다시 말하지만 유효성 검사가 실패하면 적절한 응답이 자동으로 생성됩니다. 유효성 검사가 통과되면 컨트롤러가 정상적으로 계속 실행됩니다.

또는 유효성 검사 규칙을 단일 `|` 구분 문자열 대신 규칙 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

또한 `validateWithBag` 메소드를 사용하여 요청을 검증하고 [이름이 지정된 오류 백](#named-error-bags) 내에 오류 메시지를 저장할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중지

때로는 첫 번째 검증 실패 후 속성에 대한 검증 규칙 실행을 중지하고 싶을 수도 있습니다. 이렇게 하려면 `bail` 규칙을 속성에 할당합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

이 예에서 `title` 속성에 대한 `unique` 규칙이 실패하면 `max` 규칙이 확인되지 않습니다. 규칙은 할당된 순서대로 유효성이 검사됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩된 속성에 대한 참고 사항

수신되는 HTTP 요청에 "중첩" 필드 데이터가 포함되어 있는 경우 "점" 구문을 사용하여 유효성 검사 규칙에 다음 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

반면, 필드 이름에 리터럴 마침표가 포함된 경우 백슬래시로 마침표를 이스케이프 처리하여 이것이 "점" 구문으로 해석되는 것을 명시적으로 방지할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
### 검증 오류 표시

그렇다면 수신 요청 필드가 지정된 유효성 검사 규칙을 통과하지 못하면 어떻게 될까요? 이전에 언급했듯이 Laravel는 자동으로 사용자를 이전 위치로 다시 리디렉션합니다. 또한 모든 유효성 검사 오류와 [요청 입력](/docs/12.x/requests#retrieving-old-input)은 자동으로 [세션에 플래시](/docs/12.x/session#flash-data)됩니다.

`$errors` 변수는 `web` 미들웨어 그룹에서 제공하는 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에 의해 애플리케이션의 모든 뷰와 공유됩니다. 이 미들웨어가 적용되면 `$errors` 변수는 뷰에서 항상 사용할 수 있으므로 `$errors` 변수가 항상 정의되어 안전하게 사용할 수 있다고 편리하게 가정할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스가 됩니다. 이 개체 작업에 대한 자세한 내용은 [문서 확인](#working-with-error-messages)을 참조하세요.

따라서 이 예에서는 유효성 검사가 실패하면 사용자가 컨트롤러의 `create` 메서드로 리디렉션되어 뷰에 오류 메시지를 표시할 수 있습니다.

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
#### 오류 메시지 사용자 지정

Laravel의 내장 유효성 검사 규칙에는 각각 애플리케이션의 `lang/en/validation.php` 파일에 있는 오류 메시지가 있습니다. 응용 프로그램에 `lang` 디렉터리가 없으면 `lang:publish` Artisan 명령을 사용하여 Laravel에 디렉터리를 생성하도록 지시할 수 있습니다.

`lang/en/validation.php` 파일 내에서 각 유효성 검사 규칙에 대한 번역 항목을 찾을 수 있습니다. 애플리케이션의 필요에 따라 이러한 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리에 복사하여 애플리케이션 언어에 대한 메시지를 번역할 수도 있습니다. Laravel 현지화에 대해 자세히 알아보려면 전체 [현지화 문서](/docs/12.x/localization)를 확인하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되지 않습니다. Laravel의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR 요청 및 검증

이 예에서는 전통적인 양식을 사용하여 애플리케이션에 데이터를 보냈습니다. 그러나 많은 애플리케이션은 JavaScript 기반 프론트엔드에서 XHR 요청을 받습니다. XHR 요청 중에 `validate` 메서드를 사용하면 Laravel는 리디렉션 응답을 생성하지 않습니다. 대신, Laravel는 [모든 유효성 검사 오류를 포함하는 JSON 응답](#validation-error-response-format)을 생성합니다. 이 JSON 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
#### `@error` 지시어

`@error` [Blade](/docs/12.x/blade) 지시어를 사용하면 특정 속성에 대한 유효성 검사 오류 메시지가 있는지 빠르게 확인할 수 있습니다. `@error` 지시문 내에서 `$message` 변수를 에코하여 오류 메시지를 표시할 수 있습니다.

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

[이름이 지정된 오류 백](#named-error-bags)을 사용하는 경우 오류 백의 이름을 `@error` 지시문의 두 번째 인수로 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### 양식 다시 채우기

유효성 검사 오류로 인해 Laravel가 리디렉션 응답을 생성하면 프레임워크는 자동으로 [요청의 모든 입력을 세션에 플래시](/docs/12.x/session#flash-data)합니다. 이는 다음 요청 시 입력에 편리하게 액세스하고 사용자가 제출하려고 시도한 양식을 다시 채울 수 있도록 하기 위한 것입니다.

이전 요청에서 깜박인 입력을 검색하려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다. `old` 메서드는 [세션](/docs/12.x/session)에서 이전에 플래시된 입력 데이터를 가져옵니다.

```php
$title = $request->old('title');
```

Laravel는 글로벌 `old` 도우미도 제공합니다. [Blade 템플릿](/docs/12.x/blade) 내에서 이전 입력을 표시하는 경우 `old` 도우미를 사용하여 양식을 다시 채우는 것이 더 편리합니다. 해당 필드에 대한 이전 입력이 없으면 `null`가 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
### 선택 필드에 대한 참고 사항

기본적으로 Laravel에는 애플리케이션의 전역 미들웨어 스택에 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어가 포함되어 있습니다. 이 때문에 유효성 검사기가 `null` 값을 유효하지 않은 것으로 간주하지 않도록 하려면 "선택적" 요청 필드를 `nullable`로 표시해야 하는 경우가 많습니다. 예를 들어:

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

이 예에서는 `publish_at` 필드가 `null` 또는 유효한 날짜 표현일 수 있음을 지정합니다. `nullable` 수정자가 규칙 정의에 추가되지 않으면 유효성 검사기는 `null`를 잘못된 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
### 검증 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고 수신 HTTP 요청이 JSON 응답을 기대하는 경우 Laravel는 자동으로 오류 메시지 형식을 지정하고 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래에서는 유효성 검사 오류에 대한 JSON 응답 형식의 예를 검토할 수 있습니다. 중첩된 오류 키는 "점" 표기법 형식으로 평면화됩니다.

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
## 양식 요청 확인 (Form Request Validation)

<a name="creating-form-requests"></a>
### 양식 요청 생성

보다 복잡한 유효성 검사 시나리오의 경우 "양식 요청"을 생성할 수 있습니다. 양식 요청은 자체 유효성 검사 및 인증 논리를 캡슐화하는 사용자 지정 요청 클래스입니다. 양식 요청 클래스를 생성하려면 `make:request` Artisan CLI 명령을 사용할 수 있습니다.

```shell
php artisan make:request StorePostRequest
```

생성된 양식 요청 클래스는 `app/Http/Requests` 디렉토리에 배치됩니다. 이 디렉터리가 없으면 `make:request` 명령을 실행할 때 생성됩니다. Laravel에 의해 생성된 각 양식 요청에는 `authorize` 및 `rules`의 두 가지 방법이 있습니다.

짐작할 수 있듯이 `authorize` 메서드는 현재 인증된 사용자가 요청에 표시된 작업을 수행할 수 있는지 확인하는 역할을 담당하는 반면, `rules` 메서드는 요청 데이터에 적용해야 하는 유효성 검사 규칙을 반환합니다.

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
> `rules` 메서드의 서명 내에서 필요한 종속성을 유형 힌트로 지정할 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 해결됩니다.

그렇다면 유효성 검사 규칙은 어떻게 평가됩니까? 당신이 해야 할 일은 컨트롤러 메소드에 대한 요청을 유형 힌트하는 것뿐입니다. 들어오는 양식 요청은 컨트롤러 메서드가 호출되기 전에 유효성이 검사됩니다. 즉, 유효성 검사 논리로 컨트롤러를 복잡하게 만들 필요가 없습니다.

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

유효성 검사에 실패하면 사용자를 이전 위치로 다시 보내기 위한 리디렉션 응답이 생성됩니다. 오류는 세션에도 플래시되어 표시할 수 있습니다. 요청이 XHR 요청인 경우 422 상태 코드가 포함된 HTTP 응답이 [JSON 유효성 검사 오류 표현](#validation-error-response-format)을 포함하여 사용자에게 반환됩니다.

> [!NOTE]
> Inertia 기반 Laravel 프론트엔드에 실시간 양식 요청 확인을 추가해야 합니까? [Laravel 예지](/docs/12.x/precognition)를 확인해보세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 검증 수행

초기 검증이 완료된 후 추가 검증을 수행해야 하는 경우가 있습니다. 양식 요청의 `after` 메소드를 사용하여 이를 수행할 수 있습니다.

`after` 메소드는 검증이 완료된 후 호출될 콜러블 또는 클로저의 배열을 반환해야 합니다. 지정된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 수신하므로 필요한 경우 추가 오류 메시지를 표시할 수 있습니다.

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

언급한 대로 `after` 메서드에서 반환된 배열에는 호출 가능한 클래스가 포함될 수도 있습니다. 이러한 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 수신합니다.

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
#### 첫 번째 검증 실패 시 중지

요청 클래스에 `stopOnFirstFailure` 속성을 추가하면 단일 유효성 검사가 실패하면 모든 속성의 유효성 검사를 중지해야 한다고 유효성 검사기에 알릴 수 있습니다.

```php
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 사용자 지정

양식 요청 유효성 검사가 실패하면 사용자를 이전 위치로 다시 보내기 위한 리디렉션 응답이 생성됩니다. 그러나 이 동작을 자유롭게 사용자 지정할 수 있습니다. 이렇게 하려면 양식 요청에 `$redirect` 속성을 정의하세요.

```php
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

또는 사용자를 명명된 라우트로 리디렉션하려는 경우 대신 `$redirectRoute` 속성을 정의할 수 있습니다.

```php
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
### 양식 요청 승인

양식 요청 클래스에는 `authorize` 메소드도 포함되어 있습니다. 이 방법 내에서 인증된 사용자가 실제로 특정 리소스를 업데이트할 권한이 있는지 확인할 수 있습니다. 예를 들어 사용자가 업데이트하려는 블로그 댓글을 실제로 소유하고 있는지 확인할 수 있습니다. 아마도 다음 방법 내에서 [승인 게이트 및 정책](/docs/12.x/authorization)과 상호 작용하게 될 것입니다.

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

모든 양식 요청은 기본 Laravel 요청 클래스를 확장하므로 `user` 메소드를 사용하여 현재 인증된 사용자에 액세스할 수 있습니다. 또한 위 예제에서 `route` 메서드에 대한 호출을 확인하세요. 이 메소드는 호출되는 라우트에 정의된 URI 매개변수(예: 아래 예의 `{comment}` 매개변수)에 대한 액세스 권한을 부여합니다.

```php
Route::post('/comment/{comment}');
```

따라서 애플리케이션이 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 활용하는 경우 확인된 모델을 요청의 속성으로 액세스하여 코드를 더욱 간결하게 만들 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

`authorize` 메서드가 `false`를 반환하는 경우 403 상태 코드가 포함된 HTTP 응답이 자동으로 반환되고 컨트롤러 메서드가 실행되지 않습니다.

애플리케이션의 다른 부분에서 요청에 대한 인증 논리를 처리하려는 경우 `authorize` 메서드를 완전히 제거하거나 간단히 `true`를 반환할 수 있습니다.

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
> `authorize` 메서드의 서명 내에서 필요한 종속성을 유형 힌트로 지정할 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 사용자 지정

`messages` 메소드를 재정의하여 양식 요청에 사용되는 오류 메시지를 사용자 지정할 수 있습니다. 이 메소드는 속성/규칙 쌍의 배열과 해당 오류 메시지를 반환해야 합니다.

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
#### 검증 속성 사용자 지정

Laravel의 내장 유효성 검사 규칙 오류 메시지 중 상당수에는 `:attribute` 자리 표시자가 포함되어 있습니다. 유효성 검사 메시지의 `:attribute` 자리 표시자를 사용자 지정 속성 이름으로 바꾸려면 `attributes` 메서드를 재정의하여 사용자 지정 이름을 지정할 수 있습니다. 이 메소드는 속성/이름 쌍의 배열을 반환해야 합니다.

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
### 검증을 위한 입력 준비

유효성 검사 규칙을 적용하기 전에 요청의 데이터를 준비하거나 삭제해야 하는 경우 `prepareForValidation` 메서드를 사용할 수 있습니다.

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

마찬가지로 유효성 검사가 완료된 후 요청 데이터를 정규화해야 하는 경우 `passedValidation` 메서드를 사용할 수 있습니다.

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
## 수동으로 유효성 검사기 생성 (Manually Creating Validators)

요청에 `validate` 메서드를 사용하지 않으려면 `Validator` [facade](/docs/12.x/facades)를 사용하여 수동으로 유효성 검사기 인스턴스를 생성할 수 있습니다. 파사드의 `make` 메소드는 새로운 유효성 검사기 인스턴스를 생성합니다:

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

`make` 메소드에 전달된 첫 번째 인수는 검증 중인 데이터입니다. 두 번째 인수는 데이터에 적용되어야 하는 유효성 검사 규칙의 배열입니다.

요청 유효성 검사가 실패했는지 확인한 후 `withErrors` 메서드를 사용하여 오류 메시지를 세션에 플래시할 수 있습니다. 이 방법을 사용하면 리디렉션 후 `$errors` 변수가 뷰와 자동으로 공유되므로 해당 변수를 사용자에게 쉽게 다시 표시할 수 있습니다. `withErrors` 메서드는 유효성 검사기인 `MessageBag` 또는 PHP `array`를 허용합니다.

#### 첫 번째 검증 실패 시 중지

`stopOnFirstFailure` 메소드는 단일 검증 실패가 발생하면 모든 속성 검증을 중지해야 함을 검증자에게 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
### 자동 리디렉션

유효성 검사기 인스턴스를 수동으로 생성하고 싶지만 여전히 HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션을 활용하려는 경우 기존 유효성 검사기 인스턴스에서 `validate` 메서드를 호출할 수 있습니다. 유효성 검사에 실패하면 사용자가 자동으로 리디렉션되거나, XHR 요청의 경우 [JSON 응답이 반환됩니다](#validation-error-response-format):

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

유효성 검사가 실패할 경우 `validateWithBag` 메서드를 사용하여 [이름이 지정된 오류 백](#named-error-bags)에 오류 메시지를 저장할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
### 명명된 오류 백

단일 페이지에 여러 양식이 있는 경우 유효성 검사 오류가 포함된 `MessageBag`의 이름을 지정하여 특정 양식에 대한 오류 메시지를 검색할 수 있습니다. 이를 달성하려면 이름을 `withErrors`의 두 번째 인수로 전달하십시오.

```php
return redirect('/register')->withErrors($validator, 'login');
```

그런 다음 `$errors` 변수에서 명명된 `MessageBag` 인스턴스에 액세스할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 사용자 지정

필요한 경우 Laravel에서 제공하는 기본 오류 메시지 대신 유효성 검사기 인스턴스가 사용해야 하는 사용자 지정 오류 메시지를 제공할 수 있습니다. 사용자 지정 메시지를 지정하는 방법에는 여러 가지가 있습니다. 먼저, 사용자 지정 메시지를 `Validator::make` 메소드의 세 번째 인수로 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

이 예에서 `:attribute` 자리 표시자는 유효성 검사 중인 필드의 실제 이름으로 대체됩니다. 유효성 검사 메시지에 다른 자리 표시자를 활용할 수도 있습니다. 예를 들어:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 주어진 속성에 대한 사용자 지정 메시지 지정

때로는 특정 속성에 대해서만 사용자 지정 오류 메시지를 지정하고 싶을 수도 있습니다. "점" 표기법을 사용하여 그렇게 할 수 있습니다. 먼저 속성 이름을 지정한 다음 규칙을 지정합니다.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
#### 사용자 지정 속성 값 지정

Laravel에 내장된 오류 메시지 중 다수에는 검증 중인 필드 또는 속성의 이름으로 대체되는 `:attribute` 자리 표시자가 포함되어 있습니다. 특정 필드에 대해 이러한 자리 표시자를 대체하는 데 사용되는 값을 사용자 지정하려면 사용자 지정 속성 배열을 `Validator::make` 메소드의 네 번째 인수로 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
### 추가 검증 수행

초기 검증이 완료된 후 추가 검증을 수행해야 하는 경우가 있습니다. 유효성 검사기의 `after` 메서드를 사용하여 이를 수행할 수 있습니다. `after` 메소드는 검증이 완료된 후 호출될 콜러블 배열이나 클로저를 허용합니다. 지정된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 수신하므로 필요한 경우 추가 오류 메시지를 표시할 수 있습니다.

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

언급한 바와 같이, `after` 메소드는 콜러블 배열도 허용합니다. 이는 "검증 후" 로직이 `__invoke` 메소드를 통해 `Illuminate\Validation\Validator` 인스턴스를 수신하는 호출 가능 클래스에 캡슐화되어 있는 경우 특히 편리합니다.

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
## 검증된 입력 작업 (Working With Validated Input)

양식 요청 또는 수동으로 생성된 유효성 검사기 인스턴스를 사용하여 들어오는 요청 데이터의 유효성을 검사한 후 실제로 유효성 검사를 거친 들어오는 요청 데이터를 검색할 수 있습니다. 이는 여러 가지 방법으로 수행할 수 있습니다. 먼저, 양식 요청이나 유효성 검사기 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메소드는 검증된 데이터 배열을 반환합니다.

```php
$validated = $request->validated();

$validated = $validator->validated();
```

또는 양식 요청이나 유효성 검사기 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메소드는 `Illuminate\Support\ValidatedInput`의 인스턴스를 반환합니다. 이 객체는 검증된 데이터의 하위 집합 또는 검증된 데이터의 전체 배열을 검색하기 위해 `only`, `except` 및 `all` 메서드를 노출합니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

또한 `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복되고 액세스될 수 있습니다.

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

검증된 데이터에 추가 필드를 추가하려면 `merge` 메소드를 호출하면 됩니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

검증된 데이터를 [컬렉션](/docs/12.x/collections) 인스턴스로 검색하려면 `collect` 메소드를 호출할 수 있습니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
## 오류 메시지 작업 (Working With Error Messages)

`Validator` 인스턴스에서 `errors` 메서드를 호출하면 오류 메시지 작업을 위한 다양하고 편리한 메서드가 있는 `Illuminate\Support\MessageBag` 인스턴스가 수신됩니다. 모든 뷰에서 자동으로 사용할 수 있는 `$errors` 변수도 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 필드에 대한 첫 번째 오류 메시지 검색

특정 필드에 대한 첫 번째 오류 메시지를 검색하려면 `first` 메서드를 사용하세요.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
#### 필드에 대한 모든 오류 메시지 검색

특정 필드에 대한 모든 메시지의 배열을 검색해야 하는 경우 `get` 메서드를 사용하세요.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

배열 양식 필드의 유효성을 검사하는 경우 `*` 문자를 사용하여 각 배열 요소에 대한 모든 메시지를 검색할 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드에 대한 모든 오류 메시지 검색

모든 필드에 대한 모든 메시지의 배열을 검색하려면 `all` 메소드를 사용하십시오.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
#### 필드에 대한 메시지가 존재하는지 확인

`has` 메소드는 특정 필드에 오류 메시지가 있는지 확인하는 데 사용될 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
### 언어 파일에 사용자 지정 메시지 지정

Laravel의 내장 유효성 검사 규칙에는 각각 애플리케이션의 `lang/en/validation.php` 파일에 있는 오류 메시지가 있습니다. 응용 프로그램에 `lang` 디렉터리가 없으면 `lang:publish` Artisan 명령을 사용하여 Laravel에 디렉터리를 생성하도록 지시할 수 있습니다.

`lang/en/validation.php` 파일 내에서 각 유효성 검사 규칙에 대한 번역 항목을 찾을 수 있습니다. 애플리케이션의 필요에 따라 이러한 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

또한 이 파일을 다른 언어 디렉터리에 복사하여 애플리케이션 언어에 대한 메시지를 번역할 수도 있습니다. Laravel 현지화에 대해 자세히 알아보려면 전체 [현지화 문서](/docs/12.x/localization)를 확인하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되지 않습니다. Laravel의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다.

<a name="custom-messages-for-specific-attributes"></a>
#### 특정 속성에 대한 사용자 지정 메시지

애플리케이션의 유효성 검사 언어 파일 내에서 지정된 속성 및 규칙 조합에 사용되는 오류 메시지를 사용자 지정할 수 있습니다. 이렇게 하려면 애플리케이션 `lang/xx/validation.php` 언어 파일의 `custom` 배열에 메시지 사용자 지정를 추가하세요.

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에 속성 지정

Laravel에 내장된 오류 메시지 중 다수에는 검증 중인 필드 또는 속성의 이름으로 대체되는 `:attribute` 자리 표시자가 포함되어 있습니다. 유효성 검사 메시지의 `:attribute` 부분을 사용자 지정 값으로 바꾸려면 `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 사용자 지정 속성 이름을 지정할 수 있습니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되지 않습니다. Laravel의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에 값 지정

Laravel의 내장 유효성 검사 규칙 오류 메시지 중 일부에는 요청 속성의 현재 값으로 대체되는 `:value` 자리 표시자가 포함되어 있습니다. 그러나 때때로 유효성 검사 메시지의 `:value` 부분을 값의 사용자 지정 표현으로 바꿔야 할 수도 있습니다. 예를 들어, `payment_type`의 값이 `cc`인 경우 신용 카드 번호가 필요함을 지정하는 다음 규칙을 고려하십시오.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

이 유효성 검사 규칙이 실패하면 다음과 같은 오류 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

`cc`를 결제 유형 값으로 표시하는 대신 `values` 배열을 정의하여 `lang/xx/validation.php` 언어 파일에 보다 사용자 친화적인 값 표현을 지정할 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되지 않습니다. Laravel의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다.

이 값을 정의한 후 유효성 검사 규칙은 다음과 같은 오류 메시지를 생성합니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## 사용 가능한 검증 규칙 (Available Validation Rules)

다음은 사용 가능한 모든 유효성 검사 규칙과 해당 기능의 목록입니다.

<style>{`
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
`}</style>

#### 부울

<div class="collection-method-list" markdown="1">

[수락됨](#rule-accepted)
[허용되는 경우](#rule-accepted-if)
[부울](#rule-boolean)
[거부됨](#rule-declined)
[거절된 경우](#rule-declined-if)

</div>

#### 문자열

<div class="collection-method-list" markdown="1">

[활성 URL](#rule-active-url)
[알파](#rule-alpha)
[알파 대시](#rule-alpha-dash)
[영숫자](#rule-alpha-num)
[아스키](#rule-ascii)
[확인됨](#rule-confirmed)
[현재 비밀번호](#rule-current-password)
[다른](#rule-different)
[다음으로 시작하지 않음](#rule-doesnt-start-with)
[다음으로 끝나지 않음](#rule-doesnt-end-with)
[이메일](#rule-email)
[다음으로 끝남](#rule-ends-with)
[열거형](#rule-enum)
[헥스 컬러](#rule-hex-color)
[인](#rule-in)
[IP 주소](#rule-ip)
[JSON](#rule-json)
[소문자](#rule-lowercase)
[MAC 주소](#rule-mac)
[최대](#rule-max)
[최소](#rule-min)
[포함되지 않음](#rule-not-in)
[정규식](#rule-regex)
[정규식이 아님](#rule-not-regex)
[동일](#rule-same)
[사이즈](#rule-size)
[다음으로 시작](#rule-starts-with)
[문자열](#rule-string)
[대문자](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

#### 숫자

<div class="collection-method-list" markdown="1">

[사이](#rule-between)
[10진수](#rule-decimal)
[다른](#rule-different)
[숫자](#rule-digits)
[자릿수 사이](#rule-digits-between)
[보다 큼](#rule-gt)
[보다 크거나 같음](#rule-gte)
[정수](#rule-integer)
[미만](#rule-lt)
[작거나 같음](#rule-lte)
[최대](#rule-max)
[최대 자릿수](#rule-max-digits)
[최소](#rule-min)
[최소 자릿수](#rule-min-digits)
[복수](#rule-multiple-of)
[숫자](#rule-numeric)
[동일](#rule-same)
[사이즈](#rule-size)

</div>

#### 배열

<div class="collection-method-list" markdown="1">

[어레이](#rule-array)
[사이](#rule-between)
[포함](#rule-contains)
[포함하지 않음](#rule-doesnt-contain)
[고유함](#rule-distinct)
[어레이 내](#rule-in-array)
[배열 키](#rule-in-array-keys)
[목록](#rule-list)
[최대](#rule-max)
[최소](#rule-min)
[사이즈](#rule-size)

</div>

#### 날짜

<div class="collection-method-list" markdown="1">

[이후](#rule-after)
[이후 또는 같음](#rule-after-or-equal)
[전](#rule-before)
[이전 또는 같음](#rule-before-or-equal)
[날짜](#rule-date)
[날짜가 같음](#rule-date-equals)
[날짜 형식](#rule-date-format)
[다른](#rule-different)
[시간대](#rule-timezone)

</div>

#### 파일

<div class="collection-method-list" markdown="1">

[사이](#rule-between)
[치수](#rule-dimensions)
[인코딩](#rule-encoding)
[확장](#rule-extensions)
[파일](#rule-file)
[이미지](#rule-image)
[최대](#rule-max)
[MIME 유형](#rule-mimetypes)
[파일 확장자별 MIME 유형](#rule-mimes)
[사이즈](#rule-size)

</div>

#### 데이터 베이스

<div class="collection-method-list" markdown="1">

[존재함](#rule-exists)
[고유](#rule-unique)

</div>

#### 유용

<div class="collection-method-list" markdown="1">

[다음 중 하나](#rule-anyof)
[보석](#rule-bail)
[제외](#rule-exclude)
[다음 경우 제외](#rule-exclude-if)
[제외 제외](#rule-exclude-unless)
[다음으로 제외](#rule-exclude-with)
[없이 제외](#rule-exclude-without)
[채워짐](#rule-filled)
[누락](#rule-missing)
[누락된 경우](#rule-missing-if)
[누락되지 않은 경우](#rule-missing-unless)
[누락됨](#rule-missing-with)
[모두 누락됨](#rule-missing-with-all)
[널 입력 가능](#rule-nullable)
[현재](#rule-present)
[현재의 경우](#rule-present-if)
[현재가 아니면](#rule-present-unless)
[다음과 함께 제공](#rule-present-with)
[모두와 함께 선물](#rule-present-with-all)
[금지](#rule-prohibited)
[금지되는 경우](#rule-prohibited-if)
[동의 시 금지](#rule-prohibited-if-accepted)
[거부시 금지](#rule-prohibited-if-declined)
[금지](#rule-prohibited-unless)
[금지](#rule-prohibits)
[필수](#rule-required)
[필수인 경우](#rule-required-if)
[수락하는 경우 필수](#rule-required-if-accepted)
[거부시 필수](#rule-required-if-declined)
[필수 사항](#rule-required-unless)
[필수](#rule-required-with)
[모두 필수](#rule-required-with-all)
[없이 필수](#rule-required-without)
[모두 제외 필수](#rule-required-without-all)
[필수 배열 키](#rule-required-array-keys)
[가끔](#validating-when-present)

</div>

<a name="rule-accepted"></a>
#### 수락됨

검증 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true` 또는 `"true"`여야 합니다. 이는 "서비스 약관" 동의 또는 유사한 필드를 확인하는 데 유용합니다.

<a name="rule-accepted-if"></a>
#### allowed_if:anotherfield,값,...

유효성 검사 중인 다른 필드가 지정된 값과 같은 경우 유효성 검사 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true` 또는 `"true"`여야 합니다. 이는 "서비스 약관" 동의 또는 유사한 필드를 확인하는 데 유용합니다.

<a name="rule-active-url"></a>
#### 활성_URL

유효성 검사 중인 필드에는 `dns_get_record` PHP 함수에 따라 유효한 A 또는 AAAA 레코드가 있어야 합니다. 제공된 URL의 호스트 이름은 `dns_get_record`에 전달되기 전에 `parse_url` PHP 함수를 사용하여 추출됩니다.

<a name="rule-after"></a>
#### 이후:_date_

유효성 검사 중인 필드는 지정된 날짜 이후의 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 `strtotime` PHP 함수로 전달됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

`strtotime`에서 평가할 날짜 문자열을 전달하는 대신 날짜와 비교할 다른 필드를 지정할 수 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```

편의를 위해 `date` 규칙 빌더를 사용하여 날짜 기반 규칙을 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

`afterToday` 및 `todayOrAfter` 메소드는 날짜를 유창하게 표현하는 데 사용할 수 있으며 각각 오늘 이후, 오늘 또는 이후여야 합니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
#### 이후\_또는\_equal:_date_

유효성 검사 중인 필드는 지정된 날짜 이후의 값이어야 합니다. 자세한 내용은 [이후](#rule-after) 규칙을 참조하세요.

편의를 위해 `date` 규칙 빌더를 사용하여 날짜 기반 규칙을 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
#### 아무거나

`Rule::anyOf` 유효성 검사 규칙을 사용하면 유효성 검사 중인 필드가 지정된 유효성 검사 규칙 세트 중 하나를 충족해야 함을 지정할 수 있습니다. 예를 들어, 다음 규칙은 `username` 필드가 이메일 주소이거나 길이가 6자 이상인 영숫자 문자열(대시 포함)인지 확인합니다.

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
#### 알파

유효성 검사 대상 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함된 전체 유니코드 알파벳 문자여야 합니다.

이 유효성 검사 규칙을 ASCII 범위(`a-z` 및 `A-Z`)의 문자로 제한하려면 유효성 검사 규칙에 `ascii` 옵션을 제공할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
#### alpha_dash

유효성 검사 대상 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 전체 유니코드 영숫자 문자와 ASCII 대시(`-`) 및 ASCII 밑줄(`_`)이어야 합니다.

이 유효성 검사 규칙을 ASCII 범위(`a-z`, `A-Z` 및 `0-9`)의 문자로 제한하려면 유효성 검사 규칙에 `ascii` 옵션을 제공할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
#### alpha_num

유효성 검사 대상 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) 및 [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 전체 유니코드 영숫자 문자여야 합니다.

이 유효성 검사 규칙을 ASCII 범위(`a-z`, `A-Z` 및 `0-9`)의 문자로 제한하려면 유효성 검사 규칙에 `ascii` 옵션을 제공할 수 있습니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
#### 정렬

검증 중인 필드는 PHP `array`여야 합니다.

`array` 규칙에 추가 값이 제공되면 입력 배열의 각 키가 규칙에 제공된 값 목록 내에 있어야 합니다. 다음 예에서 입력 배열의 `admin` 키는 `array` 규칙에 제공된 값 목록에 포함되어 있지 않으므로 유효하지 않습니다.

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

일반적으로 배열 내에 존재할 수 있는 배열 키를 항상 지정해야 합니다.

<a name="rule-ascii"></a>
#### 아스키

유효성 검사 대상 필드는 전체가 7비트 ASCII 문자여야 합니다.

<a name="rule-bail"></a>
#### 보석

첫 번째 유효성 검사가 실패한 후 해당 필드에 대한 유효성 검사 규칙 실행을 중지합니다.

`bail` 규칙은 유효성 검사에 실패할 경우에만 특정 필드의 유효성 검사를 중지하지만, `stopOnFirstFailure` 메서드는 단일 유효성 검사가 실패하면 모든 속성의 유효성 검사를 중지해야 한다고 유효성 검사기에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
#### 이전:_date_

유효성 검사 중인 필드는 지정된 날짜 이전의 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 PHP `strtotime` 함수로 전달됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로 유효성 검사 중인 다른 필드의 이름이 `date` 값으로 제공될 수 있습니다.

편의를 위해 `date` 규칙 빌더를 사용하여 날짜 기반 규칙을 구성할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

`beforeToday` 및 `todayOrBefore` 메소드는 날짜를 유창하게 표현하는 데 사용할 수 있으며 각각 오늘 이전, 오늘 또는 이전이어야 합니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
#### 이전\_또는\_equal:_date_

유효성 검사 중인 필드는 지정된 날짜보다 이전이거나 같은 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환하기 위해 PHP `strtotime` 함수로 전달됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로 유효성 검사 중인 다른 필드의 이름이 `date` 값으로 제공될 수 있습니다.

편의를 위해 `date` 규칙 빌더를 사용하여 날짜 기반 규칙을 구성할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
#### :_min_,_max_ 사이

유효성 검사 중인 필드의 크기는 지정된 _min_과 _max_(포함) 사이여야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-boolean"></a>
#### 부울

유효성 검사 중인 필드는 부울로 캐스팅될 수 있어야 합니다. 허용되는 입력은 `true`, `false`, `1`, `0`, `"1"` 및 `"0"`입니다.

`strict` 매개변수를 사용하면 해당 값이 `true` 또는 `false`인 경우에만 필드가 유효한 것으로 간주할 수 있습니다.

```php
'foo' => 'boolean:strict'
```

<a name="rule-confirmed"></a>
#### 확인됨

유효성 검사 중인 필드에는 `{field}_confirmation`와 일치하는 필드가 있어야 합니다. 예를 들어 유효성 검사 중인 필드가 `password`인 경우 일치하는 `password_confirmation` 필드가 입력에 있어야 합니다.

사용자 지정 확인 필드 이름을 전달할 수도 있습니다. 예를 들어, `confirmed:repeat_username`는 `repeat_username` 필드가 유효성 검사 중인 필드와 일치할 것으로 예상합니다.

<a name="rule-contains"></a>
#### 포함:_foo_,_bar_,...

유효성 검사 대상 필드는 지정된 매개변수 값을 모두 포함하는 배열이어야 합니다. 이 규칙에서는 배열을 `implode`해야 하는 경우가 많기 때문에 `Rule::contains` 메서드를 사용하여 규칙을 원활하게 구성할 수 있습니다.

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
#### dont_contain:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 매개변수 값을 전혀 포함하지 않는 배열이어야 합니다. 이 규칙에서는 배열을 `implode`해야 하는 경우가 많기 때문에 `Rule::doesntContain` 메서드를 사용하여 규칙을 원활하게 구성할 수 있습니다.

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
#### 현재_비밀번호

검증 중인 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 매개변수를 사용하여 [인증 가드](/docs/12.x/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
#### 날짜

유효성 검사 중인 필드는 `strtotime` PHP 함수에 따라 유효한 비상대 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

유효성 검사 중인 필드는 지정된 날짜와 동일해야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되기 위해 PHP `strtotime` 함수로 전달됩니다.

<a name="rule-date-format"></a>
#### 날짜_형식:_format_,...

유효성 검사 중인 필드는 지정된 _formats_ 중 하나와 일치해야 합니다. 필드 유효성을 검사할 때 `date` 또는 `date_format` 중 하나만 사용해야 하며 둘 다 사용할 수는 없습니다. 이 유효성 검사 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 형식을 지원합니다.

편의를 위해 `date` 규칙 빌더를 사용하여 날짜 기반 규칙을 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
#### 십진수:_min_,_max_

검증 중인 필드는 숫자여야 하며 지정된 소수 자릿수를 포함해야 합니다.

```php
// Must have exactly two decimal places (9.99)...
'price' => 'decimal:2'

// Must have between 2 and 4 decimal places...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
#### 거절하다

검증 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false` 또는 `"false"`여야 합니다.

<a name="rule-declined-if"></a>
#### 거부됨_if:anotherfield,값,...

유효성 검사 중인 다른 필드가 지정된 값과 같은 경우 유효성 검사 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false` 또는 `"false"`여야 합니다.

<a name="rule-different"></a>
#### 다른:_field_

유효성 검사 중인 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### 숫자:_value_

검증 중인 정수의 정확한 길이는 _value_여야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 중인 정수는 지정된 _min_과 _max_ 사이의 길이를 가져야 합니다.

<a name="rule-dimensions"></a>
#### 치수

검증 중인 파일은 규칙 매개변수에 지정된 치수 제약 조건을 충족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

사용 가능한 제약 조건은 _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_입니다.

_ratio_ 제약 조건은 너비를 높이로 나눈 값으로 표현되어야 합니다. 이는 `3/2`와 같은 분수 또는 `1.5`와 같은 부동소수점으로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

이 규칙에는 여러 인수가 필요하므로 `Rule::dimensions` 메서드를 사용하여 규칙을 유창하게 구성하는 것이 더 편리한 경우가 많습니다.

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

<a name="rule-distinct"></a>
#### 별개의

배열의 유효성을 검사할 때 유효성 검사 중인 필드에 중복된 값이 있어서는 안 됩니다.

```php
'foo.*.id' => 'distinct'
```

Distinct는 기본적으로 느슨한 변수 비교를 사용합니다. 엄격한 비교를 사용하려면 유효성 검사 규칙 정의에 `strict` 매개변수를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:strict'
```

규칙이 대문자 사용 차이를 무시하도록 확인 규칙의 인수에 `ignore_case`를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
#### :_foo_,_bar_,...로 시작_하지 않음

유효성 검사 중인 필드는 지정된 값 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### dont_end_with:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 값 중 하나로 끝나서는 안 됩니다.

<a name="rule-email"></a>
#### 이메일

검증 중인 필드는 이메일 주소 형식이어야 합니다. 이 유효성 검사 규칙은 이메일 주소 유효성을 검사하기 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 활용합니다. 기본적으로 `RFCValidation` 유효성 검사기가 적용되지만 다른 유효성 검사 스타일도 적용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

위의 예에서는 `RFCValidation` 및 `DNSCheckValidation` 유효성 검사를 적용합니다. 적용할 수 있는 유효성 검사 스타일의 전체 목록은 다음과 같습니다.

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 주소의 유효성을 검사합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 유효성을 검사합니다. 경고가 발견되면 실패합니다(예: 후행 마침표 및 여러 개의 연속 마침표).
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인하세요.
- `spoof`: `SpoofCheckValidation` - 이메일 주소에 동형이의어 또는 사기성 유니코드 문자가 포함되어 있지 않은지 확인하세요.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 기능에 따라 이메일 주소가 유효한지 확인하세요.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 기능에 따라 이메일 주소가 유효한지 확인하고 일부 유니코드 문자를 허용합니다.

</div>

편의를 위해 Fluent Rule Builder를 사용하여 이메일 유효성 검사 규칙을 구축할 수 있습니다.

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
> `dns` 및 `spoof` 검사기에는 PHP `intl` 확장이 필요합니다.

<a name="rule-encoding"></a>
#### 인코딩:*encoding_type*

유효성 검사 중인 필드는 지정된 문자 인코딩과 일치해야 합니다. 이 규칙은 PHP의 `mb_check_encoding` 함수를 사용하여 지정된 파일 또는 문자열 값의 인코딩을 확인합니다. 편의를 위해 Laravel의 흐름 파일 규칙 빌더를 사용하여 `encoding` 규칙을 구성할 수 있습니다.

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
#### 끝_with:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### 열거형

`Enum` 규칙은 유효성 검사 중인 필드에 유효한 열거형 값이 포함되어 있는지 여부를 확인하는 클래스 기반 규칙입니다. `Enum` 규칙은 열거형의 이름을 유일한 생성자 인수로 허용합니다. 기본 값의 유효성을 검사할 때 지원되는 Enum이 `Enum` 규칙에 제공되어야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

`Enum` 규칙의 `only` 및 `except` 메서드는 유효한 것으로 간주되어야 하는 열거형 사례를 제한하는 데 사용될 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

`when` 메소드는 `Enum` 규칙을 조건부로 수정하는 데 사용될 수 있습니다.

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
#### 들어오지 못하게 하다

유효성 검사 중인 필드는 `validate` 및 `validated` 메서드에서 반환된 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### 제외_if:_anotherfield_,_값_

_anotherfield_ 필드가 _value_와 같은 경우 유효성 검사 중인 필드는 `validate` 및 `validated` 메서드에서 반환된 요청 데이터에서 제외됩니다.

복잡한 조건부 제외 논리가 필요한 경우 `Rule::excludeIf` 방법을 활용할 수 있습니다. 이 메소드는 부울 또는 클로저를 허용합니다. 클로저가 제공되면 클로저는 `true` 또는 `false`를 반환하여 유효성 검사 중인 필드를 제외해야 하는지 여부를 나타내야 합니다.

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
#### 제외_unless:_anotherfield_,_값_

유효성 검사 중인 필드는 _anotherfield_의 필드가 _value_와 같지 않으면 `validate` 및 `validated` 메서드에서 반환된 요청 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`)인 경우 비교 필드가 `null`이거나 비교 필드가 요청 데이터에서 누락되지 않는 한 유효성 검사 중인 필드가 제외됩니다.

<a name="rule-exclude-with"></a>
#### 제외_with:_anotherfield_

유효성 검사 중인 필드는 _anotherfield_ 필드가 있는 경우 `validate` 및 `validated` 메서드에서 반환된 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### 제외_without:_anotherfield_

유효성 검사 중인 필드는 _anotherfield_ 필드가 없는 경우 `validate` 및 `validated` 메서드에서 반환된 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### 존재:_table_,_column_

검증 중인 필드는 지정된 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### 존재 규칙의 기본 사용법

```php
'state' => 'exists:states'
```

`column` 옵션을 지정하지 않으면 필드 이름이 사용됩니다. 따라서 이 경우 규칙은 `states` 데이터베이스 테이블에 요청의 `state` 속성 값과 일치하는 `state` 열 값이 있는 레코드가 포함되어 있는지 확인합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 지정 열 이름 지정

데이터베이스 테이블 이름 뒤에 배치하여 유효성 검사 규칙에서 사용해야 하는 데이터베이스 열 이름을 명시적으로 지정할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

경우에 따라 `exists` 쿼리에 사용할 특정 데이터베이스 연결을 지정해야 할 수도 있습니다. 테이블 이름 앞에 연결 이름을 추가하여 이를 수행할 수 있습니다.

```php
'email' => 'exists:connection.staff,email'
```

테이블 이름을 직접 지정하는 대신 테이블 이름을 결정하는 데 사용해야 하는 Eloquent 모델을 지정할 수 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

유효성 검사 규칙에 의해 실행되는 쿼리를 사용자 지정하려면 `Rule` 클래스를 사용하여 규칙을 유연하게 정의할 수 있습니다. 이 예에서는 `|` 문자를 사용하여 구분하는 대신 유효성 검사 규칙을 배열로 지정합니다.

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

열 이름을 `exists` 메서드의 두 번째 인수로 제공하여 `Rule::exists` 메서드에서 생성된 `exists` 규칙에서 사용해야 하는 데이터베이스 열 이름을 명시적으로 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

때로는 데이터베이스에 값 배열이 존재하는지 확인하고 싶을 수도 있습니다. 유효성을 검사하는 필드에 `exists` 및 [array](#rule-array) 규칙을 모두 추가하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

이 두 규칙이 모두 필드에 할당되면 Laravel는 자동으로 단일 쿼리를 작성하여 지정된 모든 값이 지정된 테이블에 존재하는지 확인합니다.

<a name="rule-extensions"></a>
#### 확장자:_foo_,_bar_,...

유효성 검사 중인 파일에는 나열된 확장자 중 하나에 해당하는 사용자 할당 확장자가 있어야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 사용자가 할당한 확장자만으로 파일 유효성을 검사하는 데 의존해서는 안 됩니다. 이 규칙은 일반적으로 항상 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 함께 사용해야 합니다.

<a name="rule-file"></a>
#### 파일

검증 중인 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
#### 채우는

유효성 검사 중인 필드는 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
#### gt:_field_

유효성 검사 중인 필드는 지정된 _field_ 또는 _value_보다 커야 합니다. 두 필드는 동일한 유형이어야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 규칙을 사용하여 평가됩니다.

<a name="rule-gte"></a>
#### gte:_field_

유효성 검사 중인 필드는 지정된 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 동일한 유형이어야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 규칙을 사용하여 평가됩니다.

<a name="rule-hex-color"></a>
#### hex_color

유효성 검사 중인 필드에는 [16진수](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값이 포함되어야 합니다.

<a name="rule-image"></a>
#### 영상

유효성 검사 대상 파일은 이미지(jpg, jpeg, png, bmp, gif 또는 webp)여야 합니다.

> [!WARNING]
> 기본적으로 이미지 규칙은 XSS 취약점 가능성으로 인해 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 하는 경우 `allow_svg` 지시문을 `image` 규칙(`image:allow_svg`)에 제공할 수 있습니다.

<a name="rule-in"></a>
#### :_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 값 목록에 포함되어야 합니다. 이 규칙에서는 배열을 `implode`해야 하는 경우가 많기 때문에 `Rule::in` 메서드를 사용하여 규칙을 원활하게 구성할 수 있습니다.

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

`in` 규칙이 `array` 규칙과 결합되면 입력 배열의 각 값이 `in` 규칙에 제공된 값 목록 내에 있어야 합니다. 다음 예에서 입력 배열의 `LAS` 공항 코드는 `in` 규칙에 제공된 공항 목록에 포함되어 있지 않으므로 유효하지 않습니다.

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

유효성 검사 중인 필드는 _anotherfield_의 값에 있어야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

유효성 검사 대상 필드는 주어진 _values_ 중 하나 이상을 배열 내의 키로 갖는 배열이어야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
#### 정수

검증 중인 필드는 정수여야 합니다.

`strict` 매개변수를 사용하면 해당 유형이 `integer`인 경우에만 필드가 유효한 것으로 간주할 수 있습니다. 정수 값이 있는 문자열은 유효하지 않은 것으로 간주됩니다.

```php
'age' => 'integer:strict'
```

> [!WARNING]
> 이 유효성 검사 규칙은 입력이 "정수" 변수 유형인지 확인하지 않고 입력이 PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 유형인지만 확인합니다. 입력이 숫자인지 확인해야 하는 경우 이 규칙을 [`numeric` 확인 규칙](#rule-numeric)과 함께 사용하세요.

<a name="rule-ip"></a>
#### 아이피

검증 중인 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
#### IPv4

검증 중인 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
#### IPv6

검증 중인 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
#### JSON

검증 중인 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
#### lt:_field_

유효성 검사 중인 필드는 지정된 _field_보다 작아야 합니다. 두 필드는 동일한 유형이어야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 규칙을 사용하여 평가됩니다.

<a name="rule-lte"></a>
#### lte:_field_

유효성 검사 중인 필드는 지정된 _field_보다 작거나 같아야 합니다. 두 필드는 동일한 유형이어야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 규칙을 사용하여 평가됩니다.

<a name="rule-lowercase"></a>
#### 소문자

유효성 검사 중인 필드는 소문자여야 합니다.

<a name="rule-list"></a>
#### 목록

유효성 검사 대상 필드는 목록인 배열이어야 합니다. 키가 0부터 `count($array) - 1`까지의 연속 숫자로 구성된 경우 배열은 목록으로 간주됩니다.

<a name="rule-mac"></a>
#### mac_address

검증 중인 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
#### max:_value_

유효성 검사 중인 필드는 최대 _value_보다 작거나 같아야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
#### max_digits:_value_

검증 중인 정수의 최대 길이는 _value_여야 합니다.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

유효성 검사 중인 파일은 지정된 MIME 유형 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime',

'media' => 'mimetypes:image/*,video/*',
```

업로드된 파일의 MIME 유형을 결정하기 위해 파일의 내용을 읽고 프레임워크는 클라이언트가 제공한 MIME 유형과 다를 수 있는 MIME 유형을 추측하려고 시도합니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

검증 중인 파일에는 나열된 확장자 중 하나에 해당하는 MIME 유형이 있어야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

확장자만 지정하면 되지만 이 규칙은 실제로 파일 내용을 읽고 MIME 유형을 추측하여 파일의 MIME 유형을 검증합니다. MIME 유형 및 해당 확장자의 전체 목록은 다음 위치에서 찾을 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME 유형 및 확장자

이 확인 규칙은 MIME 유형과 사용자가 파일에 할당한 확장자 간의 일치를 확인하지 않습니다. 예를 들어, `mimes:png` 유효성 검사 규칙은 파일 이름이 `photo.txt`인 경우에도 유효한 PNG 콘텐츠가 포함된 파일을 유효한 PNG 이미지로 간주합니다. 사용자가 할당한 파일 확장자를 확인하려면 [확장자](#rule-extensions) 규칙을 사용할 수 있습니다.

<a name="rule-min"></a>
#### 최소:_value_

검증 중인 필드에는 최소 _value_가 있어야 합니다. 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
#### min_digits:_value_

검증 중인 정수의 최소 길이는 _value_여야 합니다.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

검증 중인 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
#### 없어진

유효성 검사 중인 필드는 입력 데이터에 없어야 합니다.

<a name="rule-missing-if"></a>
#### 누락_if:_anotherfield_,_값_,...

_anotherfield_ 필드가 임의의 _value_와 같은 경우 유효성 검사 중인 필드가 없어야 합니다.

<a name="rule-missing-unless"></a>
#### 누락된_unless:_anotherfield_,_값_

_anotherfield_ 필드가 임의의 _value_와 동일하지 않으면 유효성 검사 중인 필드가 존재해서는 안 됩니다.

<a name="rule-missing-with"></a>
#### 누락_with:_foo_,_bar_,...

유효성 검사 중인 필드는 다른 지정된 필드가 있는 경우에만_ 존재해서는 안 됩니다.

<a name="rule-missing-with-all"></a>
#### Missing_with_all:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 다른 필드가 모두 존재하는 경우에만_ 존재해서는 안 됩니다.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 값 목록에 포함되어서는 안 됩니다. `Rule::notIn` 메소드를 사용하여 규칙을 원활하게 구성할 수 있습니다.

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

유효성 검사 중인 필드는 지정된 정규식과 일치하지 않아야 합니다.

내부적으로 이 규칙은 PHP `preg_match` 함수를 사용합니다. 지정된 패턴은 `preg_match`에서 요구하는 것과 동일한 형식을 준수해야 하므로 유효한 구분 기호도 포함해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때 특히 정규식에 `|` 문자가 포함된 경우 `|` 구분 기호를 사용하는 대신 배열을 사용하여 유효성 검사 규칙을 지정해야 할 수도 있습니다.

<a name="rule-nullable"></a>
#### 널 입력 가능

검증 중인 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
#### 숫자

검증 중인 필드는 [숫자](https://www.php.net/manual/en/function.is-numeric.php)여야 합니다.

`strict` 매개변수를 사용하면 해당 값이 정수 또는 부동 소수점 유형인 경우에만 필드가 유효한 것으로 간주할 수 있습니다. 숫자 문자열은 유효하지 않은 것으로 간주됩니다.

```php
'amount' => 'numeric:strict'
```

<a name="rule-present"></a>
#### 현재의

유효성 검증 중인 필드가 입력 데이터에 존재해야 합니다.

<a name="rule-present-if"></a>
#### 현재_if:_anotherfield_,_값_,...

_anotherfield_ 필드가 임의의 _value_와 같은 경우 유효성 검사 중인 필드가 있어야 합니다.

<a name="rule-present-unless"></a>
#### 현재_unless:_anotherfield_,_value_

_anotherfield_ 필드가 _value_와 동일하지 않은 경우 유효성 검사 중인 필드가 있어야 합니다.

<a name="rule-present-with"></a>
#### 현재_with:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 다른 필드가 있는 경우에만_ 존재해야 합니다.

<a name="rule-present-with-all"></a>
#### 현재_with_all:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 다른 필드가 모두 존재하는 경우에만_ 존재해야 합니다.

<a name="rule-prohibited"></a>
#### 금지된

유효성 검사 중인 필드가 누락되었거나 비어 있어야 합니다. 다음 기준 중 하나를 충족하는 경우 필드는 "비어 있습니다".

<div class="content-list" markdown="1">

- 값은 `null`입니다.
- 값은 빈 문자열입니다.
- 값은 빈 배열 또는 빈 `Countable` 객체입니다.
- 값은 경로가 비어 있는 업로드된 파일입니다.

</div>

<a name="rule-prohibited-if"></a>
#### 금지_if:_anotherfield_,_값_,...

_anotherfield_ 필드가 임의의 _value_와 같은 경우 유효성 검사 중인 필드가 누락되거나 비어 있어야 합니다. 다음 기준 중 하나를 충족하는 경우 필드는 "비어 있습니다".

<div class="content-list" markdown="1">

- 값은 `null`입니다.
- 값은 빈 문자열입니다.
- 값은 빈 배열 또는 빈 `Countable` 객체입니다.
- 값은 경로가 비어 있는 업로드된 파일입니다.

</div>

복잡한 조건부 금지 논리가 필요한 경우 `Rule::prohibitedIf` 방법을 활용할 수 있습니다. 이 메소드는 부울 또는 클로저를 허용합니다. 클로저가 제공되면 클로저는 `true` 또는 `false`를 반환하여 유효성 검사 중인 필드가 금지되어야 하는지 여부를 나타내야 합니다.

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
#### allowed_if_accepted:_anotherfield_,...

_anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true` 또는 `"true"`와 같은 경우 유효성 검사 중인 필드가 누락되었거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
#### allowed_if_declined:_anotherfield_,...

_anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false` 또는 `"false"`와 같은 경우 유효성 검사 중인 필드가 누락되었거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
#### allowed_unless:_anotherfield_,_value_,...

_anotherfield_ 필드가 _value_와 동일하지 않은 경우 유효성 검사 중인 필드는 누락되거나 비어 있어야 합니다. 다음 기준 중 하나를 충족하는 경우 필드는 "비어 있습니다".

<div class="content-list" markdown="1">

- 값은 `null`입니다.
- 값은 빈 문자열입니다.
- 값은 빈 배열 또는 빈 `Countable` 객체입니다.
- 값은 경로가 비어 있는 업로드된 파일입니다.

</div>

<a name="rule-prohibits"></a>
#### :_anotherfield_를 금지합니다...

유효성 검사 중인 필드가 누락되거나 비어 있지 않은 경우 _anotherfield_의 모든 필드가 누락되거나 비어 있어야 합니다. 다음 기준 중 하나를 충족하는 경우 필드는 "비어 있습니다".

<div class="content-list" markdown="1">

- 값은 `null`입니다.
- 값은 빈 문자열입니다.
- 값은 빈 배열 또는 빈 `Countable` 객체입니다.
- 값은 경로가 비어 있는 업로드된 파일입니다.

</div>

<a name="rule-regex"></a>
#### 정규식:_pattern_

유효성 검사 중인 필드는 지정된 정규식과 일치해야 합니다.

내부적으로 이 규칙은 PHP `preg_match` 함수를 사용합니다. 지정된 패턴은 `preg_match`에서 요구하는 것과 동일한 형식을 준수해야 하므로 유효한 구분 기호도 포함해야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때 특히 정규식에 `|` 문자가 포함된 경우 `|` 구분 기호를 사용하는 대신 배열에 규칙을 지정해야 할 수도 있습니다.

<a name="rule-required"></a>
#### 필수의

유효성 검사 중인 필드는 입력 데이터에 있어야 하며 비어 있으면 안 됩니다. 다음 기준 중 하나를 충족하는 경우 필드는 "비어 있습니다".

<div class="content-list" markdown="1">

- 값은 `null`입니다.
- 값은 빈 문자열입니다.
- 값은 빈 배열 또는 빈 `Countable` 객체입니다.
- 값은 경로가 없는 업로드된 파일입니다.

</div>

<a name="rule-required-if"></a>
#### 필수_if:_anotherfield_,_값_,...

_anotherfield_ 필드가 임의의 _value_와 같은 경우 유효성 검사 중인 필드가 있어야 하며 비어 있어서는 안 됩니다.

`required_if` 규칙에 대해 더 복잡한 조건을 구성하려면 `Rule::requiredIf` 방법을 사용할 수 있습니다. 이 메소드는 부울 또는 클로저를 허용합니다. 클로저를 전달하면 클로저는 `true` 또는 `false`를 반환하여 유효성 검사 중인 필드가 필요한지 여부를 나타내야 합니다.

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
#### 필수_if_accepted:_anotherfield_,...

_anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true` 또는 `"true"`와 같은 경우 유효성 검사 중인 필드가 있어야 하며 비어 있지 않아야 합니다.

<a name="rule-required-if-declined"></a>
#### 필수_if_거절:_anotherfield_,...

_anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false` 또는 `"false"`와 같은 경우 유효성 검사 중인 필드가 있어야 하며 비어 있지 않아야 합니다.

<a name="rule-required-unless"></a>
#### 필수_unless:_anotherfield_,_값_,...

유효성 검사 중인 필드는 존재해야 하며 _anotherfield_ 필드가 _value_와 동일하지 않는 한 비어 있어서는 안 됩니다. 이는 또한 _value_가 `null`가 아닌 한 요청 데이터에 _anotherfield_가 있어야 함을 의미합니다. _value_가 `null`(`required_unless:name,null`)인 경우 비교 필드가 `null`이거나 요청 데이터에서 비교 필드가 누락되지 않는 한 유효성 검사 중인 필드가 필요합니다.

<a name="rule-required-with"></a>
#### 필수_with:_foo_,_bar_,...

유효성 검사 중인 필드는 존재해야 하며 비어 있지 않아야 합니다. 지정된 다른 필드 중 하나라도 존재하고 비어 있지 않은 경우에만_입니다.

<a name="rule-required-with-all"></a>
#### 필수_with_all:_foo_,_bar_,...

유효성 검사 대상 필드는 반드시 존재해야 하며 비어 있지 않아야 합니다. 지정된 다른 모든 필드가 모두 존재하고 비어 있지 않은 경우에만_입니다.

<a name="rule-required-without"></a>
#### 필수_없이:_foo_,_bar_,...

유효성 검사 중인 필드는 반드시 존재해야 하며, 지정된 다른 필드가 비어 있거나 존재하지 않는 _경우에만_ 비어 있으면 안 됩니다.

<a name="rule-required-without-all"></a>
#### 필수_없이_all:_foo_,_bar_,...

유효성 검사 중인 필드는 반드시 존재해야 하며, 지정된 다른 모든 필드가 비어 있거나 존재하지 않는 _경우에만_ 비어 있으면 안 됩니다.

<a name="rule-required-array-keys"></a>
#### 필수_배열_키s:_foo_,_bar_,...

유효성 검사 대상 필드는 배열이어야 하며 최소한 지정된 키를 포함해야 합니다.

<a name="rule-same"></a>
#### 동일:_field_

주어진 _field_는 검증 중인 필드와 일치해야 합니다.

<a name="rule-size"></a>
#### 크기:_value_

유효성 검사 중인 필드는 지정된 _value_와 일치하는 크기를 가져야 합니다. 문자열 데이터의 경우 _value_는 문자 수에 해당합니다. 숫자 데이터의 경우 _value_는 지정된 정수 값에 해당합니다(특성에는 `numeric` 또는 `integer` 규칙도 있어야 함). 배열의 경우 _size_는 배열의 `count`에 해당합니다. 파일의 경우 _size_는 파일 크기(KB)에 해당합니다. 몇 가지 예를 살펴보겠습니다.

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
#### 시작_with:_foo_,_bar_,...

유효성 검사 중인 필드는 지정된 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### 끈

유효성 검사 중인 필드는 문자열이어야 합니다. 필드가 `null`가 되도록 허용하려면 해당 필드에 `nullable` 규칙을 할당해야 합니다.

<a name="rule-timezone"></a>
#### 시간대

유효성 검사 중인 필드는 `DateTimeZone::listIdentifiers` 방법에 따라 유효한 시간대 식별자여야 합니다.

[`DateTimeZone::listIdentifiers` 메서드에서 허용되는](https://www.php.net/manual/en/datetimezone.listidentifiers.php) 인수도 이 유효성 검사 규칙에 제공될 수 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
#### 고유:_table_,_column_

유효성 검사 중인 필드는 지정된 데이터베이스 테이블 내에 존재하지 않아야 합니다.

**사용자 지정 테이블/열 이름 지정:**

테이블 이름을 직접 지정하는 대신 테이블 이름을 결정하는 데 사용해야 하는 Eloquent 모델을 지정할 수 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

`column` 옵션은 필드의 해당 데이터베이스 열을 지정하는 데 사용될 수 있습니다. `column` 옵션을 지정하지 않으면 유효성 검사 중인 필드 이름이 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

**사용자 지정 데이터베이스 연결 지정**

경우에 따라 유효성 검사기가 만든 데이터베이스 쿼리에 대한 사용자 지정 연결을 설정해야 할 수도 있습니다. 이를 수행하려면 테이블 이름 앞에 연결 이름을 추가하면 됩니다.

```php
'email' => 'unique:connection.users,email_address'
```

**주어진 ID를 무시하도록 고유 규칙을 강제 적용:**

때로는 고유한 유효성 검사 중에 특정 ID를 무시하고 싶을 수도 있습니다. 예를 들어, 사용자 이름, 이메일 주소, 위치가 포함된 "프로필 업데이트" 화면을 생각해 보세요. 이메일 주소가 고유한지 확인하고 싶을 것입니다. 그러나 사용자가 이메일 필드가 아닌 이름 필드만 변경하는 경우 사용자가 이미 해당 이메일 주소의 소유자이기 때문에 유효성 검사 오류가 발생하는 것을 원하지 않습니다.

유효성 검사기에 사용자 ID를 무시하도록 지시하기 위해 `Rule` 클래스를 사용하여 규칙을 원활하게 정의합니다. 이 예에서는 규칙을 구분하기 위해 `|` 문자를 사용하는 대신 유효성 검사 규칙을 배열로 지정합니다.

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
> 사용자가 제어하는 ​​요청 입력을 `ignore` 메서드에 전달하면 안 됩니다. 대신 자동 증가 ID 또는 Eloquent 모델 인스턴스의 UUID와 같은 시스템 생성 고유 ID만 전달해야 합니다. 그렇지 않으면 애플리케이션이 SQL 주입 공격에 취약해집니다.

모델 키의 값을 `ignore` 메서드에 전달하는 대신 전체 모델 인스턴스를 전달할 수도 있습니다. Laravel는 모델에서 자동으로 키를 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

테이블이 `id` 이외의 기본 키 열 이름을 사용하는 경우 `ignore` 메서드를 호출할 때 열 이름을 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

기본적으로 `unique` 규칙은 유효성을 검사하는 속성 이름과 일치하는 열의 고유성을 확인합니다. 그러나 `unique` 메소드의 두 번째 인수로 다른 열 이름을 전달할 수 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

**추가 Where 절 추가:**

`where` 메소드를 사용하여 쿼리를 사용자 지정하여 추가 쿼리 조건을 지정할 수 있습니다. 예를 들어, `account_id` 열 값이 `1`인 검색 레코드에만 쿼리의 범위를 지정하는 쿼리 조건을 추가해 보겠습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

**고유 검사에서 소프트 삭제된 레코드 무시:**

기본적으로 고유 규칙에는 고유성을 결정할 때 일시 삭제된 레코드가 포함됩니다. 고유성 확인에서 일시 삭제된 레코드를 제외하려면 `withoutTrashed` 메소드를 호출하면 됩니다.

```php
Rule::unique('users')->withoutTrashed();
```

모델이 일시 삭제된 레코드에 대해 `deleted_at` 이외의 열 이름을 사용하는 경우 `withoutTrashed` 메서드를 호출할 때 열 이름을 제공할 수 있습니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
#### 대문자

유효성 검사 중인 필드는 대문자여야 합니다.

<a name="rule-url"></a>
#### URL

검증 중인 필드는 유효한 URL여야 합니다.

유효한 것으로 간주되어야 하는 URL 프로토콜을 지정하려면 해당 프로토콜을 유효성 검사 규칙 매개변수로 전달할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
#### 울리드

검증 중인 필드는 유효한 [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec)(ULID)여야 합니다.

<a name="rule-uuid"></a>
#### uuid

유효성 검사 중인 필드는 유효한 RFC 9562(버전 1, 3, 4, 5, 6, 7 또는 8) 범용 고유 식별자(UUID)여야 합니다.

또한 지정된 UUID가 버전별로 UUID 사양과 일치하는지 확인할 수도 있습니다.

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
## 조건부로 규칙 추가 (Conditionally Adding Rules)

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 필드에 특정 값이 있을 때 유효성 검사 건너뛰기

다른 필드에 특정 값이 있는 경우 특정 필드의 유효성을 검사하지 않으려는 경우가 종종 있습니다. `exclude_if` 유효성 검사 규칙을 사용하여 이를 수행할 수 있습니다. 이 예에서 `has_appointment` 필드에 `false` 값이 있는 경우 `appointment_date` 및 `doctor_name` 필드는 유효성이 검사되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

또는 `exclude_unless` 규칙을 사용하여 다른 필드에 지정된 값이 없으면 지정된 필드의 유효성을 검사하지 않을 수 있습니다.

```php
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
#### 존재 여부 확인

어떤 상황에서는 해당 필드가 유효성을 검사하는 데이터에 있는 경우 **만** 해당 필드에 대해 유효성 검사를 실행하고 싶을 수도 있습니다. 이를 신속하게 수행하려면 규칙 목록에 `sometimes` 규칙을 추가하세요.

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

위의 예에서 `email` 필드는 `$data` 배열에 있는 경우에만 유효성이 검사됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드의 유효성을 검사하려는 경우 [선택적 필드에 대한 이 참고 사항](#a-note-on-optional-fields)을 확인하세요.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

때로는 더 복잡한 조건부 논리를 기반으로 유효성 검사 규칙을 추가하고 싶을 수도 있습니다. 예를 들어 다른 필드의 값이 100보다 큰 경우에만 지정된 필드를 요구할 수 있습니다. 또는 다른 필드가 있는 경우에만 지정된 값을 가지려면 두 개의 필드가 필요할 수 있습니다. 이러한 유효성 검사 규칙을 추가하는 것이 어려울 필요는 없습니다. 먼저, 절대로 변경되지 않는 _정적 규칙_을 사용하여 `Validator` 인스턴스를 만듭니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

우리 웹 애플리케이션이 게임 수집가를 위한 것이라고 가정해 보겠습니다. 게임 수집가가 우리 애플리케이션에 등록하고 100개 이상의 게임을 소유한 경우, 우리는 그들이 그토록 많은 게임을 소유한 이유를 설명하기를 원합니다. 예를 들어, 게임 재판매 상점을 운영할 수도 있고, 단순히 게임 수집을 좋아할 수도 있습니다. 이 요구 사항을 조건부로 추가하려면 `Validator` 인스턴스에서 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

`sometimes` 메소드에 전달된 첫 번째 인수는 조건부로 유효성을 검사하는 필드의 이름입니다. 두 번째 인수는 추가하려는 규칙 목록입니다. 세 번째 인수로 전달된 클로저가 `true`를 반환하면 규칙이 추가됩니다. 이 방법을 사용하면 복잡한 조건부 유효성 검사를 쉽게 구축할 수 있습니다. 여러 필드에 대한 조건부 유효성 검사를 한 번에 추가할 수도 있습니다.

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달된 `$input` 매개변수는 `Illuminate\Support\Fluent`의 인스턴스가 되며 검증 중인 입력 및 파일에 액세스하는 데 사용될 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건부 배열 유효성 검사

때로는 인덱스를 모르는 동일한 중첩 배열의 다른 필드를 기반으로 필드의 유효성을 검사해야 할 수도 있습니다. 이러한 상황에서는 클로저가 검증 중인 배열의 현재 개별 항목이 될 두 번째 인수를 받도록 허용할 수 있습니다.

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

클로저에 전달된 `$input` 매개변수와 마찬가지로 `$item` 매개변수는 속성 데이터가 배열일 때 `Illuminate\Support\Fluent`의 인스턴스입니다. 그렇지 않으면 문자열입니다.

<a name="validating-arrays"></a>
## 어레이 검증 (Validating Arrays)

[배열 유효성 검사 규칙 문서](#rule-array)에서 설명한 대로 `array` 규칙은 허용되는 배열 키 목록을 허용합니다. 배열 내에 추가 키가 있으면 유효성 검사가 실패합니다.

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

일반적으로 배열 내에 존재할 수 있는 배열 키를 항상 지정해야 합니다. 그렇지 않으면 유효성 검사기의 `validate` 및 `validated` 메서드는 해당 키가 다른 중첩 배열 유효성 검사 규칙에 의해 유효성이 검사되지 않은 경우에도 배열과 해당 키를 모두 포함하여 유효성이 검사된 모든 데이터를 반환합니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 검증

중첩된 배열 기반 양식 입력 필드의 유효성을 검사하는 것이 어려울 필요는 없습니다. 배열 내의 속성을 확인하기 위해 "점 표기법"을 사용할 수 있습니다. 예를 들어 들어오는 HTTP 요청에 `photos[profile]` 필드가 포함되어 있으면 다음과 같이 유효성을 검사할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

배열의 각 요소를 확인할 수도 있습니다. 예를 들어, 주어진 배열 입력 필드의 각 이메일이 고유한지 확인하려면 다음을 수행할 수 있습니다.

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

마찬가지로 [언어 파일의 사용자 지정 유효성 검사 메시지](#custom-messages-for-specific-attributes)를 지정할 때 `*` 문자를 사용할 수 있으므로 배열 기반 필드에 대해 단일 유효성 검사 메시지를 사용하는 것이 간편해집니다.

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
#### 중첩된 배열 데이터에 액세스

속성에 유효성 검사 규칙을 할당할 때 특정 중첩 배열 요소의 값에 액세스해야 하는 경우도 있습니다. `Rule::forEach` 방법을 사용하여 이 작업을 수행할 수 있습니다. `forEach` 메소드는 검증 중인 배열 속성의 각 반복에 대해 호출되는 클로저를 허용하고 속성 값과 명시적이고 완전히 확장된 속성 이름을 수신합니다. 클로저는 배열 요소에 할당할 규칙 배열을 반환해야 합니다.

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
### 오류 메시지 색인 및 위치

배열의 유효성을 검사할 때 응용 프로그램에 표시되는 오류 메시지 내에서 유효성 검사에 실패한 특정 항목의 인덱스나 위치를 참조할 수 있습니다. 이를 수행하려면 [사용자 지정 확인 메시지](#manual-customizing-the-error-messages) 내에 `:index`(`0`에서 시작), `:position`(`1`에서 시작) 또는 `:ordinal-position`(`1st`에서 시작) 자리 표시자를 포함할 수 있습니다.

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

위의 예에서 유효성 검사는 실패하고 사용자에게 _"사진 #2에 대해 설명해주세요."_라는 오류가 표시됩니다.

필요한 경우 `second-index`, `second-position`, `third-index`, `third-position` 등을 통해 더 깊게 중첩된 인덱스와 위치를 참조할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
## 파일 유효성 검사 (Validating Files)

Laravel는 `mimes`, `image`, `min` 및 `max`와 같이 업로드된 파일의 유효성을 검사하는 데 사용할 수 있는 다양한 유효성 검사 규칙을 제공합니다. 파일 유효성을 검사할 때 이러한 규칙을 개별적으로 자유롭게 지정할 수 있지만 Laravel는 편리하다고 생각할 수 있는 유창한 파일 유효성 검사 규칙 빌더도 제공합니다.

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
#### 파일 형식 유효성 검사

`types` 메소드를 호출할 때 확장명만 지정하면 되지만 이 메소드는 실제로 파일의 내용을 읽고 MIME 유형을 추측하여 파일의 MIME 유형을 검증합니다. MIME 유형 및 해당 확장자의 전체 목록은 다음 위치에서 찾을 수 있습니다.

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 검증

편의상 최소 및 최대 파일 크기는 파일 크기 단위를 나타내는 접미사가 붙은 문자열로 지정할 수 있습니다. `kb`, `mb`, `gb` 및 `tb` 접미사가 지원됩니다.

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
#### 이미지 파일 검증

애플리케이션이 사용자가 업로드한 이미지를 허용하는 경우 `File` 규칙의 `image` 생성자 메서드를 사용하여 유효성 검사 중인 파일이 이미지(jpg, jpeg, png, bmp, gif 또는 webp)인지 확인할 수 있습니다.

또한 `dimensions` 규칙을 사용하여 이미지 크기를 제한할 수 있습니다.

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
> 이미지 크기 검증에 대한 자세한 내용은 [차원 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약점 가능성으로 인해 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 하는 경우 `allowSvg: true`를 `image` 규칙(`File::image(allowSvg: true)`)에 전달할 수 있습니다.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기 검증

이미지의 크기를 확인할 수도 있습니다. 예를 들어 업로드된 이미지의 너비가 최소 1000픽셀, 높이가 500픽셀인지 확인하려면 `dimensions` 규칙을 사용할 수 있습니다.

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
> 이미지 크기 검증에 대한 자세한 내용은 [차원 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

<a name="validating-passwords"></a>
## 비밀번호 확인 (Validating Passwords)

비밀번호의 복잡성을 적절한 수준으로 유지하려면 Laravel의 `Password` 규칙 객체를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

`Password` 규칙 객체를 사용하면 비밀번호에 최소한 하나의 문자, 숫자, 기호 또는 대소문자가 혼합된 문자가 필요하도록 지정하는 등 애플리케이션의 비밀번호 복잡성 요구 사항을 쉽게 사용자 지정할 수 있습니다.

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

또한 `uncompromised` 방법을 사용하여 공개 비밀번호 데이터 유출 시 비밀번호가 손상되지 않았는지 확인할 수 있습니다.

```php
Password::min(8)->uncompromised()
```

내부적으로 `Password` 규칙 객체는 [k-익명성](https://en.wikipedia.org/wiki/K-anonymity) 모델을 사용하여 사용자의 개인 정보 보호나 보안을 희생하지 않고 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호가 유출되었는지 확인합니다.

기본적으로 데이터 유출 시 비밀번호가 한 번 이상 나타나면 손상된 것으로 간주됩니다. `uncompromised` 메소드의 첫 번째 인수를 사용하여 이 임계값을 사용자 지정할 수 있습니다.

```php
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

물론 위 예제의 모든 메서드를 연결할 수도 있습니다.

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

애플리케이션의 단일 위치에서 비밀번호에 대한 기본 유효성 검사 규칙을 지정하는 것이 편리할 수 있습니다. 클로저를 허용하는 `Password::defaults` 메서드를 사용하면 이 작업을 쉽게 수행할 수 있습니다. `defaults` 메소드에 제공된 클로저는 비밀번호 규칙의 기본 구성을 반환해야 합니다. 일반적으로 `defaults` 규칙은 애플리케이션 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 호출되어야 합니다.

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

그런 다음 검증 중인 특정 비밀번호에 기본 규칙을 적용하려는 경우 인수 없이 `defaults` 메소드를 호출할 수 있습니다.

```php
'password' => ['required', Password::defaults()],
```

경우에 따라 기본 비밀번호 확인 규칙에 추가 확인 규칙을 첨부할 수 있습니다. 이를 수행하려면 `rules` 메소드를 사용할 수 있습니다.

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
## 사용자 지정 검증 규칙 (Custom Validation Rules)

<a name="using-rule-objects"></a>
### 규칙 객체 사용

Laravel는 다양하고 유용한 유효성 검사 규칙을 제공합니다. 그러나 사용자가 직접 지정할 수도 있습니다. 사용자 지정 유효성 검사 규칙을 등록하는 한 가지 방법은 규칙 개체를 사용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령을 사용할 수 있습니다. 이 명령을 사용하여 문자열이 대문자인지 확인하는 규칙을 생성해 보겠습니다. Laravel는 `app/Rules` 디렉터리에 새 규칙을 배치합니다. 이 디렉터리가 없으면 Artisan 명령을 실행하여 규칙을 생성할 때 Laravel가 디렉터리를 생성합니다.

```shell
php artisan make:rule Uppercase
```

규칙이 생성되면 해당 동작을 정의할 준비가 된 것입니다. 규칙 객체에는 `validate`라는 단일 메서드가 포함되어 있습니다. 이 메소드는 속성 이름, 해당 값, 유효성 검사 오류 메시지와 함께 실패 시 호출되어야 하는 콜백을 수신합니다.

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

규칙이 정의되면 다른 유효성 검사 규칙과 함께 규칙 개체의 인스턴스를 전달하여 유효성 검사기에 연결할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

#### 검증 메시지 번역

`$fail` 클로저에 리터럴 오류 메시지를 제공하는 대신 [번역 문자열 키](/docs/12.x/localization)를 제공하고 Laravel에 오류 메시지를 번역하도록 지시할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

필요한 경우 `translate` 메소드의 첫 번째 및 두 번째 인수로 자리 표시자 대체 및 기본 언어를 제공할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

#### 추가 데이터에 접근하기

사용자 지정 유효성 검사 규칙 클래스가 유효성 검사를 받는 다른 모든 데이터에 액세스해야 하는 경우 규칙 클래스는 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스를 사용하려면 클래스에서 `setData` 메서드를 정의해야 합니다. 이 메소드는 검증 중인 모든 데이터와 함께 Laravel(검증이 진행되기 전)에 의해 자동으로 호출됩니다.

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

또는 유효성 검사 규칙이 유효성 검사를 수행하는 유효성 검사기 인스턴스에 액세스해야 하는 경우 `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

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

애플리케이션 전체에서 사용자 지정 규칙의 기능이 한 번만 필요한 경우 규칙 객체 대신 클로저를 사용할 수 있습니다. 클로저는 속성의 이름, 속성의 값, 유효성 검사가 실패할 경우 호출해야 하는 `$fail` 콜백을 받습니다.

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
### 암시적 규칙

기본적으로 유효성을 검사 중인 속성이 없거나 빈 문자열이 포함되어 있으면 사용자 지정 규칙을 포함한 일반 유효성 검사 규칙이 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에 대해 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

속성이 비어 있는 경우에도 사용자 지정 규칙을 실행하려면 규칙에서 해당 속성이 필요하다는 것을 암시해야 합니다. 새로운 암시적 규칙 객체를 빠르게 생성하려면 `make:rule` Artisan 명령을 `--implicit` 옵션과 함께 사용할 수 있습니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암시적" 규칙은 해당 속성이 필요하다는 것을 _암시_합니다. 누락되거나 비어 있는 속성을 실제로 무효화할지 여부는 귀하에게 달려 있습니다.
