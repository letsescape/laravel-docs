<!-- # Validation -->
# Validation

- [Introduction](#introduction)
- [Validation Quickstart](#validation-quickstart)
    - [Defining the Routes](#quick-defining-the-routes)
    - [Creating the Controller](#quick-creating-the-controller)
    - [Writing the Validation Logic](#quick-writing-the-validation-logic)
    - [Displaying the Validation Errors](#quick-displaying-the-validation-errors)
    - [Repopulating Forms](#repopulating-forms)
    - [A Note on Optional Fields](#a-note-on-optional-fields)
    - [Validation Error Response Format](#validation-error-response-format)
- [Form Request Validation](#form-request-validation)
    - [Creating Form Requests](#creating-form-requests)
    - [Authorizing Form Requests](#authorizing-form-requests)
    - [Customizing the Error Messages](#customizing-the-error-messages)
    - [Preparing Input for Validation](#preparing-input-for-validation)
- [Manually Creating Validators](#manually-creating-validators)
    - [Automatic Redirection](#automatic-redirection)
    - [Named Error Bags](#named-error-bags)
    - [Customizing the Error Messages](#manual-customizing-the-error-messages)
    - [Performing Additional Validation](#performing-additional-validation)
- [Working With Validated Input](#working-with-validated-input)
- [Working With Error Messages](#working-with-error-messages)
    - [Specifying Custom Messages in Language Files](#specifying-custom-messages-in-language-files)
    - [Specifying Attributes in Language Files](#specifying-attribute-in-language-files)
    - [Specifying Values in Language Files](#specifying-values-in-language-files)
- [Available Validation Rules](#available-validation-rules)
- [Conditionally Adding Rules](#conditionally-adding-rules)
- [Validating Arrays](#validating-arrays)
    - [Validating Nested Array Input](#validating-nested-array-input)
    - [Error Message Indexes and Positions](#error-message-indexes-and-positions)
- [Validating Files](#validating-files)
- [Validating Passwords](#validating-passwords)
- [Custom Validation Rules](#custom-validation-rules)
    - [Using Rule Objects](#using-rule-objects)
    - [Using Closures](#using-closures)
    - [Implicit Rules](#implicit-rules)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well. -->
Laravel은 애플리케이션으로 들어오는 데이터를 유효성 검증하기 위한 여러 가지 접근 방식을 제공합니다. 가장 일반적인 방법은 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용하는 것입니다. 하지만 이 문서에서는 다른 유효성 검증 방법들도 함께 다룹니다.

<!-- Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features. -->
Laravel에는 매우 다양한 편리한 유효성 검증 규칙들이 포함되어 있습니다. 특정 데이터베이스 테이블에서 값의 유일성까지 검증할 수 있으며, 이러한 유효성 검증 규칙 하나하나를 자세히 설명할 예정입니다. 이를 통해 Laravel의 유효성 검증 기능을 모두 이해할 수 있습니다.

<a name="validation-quickstart"></a>
<!-- ## Validation Quickstart -->
## Validation Quickstart

<!-- To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel: -->
Laravel의 강력한 유효성 검증 기능을 익히려면, 폼을 검증하고 사용자에게 에러 메시지를 표시하는 전체 예제를 살펴보는 것이 좋습니다. 아래 전체적인 흐름을 따라 읽으면, Laravel을 사용해 들어오는 요청 데이터를 어떻게 검증하는지 전반적인 이해를 하실 수 있습니다.

<a name="quick-defining-the-routes"></a>
<!-- ### Defining the Routes -->
### Defining the Routes

<!-- First, let's assume we have the following routes defined in our `routes/web.php` file: -->
우선, `routes/web.php` 파일에 다음과 같이 라우트를 정의한다고 가정해보겠습니다:

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

<!-- The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database. -->
`GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 보여주며, `POST` 라우트는 작성된 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
<!-- ### Creating the Controller -->
### Creating the Controller

<!-- Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now: -->
다음으로, 이 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 여기서는 `store` 메서드는 일단 비워두겠습니다:

```
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
<!-- ### Writing the Validation Logic -->
### Writing the Validation Logic

<!-- Now we are ready to fill in our `store` method with the logic to validate the new blog post. To do this, we will use the `validate` method provided by the `Illuminate\Http\Request` object. If the validation rules pass, your code will keep executing normally; however, if validation fails, an `Illuminate\Validation\ValidationException` exception will be thrown and the proper error response will automatically be sent back to the user. -->
이제, 새 블로그 포스트를 검증하는 로직으로 `store` 메서드를 완성할 차례입니다. 이를 위해 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드는 정상적으로 계속 실행됩니다. 그러나 검증에 실패할 경우 `Illuminate\Validation\ValidationException` 예외가 발생하며, 적절한 에러 응답이 자동으로 사용자에게 전송됩니다.

<!-- If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a [JSON response containing the validation error messages](#validation-error-response-format) will be returned. -->
전통적인 HTTP 요청에서 검증이 실패하면 이전 URL로 리다이렉트하는 응답이 생성됩니다. 만약 들어온 요청이 XHR(비동기) 요청이면, [JSON response containing the validation error messages](#validation-error-response-format)이 반환됩니다.

<!-- To get a better understanding of the `validate` method, let's jump back into the `store` method: -->
`validate` 메서드의 동작 방식을 더 잘 이해하기 위해 `store` 메서드 예시를 봅시다:

```
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

<!-- As you can see, the validation rules are passed into the `validate` method. Don't worry - all available validation rules are [documented](#available-validation-rules). Again, if the validation fails, the proper response will automatically be generated. If the validation passes, our controller will continue executing normally. -->
보시다시피, 검증 규칙들은 `validate` 메서드의 인수로 전달됩니다. 걱정하지 마세요. 사용 가능한 모든 유효성 검증 규칙은 [documented](#available-validation-rules) 자세히 문서화되어 있습니다. 다시 말씀드리면, 검증에 실패하면 적절한 응답이 자동으로 생성됩니다. 검증을 통과하면 컨트롤러는 계속 정상 실행됩니다.

<!-- Alternatively, validation rules may be specified as arrays of rules instead of a single `|` delimited string: -->
또한, 검증 규칙은 `|`로 구분된 문자열 대신 각각 배열로 지정할 수도 있습니다:

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<!-- In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a [named error bag](#named-error-bags): -->
또한, 요청을 검증하면서 발생한 에러 메시지를 [named error bag](#named-error-bags)에 저장하고 싶을 땐 `validateWithBag` 메서드를 사용할 수 있습니다:

```
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
<!-- #### Stopping on First Validation Failure -->
#### Stopping on First Validation Failure

<!-- Sometimes you may wish to stop running validation rules on an attribute after the first validation failure. To do so, assign the `bail` rule to the attribute: -->
때로는 하나의 속성(attribute)에 대해 첫 번째 유효성 검증에 실패하면 그 이후의 검증 규칙을 실행하지 않게 하고 싶을 때가 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다:

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

<!-- In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned. -->
이 예시에서, 만약 `title` 속성에 설정된 `unique` 규칙이 실패하면, 그 이후의 `max` 규칙은 검사하지 않습니다. 규칙들은 지정된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
<!-- #### A Note on Nested Attributes -->
#### A Note on Nested Attributes

<!-- If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax: -->
들어오는 HTTP 요청에 "중첩된(nested)" 필드 데이터가 들어올 경우, 검증 규칙에서 "닷(dot, .)" 문법을 이용해 필드명을 지정하면 됩니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

<!-- On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash: -->
반면, 필드명에 마침표가 실제로 포함되어 있고 이것이 "dot" 문법이 아니기를 원한다면, 백슬래시로 마침표를 이스케이프 처리해서 의도를 명확히 할 수 있습니다:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
<!-- ### Displaying the Validation Errors -->
### Displaying the Validation Errors

<!-- So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/10.x/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/10.x/session#flash-data). -->
그렇다면, 들어온 요청의 필드 값이 지정한 유효성 검증 규칙을 통과하지 못한다면 어떻게 될까요? 앞서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 뿐만 아니라, 모든 유효성 검증 에러와 [request input](/docs/10.x/requests#retrieving-old-input)이 자동으로 [flashed to the session](/docs/10.x/session#flash-data).

<!-- An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages). -->
`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에 의해 `$errors` 변수는 애플리케이션의 모든 뷰(view)에서 항상 사용할 수 있도록 자동으로 공유됩니다. 이 미들웨어는 `web` 미들웨어 그룹에 포함되어 있습니다. 따라서 여러분은 뷰 파일에서 `$errors` 변수를 항상 사용할 수 있고 `$errors` 변수가 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 클래스의 인스턴스입니다. 이 객체를 사용하는 방법이 궁금하다면 [check out its documentation](#working-with-error-messages)를 참고하세요.

<!-- So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view: -->
따라서, 이 예시에서는 검증 실패 시 사용자는 컨트롤러의 `create` 메서드로 리다이렉트되고, 뷰에서 에러 메시지를 표시할 수 있습니다:

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
<!-- #### Customizing the Error Messages -->
#### Customizing the Error Messages

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command. -->
Laravel에서 기본적으로 제공하는 유효성 검증 규칙마다 각각의 에러 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` 아티즌 명령어를 사용해 디렉토리를 만들 수 있습니다.

<!-- Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
`lang/en/validation.php` 파일에는 각각의 유효성 검증 규칙에 대한 번역 항목이 있습니다. 여러분은 애플리케이션에 맞게 이 메시지를 자유롭게 수정할 수 있습니다.

<!-- In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/10.x/localization). -->
또한, 이 파일을 원하는 언어 디렉토리로 복사하여 에러 메시지를 애플리케이션 언어에 맞게 번역할 수도 있습니다. Laravel의 다국어 지원 기능에 대해 더 자세히 알고 싶다면 [localization documentation](/docs/10.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션의 기본 구조(스캐폴딩)에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면, `lang:publish` 아티즌 명령어로 해당 파일을 퍼블리시해야 합니다.

<a name="quick-xhr-requests-and-validation"></a>
<!-- #### XHR Requests and Validation -->
#### XHR Requests and Validation

<!-- In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a [JSON response containing all of the validation errors](#validation-error-response-format). This JSON response will be sent with a 422 HTTP status code. -->
이 예제에서는 전통적인 폼을 사용하여 데이터를 애플리케이션에 전송했습니다. 하지만, 많은 애플리케이션에서는 자바스크립트로 구동되는 프론트엔드에서 XHR(비동기 HTTP) 요청을 받습니다. XHR 요청 중에 `validate` 메서드를 사용하는 경우, Laravel은 리다이렉트 응답을 생성하지 않고, 대신 [JSON response containing all of the validation errors](#validation-error-response-format)을 반환합니다. 이 JSON 응답은 422 HTTP 상태 코드로 전송됩니다.

<a name="the-at-error-directive"></a>
<!-- #### The `@error` Directive -->
#### The `@error` Directive

<!-- You may use the `@error` [Blade](/docs/10.x/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
주어진 속성(attribute)에 대한 유효성 검증 에러 메시지가 있는지 빠르게 확인해야 할 때는 [Blade](/docs/10.x/blade)의 `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 안에서 `$message` 변수를 출력해 에러 메시지를 바로 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- If you are using [named error bags](#named-error-bags), you may pass the name of the error bag as the second argument to the `@error` directive: -->
[named error bags](#named-error-bags)을 사용하는 경우, `@error` 디렉티브의 두 번째 인수로 에러 백의 이름을 넘길 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
<!-- ### Repopulating Forms -->
### Repopulating Forms

<!-- When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/10.x/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit. -->
Laravel은 유효성 검증 실패로 인해 리다이렉트 응답을 생성할 때, 프레임워크가 요청의 모든 입력값을 [flash all of the request's input to the session](/docs/10.x/session#flash-data)합니다. 이는 다음 요청에서 이전 입력값에 쉽게 접근하여, 사용자가 제출했던 폼을 편리하게 다시 표시할 수 있도록 하기 위함입니다.

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/10.x/session): -->
이전에 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. `old` 메서드는 [session](/docs/10.x/session)에서 플래시된 입력값을 불러옵니다:

```
$title = $request->old('title');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/10.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade template](/docs/10.x/blade)에서 이전 입력값을 표시할 때는 `old` 헬퍼를 사용하는 것이 더 간편합니다. 지정한 필드에 이전 입력값이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
<!-- ### A Note on Optional Fields -->
### A Note on Optional Fields

<!-- By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware are listed in the stack by the `App\Http\Kernel` class. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example: -->
기본적으로 Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함시킵니다. 이 미들웨어들은 `App\Http\Kernel` 클래스에 등록되어 있습니다. 이 때문에, "선택적(optional)" 요청 필드를 유효성 검증 시 `nullable`로 명시해야 `null` 값이 유효하지 않은 값으로 처리되지 않습니다. 예를 들어:

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

<!-- In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date. -->
이 예시에서 `publish_at` 필드는 `null`이거나, 날짜 포맷의 값이 모두 허용됩니다. 만약 규칙 지정 시 `nullable`을 추가하지 않으면, 검증기는 `null` 값을 유효하지 않은 날짜로 간주하니 주의해야 합니다.

<a name="validation-error-response-format"></a>
<!-- ### Validation Error Response Format -->
### Validation Error Response Format

<!-- When your application throws a `Illuminate\Validation\ValidationException` exception and the incoming HTTP request is expecting a JSON response, Laravel will automatically format the error messages for you and return a `422 Unprocessable Entity` HTTP response. -->
애플리케이션에서 `Illuminate\Validation\ValidationException` 예외를 발생시키고, 들어온 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 에러 메시지를 자동으로 포맷해서 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

<!-- Below, you can review an example of the JSON response format for validation errors. Note that nested error keys are flattened into "dot" notation format: -->
아래는 유효성 검증 에러에 대한 JSON 응답 예시입니다. 중첩된 에러 키는 "dot" 표기법으로 평탄화(flatten)되어 표현됩니다:

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
<!-- ## Form Request Validation -->
## Form Request Validation

<a name="creating-form-requests"></a>
<!-- ### Creating Form Requests -->
### Creating Form Requests

<!-- For more complex validation scenarios, you may wish to create a "form request". Form requests are custom request classes that encapsulate their own validation and authorization logic. To create a form request class, you may use the `make:request` Artisan CLI command: -->
좀 더 복잡한 유효성 검증 시나리오에서는 "폼 리퀘스트(form request)"를 생성해서 사용하는 것이 좋습니다. 폼 리퀘스트는 자체적으로 유효성 검증과 인가(authorization) 로직을 캡슐화하는 커스텀 리퀘스트 클래스입니다. 폼 리퀘스트 클래스를 생성하려면, `make:request` 아티즌 CLI 명령어를 사용하면 됩니다:

```shell
php artisan make:request StorePostRequest
```

<!-- The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`. -->
생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉토리에 위치하게 됩니다. 이 디렉토리가 원래 없었다면, `make:request` 명령어 실행과 동시에 자동 생성됩니다. Laravel에서 생성하는 각 폼 리퀘스트에는 `authorize`와 `rules` 두 가지 메서드가 포함되어 있습니다.

<!-- As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data: -->
예상하신 것처럼, `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 표현하는 동작을 수행할 수 있는지를 결정하는 역할을 하고, `rules` 메서드는 요청 데이터에 적용될 유효성 검증 규칙을 반환합니다:

```
/**
 * Get the validation rules that apply to the request.
 *
 * @return array<string, \Illuminate\Contracts\Validation\Rule|array|string>
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
> `rules` 메서드의 시그니처에 필요한 모든 의존성을 타입힌트로 선언하면, Laravel [service container](/docs/10.x/container)를 통해 자동으로 주입됩니다.

<!-- So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic: -->
그렇다면, 이 유효성 검증 규칙들은 언제 평가될까요? 컨트롤러 메서드에서 요청을 타입힌트로 받기만 하면 됩니다. 컨트롤러 메서드가 호출되기 전에 들어오는 폼 리퀘스트가 먼저 유효성 검증을 마치기 때문에, 컨트롤러에 별도의 유효성 검증 코드를 작성할 필요가 없습니다:

```
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

<!-- If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a [JSON representation of the validation errors](#validation-error-response-format). -->
유효성 검증에 실패하면, 사용자는 이전 위치로 리다이렉트되며, 에러도 세션에 플래시됩니다. 만약 요청이 XHR 요청이었다면 422 상태 코드의 HTTP 응답, 즉 [JSON representation of the validation errors](#validation-error-response-format)이 반환됩니다.

> [!NOTE]
> 인에르시아(Inertia) 기반 Laravel 프론트엔드에 실시간 폼 리퀘스트 유효성 검증을 추가해야 하나요? [Laravel Precognition](/docs/10.x/precognition)을 참고하세요.

<a name="performing-additional-validation-on-form-requests"></a>
<!-- #### Performing Additional Validation -->
#### Performing Additional Validation

<!-- Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the form request's `after` method. -->
때로는, 초기 유효성 검증이 완료된 이후에 추가 검증을 해야 할 수도 있습니다. 이럴 땐 폼 리퀘스트의 `after` 메서드를 사용합니다.

<!-- The `after` method should return an array of callables or closures which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary: -->
`after` 메서드는 콜러블(callable) 또는 클로저(closure)의 배열을 반환해야 하며, 유효성 검증 완료 후에 호출됩니다. 이 콜러블에는 `Illuminate\Validation\Validator` 인스턴스가 전달되므로, 필요시 추가 에러 메시지를 등록할 수 있습니다:

```
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

<!-- As noted, the array returned by the `after` method may also contain invokable classes. The `__invoke` method of these classes will receive an `Illuminate\Validation\Validator` instance: -->
설명한 것처럼, `after` 메서드가 반환하는 배열에는 바로 실행 가능한 클래스도 포함될 수 있습니다. 이런 클래스의 `__invoke` 메서드에는 `Illuminate\Validation\Validator` 인스턴스가 전달됩니다:

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
<!-- #### Stopping on the First Validation Failure -->
#### Stopping on the First Validation Failure

<!-- By adding a `stopOnFirstFailure` property to your request class, you may inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가하면, 하나의 검증 실패 발생 시 모든 속성(attribute)의 유효성 검증을 즉시 중단하도록 검증기에 알릴 수 있습니다:

```
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
<!-- #### Customizing the Redirect Location -->
#### Customizing the Redirect Location

<!-- As previously discussed, a redirect response will be generated to send the user back to their previous location when form request validation fails. However, you are free to customize this behavior. To do so, define a `$redirect` property on your form request: -->
앞서 설명한 것처럼, 폼 리퀘스트 유효성 검증 실패 시 사용자는 이전 위치로 리다이렉트됩니다. 하지만 이 동작을 자유롭게 변경할 수 있습니다. 폼 리퀘스트에 `$redirect` 프로퍼티를 정의하면 됩니다:

```
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

<!-- Or, if you would like to redirect users to a named route, you may define a `$redirectRoute` property instead: -->
또는, 네임드 라우트로 리다이렉트하고 싶다면 `$redirectRoute` 프로퍼티를 정의하면 됩니다:

```
/**
 * The route that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirectRoute = 'dashboard';
```

<a name="authorizing-form-requests"></a>
<!-- ### Authorizing Form Requests -->
### Authorizing Form Requests

<!-- The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/10.x/authorization) within this method: -->
폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드에서 인증된 사용자가 실제로 해당 리소스를 수정할 권한이 있는지 결정할 수 있습니다. 예를 들어, 사용자가 어떤 블로그 댓글을 수정하려고 하는데, 실제로 그 댓글의 작성자인지 확인할 수 있습니다. 일반적으로 이 메서드 안에서 [authorization gates and policies](/docs/10.x/authorization)을 활용하게 됩니다:

```
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

<!-- Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also, note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below: -->
모든 폼 리퀘스트는 Laravel의 기본 리퀘스트 클래스를 확장하므로, `user` 메서드로 현재 인증된 사용자를 얻을 수 있습니다. 또한 위 예시의 `route` 메서드를 보면, 호출된 라우트에서 정의한 URI 파라미터(예: `{comment}`)에 접근할 수 있습니다:

```
Route::post('/comment/{comment}');
```

<!-- Therefore, if your application is taking advantage of [route model binding](/docs/10.x/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request: -->
따라서, [route model binding](/docs/10.x/routing#route-model-binding)를 활용하면, 리퀘스트의 속성(property)으로 바로 바인딩된 모델 인스턴스를 사용할 수 있어 코드가 더 간결해집니다:

```
return $this->user()->can('update', $this->comment);
```

<!-- If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute. -->
만약 `authorize` 메서드가 `false`를 반환하면, Laravel은 자동으로 403 상태 코드의 HTTP 응답을 반환하며, 컨트롤러 메서드는 실행되지 않습니다.

<!-- If you plan to handle authorization logic for the request in another part of your application, you may remove the `authorize` method completely, or simply return `true`: -->
만약 요청의 인가(authorization) 로직을 애플리케이션의 다른 부분에서 처리할 계획이라면, `authorize` 메서드를 아예 삭제하거나, 항상 `true`를 반환하도록 만들 수도 있습니다:

```
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드의 시그니처에도 필요한 의존성을 타입힌트로 선언할 수 있습니다. Laravel [service container](/docs/10.x/container)에서 자동으로 주입해줍니다.

<a name="customizing-the-error-messages"></a>
<!-- ### Customizing the Error Messages -->
### Customizing the Error Messages

<!-- You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages: -->
폼 리퀘스트에서 사용하는 에러 메시지는 `messages` 메서드를 오버라이딩하면 커스터마이징할 수 있습니다. 이 메서드는 속성/규칙 쌍과 그에 대응하는 에러 메시지의 배열을 반환하면 됩니다:

```
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
<!-- #### Customizing the Validation Attributes -->
#### Customizing the Validation Attributes

<!-- Many of Laravel's built-in validation rule error messages contain an `:attribute` placeholder. If you would like the `:attribute` placeholder of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs: -->
Laravel의 기본 유효성 검증 에러 메시지에는 `:attribute` 플레이스홀더가 많이 포함되어 있습니다. 이 `:attribute`를 커스텀한 속성명으로 바꿔서 표시하고 싶을 때는 `attributes` 메서드를 오버라이딩하면 됩니다. 이 메서드는 속성/표시명 쌍의 배열을 반환해야 합니다:

```
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
<!-- ### Preparing Input for Validation -->
### Preparing Input for Validation

<!-- If you need to prepare or sanitize any data from the request before you apply your validation rules, you may use the `prepareForValidation` method: -->
유효성 검증 규칙을 적용하기 전, 요청의 일부 데이터를 준비하거나 정제(sanitize)해야 할 필요가 있다면, `prepareForValidation` 메서드를 사용할 수 있습니다:

```
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

<!-- Likewise, if you need to normalize any request data after validation is complete, you may use the `passedValidation` method: -->
마찬가지로, 유효성 검증이 끝난 뒤 요청 데이터의 정규화 작업이 필요하다면, `passedValidation` 메서드를 사용할 수 있습니다:

```
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>

<!-- ## Manually Creating Validators -->
## Manually Creating Validators

<!-- If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/10.x/facades). The `make` method on the facade generates a new validator instance: -->
요청에서 `validate` 메서드를 사용하지 않고 직접 validator 인스턴스를 생성하고 싶다면, `Validator` [facade](/docs/10.x/facades)를 사용할 수 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

```
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
            return redirect('post/create')
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

<!-- The first argument passed to the `make` method is the data under validation. The second argument is an array of the validation rules that should be applied to the data. -->
`make` 메서드의 첫 번째 인수에는 유효성 검사를 진행할 데이터를 전달합니다. 두 번째 인수에는 해당 데이터에 적용할 유효성 검사 규칙의 배열을 전달합니다.

<!-- After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`. -->
요청의 유효성 검사가 실패했는지 판별한 후에는, `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면, 리다이렉션 후에 `$errors` 변수가 자동으로 뷰에 공유되어 사용자가 에러 메시지를 쉽게 확인할 수 있습니다. `withErrors` 메서드에는 validator, `MessageBag`, 또는 PHP `array`를 전달할 수 있습니다.

<!-- #### Stopping on First Validation Failure -->
#### Stopping on First Validation Failure

<!-- The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`stopOnFirstFailure` 메서드를 사용하면, 하나의 유효성 검사가 실패하면 이후의 모든 속성에 대한 검증을 멈추도록 validator에 알릴 수 있습니다.

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
<!-- ### Automatic Redirection -->
### Automatic Redirection

<!-- If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a [JSON response will be returned](#validation-error-response-format): -->
validator 인스턴스를 수동으로 생성하더라도 HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 함께 활용하고 싶다면, 기존 validator 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 유효성 검사가 실패하면 사용자는 자동으로 리다이렉트되거나, XHR 요청인 경우 [JSON response will be returned](#validation-error-response-format)됩니다.

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

<!-- You may use the `validateWithBag` method to store the error messages in a [named error bag](#named-error-bags) if validation fails: -->
유효성 검사 실패 시 에러 메시지를 [named error bag](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
<!-- ### Named Error Bags -->
### Named Error Bags

<!-- If you have multiple forms on a single page, you may wish to name the `MessageBag` containing the validation errors, allowing you to retrieve the error messages for a specific form. To achieve this, pass a name as the second argument to `withErrors`: -->
하나의 페이지에 여러 폼이 있는 경우, 유효성 검사 에러를 담고 있는 `MessageBag`에 이름을 붙여서 특정 폼에 대한 에러 메시지만 가져오고 싶을 수 있습니다. 이를 위해 `withErrors`의 두 번째 인수로 이름을 전달하면 됩니다.

```
return redirect('register')->withErrors($validator, 'login');
```

<!-- You may then access the named `MessageBag` instance from the `$errors` variable: -->
이후에는 `$errors` 변수에서 명명된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
<!-- ### Customizing the Error Messages -->
### Customizing the Error Messages

<!-- If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method: -->
필요하다면 validator 인스턴스가 기본적으로 제공하는 Laravel의 에러 메시지 대신 커스텀 에러 메시지를 사용할 수 있습니다. 커스텀 메시지는 여러 방법으로 지정할 수 있습니다. 가장 먼저, `Validator::make`의 세 번째 인수로 메시지 배열을 전달하는 방법이 있습니다.

```
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

<!-- In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example: -->
이 예시에서 `:attribute` 플레이스홀더는 실제 유효성 검사가 적용되는 필드명으로 대체됩니다. 또한, 유효성 검사 메시지에는 다양한 플레이스홀더를 사용할 수 있습니다. 예를 들어:

```
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
<!-- #### Specifying a Custom Message for a Given Attribute -->
#### Specifying a Custom Message for a Given Attribute

<!-- Sometimes you may wish to specify a custom error message only for a specific attribute. You may do so using "dot" notation. Specify the attribute's name first, followed by the rule: -->
특정 속성에만 커스텀 에러 메시지를 지정하고 싶을 때는 "도트" 표기법을 사용하면 됩니다. 먼저 속성명을 적고 그 뒤에 규칙명을 적습니다.

```
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
<!-- #### Specifying Custom Attribute Values -->
#### Specifying Custom Attribute Values

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method: -->
Laravel의 기본 에러 메시지에는 보통 `:attribute` 플레이스홀더가 들어 있는데, 이는 해당 속성명으로 대체됩니다. 특정 필드에 대해 이 플레이스홀더가 표시되는 값을 바꾸고 싶다면, `Validator::make`의 네 번째 인수로 커스텀 속성 배열을 전달하세요.

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
<!-- ### Performing Additional Validation -->
### Performing Additional Validation

<!-- Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the validator's `after` method. The `after` method accepts a closure or an array of callables which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary: -->
처음 유효성 검사 후에 별도의 추가 검증이 필요하다면, validator의 `after` 메서드를 사용할 수 있습니다. `after` 메서드는 검증이 끝난 후에 호출되는 클로저 또는 콜러블(callable)의 배열을 인수로 받습니다. 전달한 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아서, 필요한 경우 추가적인 에러 메시지를 등록할 수 있습니다.

```
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

<!-- As noted, the `after` method also accepts an array of callables, which is particularly convenient if your "after validation" logic is encapsulated in invokable classes, which will receive an `Illuminate\Validation\Validator` instance via their `__invoke` method: -->
위에서 설명했듯이, `after` 메서드는 콜러블 배열도 받을 수 있습니다. "검증 이후 로직"이 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받는 호출 가능한 클래스에 캡슐화되어 있다면 더욱 편리합니다.

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
<!-- ## Working With Validated Input -->
## Working With Validated Input

<!-- After validating incoming request data using a form request or a manually created validator instance, you may wish to retrieve the incoming request data that actually underwent validation. This can be accomplished in several ways. First, you may call the `validated` method on a form request or validator instance. This method returns an array of the data that was validated: -->
폼 리퀘스트 또는 직접 생성한 validator 인스턴스를 사용해 들어온 요청 데이터를 검증한 뒤, 실제로 검증을 통과한 입력 데이터를 가져오고 싶을 수 있습니다. 이를 위해 몇 가지 방법이 있습니다. 먼저, 폼 리퀘스트나 validator 인스턴스에서 `validated` 메서드를 호출하면, 검증된 데이터의 배열을 반환합니다.

```
$validated = $request->validated();

$validated = $validator->validated();
```

<!-- Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data: -->
또는, 폼 리퀘스트나 validator 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 반환된 객체는 `only`, `except`, `all` 메서드를 제공하여 검증된 데이터의 일부만 선택하거나, 전체를 배열로 반환할 수 있습니다.

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

<!-- In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array: -->
또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 순회하거나 배열 인덱스로 접근할 수 있습니다.

```
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

<!-- If you would like to add additional fields to the validated data, you may call the `merge` method: -->
추가적으로 검증된 데이터에 필드를 덧붙이고 싶다면, `merge` 메서드를 사용할 수 있습니다.

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

<!-- If you would like to retrieve the validated data as a [collection](/docs/10.x/collections) instance, you may call the `collect` method: -->
검증된 데이터를 [collection](/docs/10.x/collections) 인스턴스로 받아 활용하고 싶다면, `collect` 메서드를 호출하면 됩니다.

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
<!-- ## Working With Error Messages -->
## Working With Error Messages

<!-- After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class. -->
`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 에러 메시지를 다루기에 편리한 `Illuminate\Support\MessageBag` 인스턴스를 얻을 수 있습니다. 뷰에서 자동으로 사용할 수 있는 `$errors` 변수도 바로 이 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
<!-- #### Retrieving the First Error Message for a Field -->
#### Retrieving the First Error Message for a Field

<!-- To retrieve the first error message for a given field, use the `first` method: -->
특정 필드에 대해 첫 번째 에러 메시지만 가져오고 싶다면 `first` 메서드를 사용하세요.

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
<!-- #### Retrieving All Error Messages for a Field -->
#### Retrieving All Error Messages for a Field

<!-- If you need to retrieve an array of all the messages for a given field, use the `get` method: -->
특정 필드에 대한 모든 에러 메시지를 배열로 받고 싶다면 `get` 메서드를 사용하세요.

```
foreach ($errors->get('email') as $message) {
    // ...
}
```

<!-- If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character: -->
배열 형태의 폼 필드를 검증하는 경우, `*` 문자를 사용해 각 요소에 대한 모든 메시지를 가져올 수도 있습니다.

```
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
<!-- #### Retrieving All Error Messages for All Fields -->
#### Retrieving All Error Messages for All Fields

<!-- To retrieve an array of all messages for all fields, use the `all` method: -->
폼의 모든 필드에 대한 모든 메시지를 배열로 받고자 한다면 `all` 메서드를 사용하세요.

```
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
<!-- #### Determining if Messages Exist for a Field -->
#### Determining if Messages Exist for a Field

<!-- The `has` method may be used to determine if any error messages exist for a given field: -->
`has` 메서드는 특정 필드에 대한 에러 메시지가 존재하는지 확인할 때 사용할 수 있습니다.

```
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
<!-- ### Specifying Custom Messages in Language Files -->
### Specifying Custom Messages in Language Files

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command. -->
Laravel의 기본 유효성 검사 규칙은 각각의 에러 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 만약 프로젝트에 `lang` 디렉터리가 없다면, `lang:publish` Artisan 명령어로 생성할 수 있습니다.

<!-- Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
`lang/en/validation.php` 파일에는 각 유효성 검사 규칙별로 변환 항목이 존재합니다. 애플리케이션의 요구에 따라 이 메시지들을 자유롭게 수정할 수 있습니다.

<!-- In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/10.x/localization). -->
또한, 이 파일을 다른 언어 디렉터리로 복사해 애플리케이션 언어에 맞도록 메시지를 번역할 수 있습니다. Laravel의 지역화에 관해 더 자세히 알고 싶다면 [localization documentation](/docs/10.x/localization)를 참고하세요.

> [!WARNING]
> 기본적으로 Laravel 앱 스캐폴딩(기본 코드 구조)에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용하여 파일을 배포해야 합니다.

<a name="custom-messages-for-specific-attributes"></a>
<!-- #### Custom Messages for Specific Attributes -->
#### Custom Messages for Specific Attributes

<!-- You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file: -->
특정 속성명과 규칙 조합에 대해 언어 파일에서 사용할 에러 메시지를 커스터마이징하려면, 애플리케이션의 `lang/xx/validation.php` 언어 파일의 `custom` 배열에 해당 내용을 추가합니다.

```
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
<!-- ### Specifying Attributes in Language Files -->
### Specifying Attributes in Language Files

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. If you would like the `:attribute` portion of your validation message to be replaced with a custom value, you may specify the custom attribute name in the `attributes` array of your `lang/xx/validation.php` language file: -->
Laravel의 기본 에러 메시지에는 보통 `:attribute` 플레이스홀더가 사용되며, 이는 유효성 검사를 거치는 필드명으로 대체됩니다. 만약 유효성 검사 메시지의 `:attribute` 부분을 커스텀 값으로 대체하고 싶다면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에서 커스텀 속성명을 지정할 수 있습니다.

```
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 앱 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용해야 합니다.

<a name="specifying-values-in-language-files"></a>
<!-- ### Specifying Values in Language Files -->
### Specifying Values in Language Files

<!-- Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`: -->
Laravel의 몇몇 기본 유효성 검사 에러 메시지에는 `:value` 플레이스홀더가 사용되며, 이는 해당 속성의 실제 값으로 대체됩니다. 그러나, 경우에 따라 `:value` 부분을 더 사용자 친화적인 값으로 바꿔주고 싶을 때가 있습니다. 예를 들어, `payment_type`이 `cc`일 때 카드 번호가 필수임을 지정하는 아래 규칙을 보겠습니다.

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

<!-- If this validation rule fails, it will produce the following error message: -->
이 유효성 검사가 실패한다면, 다음과 같은 에러 메시지가 표시됩니다.

```none
The credit card number field is required when payment type is cc.
```

<!-- Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `lang/xx/validation.php` language file by defining a `values` array: -->
여기서 `cc` 대신 좀 더 알아보기 쉬운 값 표시를 원한다면, `lang/xx/validation.php` 언어 파일의 `values` 배열에서 바꿔줄 수 있습니다.

```
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel 앱 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어를 사용해야 합니다.

<!-- After defining this value, the validation rule will produce the following error message: -->
이렇게 값을 정의하면 유효성 검사 규칙이 다음과 같은 에러 메시지를 보여주게 됩니다.

```none
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
<!-- ## Available Validation Rules -->
## Available Validation Rules

<!-- Below is a list of all available validation rules and their function: -->
아래는 사용 가능한 모든 유효성 검사 규칙과 해당 기능을 정리한 목록입니다.



<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Active URL](#rule-active-url)
[After (Date)](#rule-after)
[After Or Equal (Date)](#rule-after-or-equal)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Array](#rule-array)
[Ascii](#rule-ascii)
[Bail](#rule-bail)
[Before (Date)](#rule-before)
[Before Or Equal (Date)](#rule-before-or-equal)
[Between](#rule-between)
[Boolean](#rule-boolean)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Decimal](#rule-decimal)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Dimensions (Image Files)](#rule-dimensions)
[Distinct](#rule-distinct)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Exists (Database)](#rule-exists)
[Extensions](#rule-extensions)
[File](#rule-file)
[Filled](#rule-filled)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Hex Color](#rule-hex-color)
[Image (File)](#rule-image)
[In](#rule-in)
[In Array](#rule-in-array)
[Integer](#rule-integer)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Multiple Of](#rule-multiple-of)
[Not In](#rule-not-in)
[Not Regex](#rule-not-regex)
[Nullable](#rule-nullable)
[Numeric](#rule-numeric)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Regular Expression](#rule-regex)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#validating-when-present)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[Unique (Database)](#rule-unique)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)
-->
[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Active URL](#rule-active-url)
[After (Date)](#rule-after)
[After Or Equal (Date)](#rule-after-or-equal)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Array](#rule-array)
[Ascii](#rule-ascii)
[Bail](#rule-bail)
[Before (Date)](#rule-before)
[Before Or Equal (Date)](#rule-before-or-equal)
[Between](#rule-between)
[Boolean](#rule-boolean)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Decimal](#rule-decimal)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Dimensions (Image Files)](#rule-dimensions)
[Distinct](#rule-distinct)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Exists (Database)](#rule-exists)
[Extensions](#rule-extensions)
[File](#rule-file)
[Filled](#rule-filled)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Hex Color](#rule-hex-color)
[Image (File)](#rule-image)
[In](#rule-in)
[In Array](#rule-in-array)
[Integer](#rule-integer)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Multiple Of](#rule-multiple-of)
[Not In](#rule-not-in)
[Not Regex](#rule-not-regex)
[Nullable](#rule-nullable)
[Numeric](#rule-numeric)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Regular Expression](#rule-regex)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#validating-when-present)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[Unique (Database)](#rule-unique)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

<!-- </div> -->
</div>

<a name="rule-accepted"></a>
<!-- #### accepted -->
#### accepted

<!-- The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. This is useful for validating "Terms of Service" acceptance or similar fields. -->
해당 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값을 가져야 합니다. 주로 "서비스 약관 동의" 같은 항목을 검증할 때 유용하게 사용할 수 있습니다.

<a name="rule-accepted-if"></a>
<!-- #### accepted_if:anotherfield,value,... -->
#### accepted_if:anotherfield,value,...

<!-- The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields. -->
해당 필드는, 유효성 검사 중인 다른 필드가 특정 값과 같을 때 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값을 필수로 가져야 합니다. 마찬가지로 "서비스 약관 동의"와 같은 입력을 조건부로 검증할 때 활용할 수 있습니다.

<a name="rule-active-url"></a>
<!-- #### active_url -->
#### active_url

<!-- The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`. -->
해당 필드는 `dns_get_record` PHP 함수에 따라 A 또는 AAAA 레코드가 유효하게 존재하는 값이어야 합니다. URL에서 호스트명은 `parse_url` PHP 함수로 추출된 뒤 `dns_get_record`로 전달됩니다.

<a name="rule-after"></a>
<!-- #### after:_date_ -->
#### after:_date_

<!-- The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance: -->
해당 필드는 지정한 날짜 이후의 값이어야 합니다. 전달된 날짜 문자열은 내부적으로 `strtotime` PHP 함수로 변환되어 유효한 `DateTime` 인스턴스와 비교됩니다.

```
'start_date' => 'required|date|after:tomorrow'
```

<!-- Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date: -->
`strtotime`으로 평가할 날짜 문자열을 직접 전달하는 대신, 비교 대상으로 다른 필드명을 지정할 수도 있습니다.

```
'finish_date' => 'required|date|after:start_date'
```

<a name="rule-after-or-equal"></a>
<!-- #### after\_or\_equal:_date_ -->
#### after\_or\_equal:_date_

<!-- The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule. -->
해당 필드는 지정한 날짜 이후 또는 같은 날짜여야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하세요.

<a name="rule-alpha"></a>
<!-- #### alpha -->
#### alpha

<!-- The field under validation must be entirely Unicode alphabetic characters contained in [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) and [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=). -->
해당 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함된 유니코드 알파벳 문자만을 포함해야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
이 규칙을 ASCII 범위의 문자(`a-z`, `A-Z`)로 제한하려면, 검증 규칙에 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
<!-- #### alpha_dash -->
#### alpha_dash

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), as well as ASCII dashes (`-`) and ASCII underscores (`_`). -->
해당 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 유니코드 영문자, 숫자 그리고 ASCII 대시(`-`), 언더스코어(`_`)만을 포함해야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
이 규칙을 ASCII 범위(`a-z` 및 `A-Z`)로 제한하고 싶다면, 마찬가지로 `ascii` 옵션을 사용할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
<!-- #### alpha_num -->
#### alpha_num

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), and [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=). -->
해당 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 유니코드 영문자 또는 숫자만을 포함해야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
ASCII 범위(`a-z` 및 `A-Z`)만 허용할 경우 `ascii` 옵션을 지정하세요.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
<!-- #### array -->
#### array

<!-- The field under validation must be a PHP `array`. -->
해당 필드는 PHP의 `array` 타입이어야 합니다.

<!-- When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule: -->
`array` 규칙에 값을 추가로 지정하면, 입력 배열에 포함된 각 키가 반드시 규칙에서 지정한 목록에 포함되어야 합니다. 다음 예시에서 입력 배열의 `admin` 키는 `array` 규칙의 허용 목록에 없으므로 유효하지 않습니다.

```
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

<!-- In general, you should always specify the array keys that are allowed to be present within your array. -->
일반적으로 배열의 허용 가능한 키 목록을 명확히 지정하는 것이 좋습니다.

<a name="rule-ascii"></a>

<!-- #### ascii -->
#### ascii

<!-- The field under validation must be entirely 7-bit ASCII characters. -->
검증 대상 필드는 반드시 7비트 ASCII 문자만으로 이루어져야 합니다.

<a name="rule-bail"></a>
<!-- #### bail -->
#### bail

<!-- Stop running validation rules for the field after the first validation failure. -->
해당 필드에서 첫 번째 유효성 검사 실패가 발생하면 이후의 유효성 검사 규칙 적용을 중단합니다.

<!-- While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`bail` 규칙은 특정 필드에 대해서만 유효성 검사를 중단합니다. 반면, `stopOnFirstFailure` 메서드는 하나의 유효성 검사 실패가 발생하면 모든 속성의 검증을 즉시 멈추도록 validator에 지시합니다.

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
<!-- #### before:_date_ -->
#### before:_date_

<!-- The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
검증 대상 필드는 지정된 날짜보다 이전이어야 합니다. 입력된 날짜 값은 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다. 또한, [`after`](#rule-after) 규칙과 마찬가지로, `date` 값 대신 검증 중인 다른 필드명을 지정할 수도 있습니다.

<a name="rule-before-or-equal"></a>
<!-- #### before\_or\_equal:_date_ -->
#### before\_or\_equal:_date_

<!-- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
검증 대상 필드는 지정된 날짜 이전이거나 그 날짜와 동일해야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 처리되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한, [`after`](#rule-after) 규칙과 동일하게, `date` 값으로 검증 중인 다른 필드명을 지정할 수도 있습니다.

<a name="rule-between"></a>
<!-- #### between:_min_,_max_ -->
#### between:_min_,_max_

<!-- The field under validation must have a size between the given _min_ and _max_ (inclusive). Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
검증 대상 필드의 크기가 지정된 _min_과 _max_ 사이(포함)여야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 판단됩니다.

<a name="rule-boolean"></a>
<!-- #### boolean -->
#### boolean

<!-- The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`. -->
검증 대상 필드는 불리언(boolean) 타입으로 변환될 수 있어야 합니다. 허용되는 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"` 입니다.

<a name="rule-confirmed"></a>
<!-- #### confirmed -->
#### confirmed

<!-- The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input. -->
검증 대상 필드는 `{field}_confirmation`과 동일한 값이어야 합니다. 예를 들어, 검증 대상 필드가 `password`라면 입력 데이터에 `password_confirmation` 필드가 존재해야 하며 값이 일치해야 합니다.

<a name="rule-current-password"></a>
<!-- #### current_password -->
#### current_password

<!-- The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/10.x/authentication) using the rule's first parameter: -->
검증 대상 필드는 인증된(로그인 중인) 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 파라미터로 [authentication guard](/docs/10.x/authentication)를 지정할 수 있습니다.

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
<!-- #### date -->
#### date

<!-- The field under validation must be a valid, non-relative date according to the `strtotime` PHP function. -->
검증 대상 필드는 PHP의 `strtotime` 함수 기준으로 유효한(상대적인 값이 아닌) 날짜여야 합니다.

<a name="rule-date-equals"></a>
<!-- #### date_equals:_date_ -->
#### date_equals:_date_

<!-- The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. -->
검증 대상 필드는 지정된 날짜와 동일해야 합니다. 날짜 값은 PHP의 `strtotime` 함수로 변환되어 유효한 `DateTime` 인스턴스로 처리됩니다.

<a name="rule-date-format"></a>
<!-- #### date_format:_format_,... -->
#### date_format:_format_,...

<!-- The field under validation must match one of the given _formats_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class. -->
검증 대상 필드는 지정된 _formats_ 중 하나와 일치해야 합니다. 필드 유효성 검사 시에는 `date` 또는 `date_format` 중 하나만 사용해야 하며, 두 가지를 함께 적용해서는 안 됩니다. 이 유효성 검사 규칙은 PHP [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 형식을 지원합니다.

<a name="rule-decimal"></a>
<!-- #### decimal:_min_,_max_ -->
#### decimal:_min_,_max_

<!-- The field under validation must be numeric and must contain the specified number of decimal places: -->
검증 대상 필드는 숫자여야 하며, 소수점 자리수가 지정된 범위와 일치해야 합니다.

```
// Must have exactly two decimal places (9.99)...
'price' => 'decimal:2'

// Must have between 2 and 4 decimal places...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
<!-- #### declined -->
#### declined

<!-- The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-declined-if"></a>
<!-- #### declined_if:anotherfield,value,... -->
#### declined_if:anotherfield,value,...

<!-- The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"` if another field under validation is equal to a specified value. -->
특정 다른 검증 대상 필드가 지정된 값과 같을 때, 검증 대상 필드는 반드시 `"no"`, `"off"`, `0`, `"0"`, `false`, `"false"` 중 하나의 값이어야 합니다.

<a name="rule-different"></a>
<!-- #### different:_field_ -->
#### different:_field_

<!-- The field under validation must have a different value than _field_. -->
검증 대상 필드는 _field_와는 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
<!-- #### digits:_value_ -->
#### digits:_value_

<!-- The integer under validation must have an exact length of _value_. -->
검증 대상 정수(integer)는 정확히 _value_ 자리여야 합니다.

<a name="rule-digits-between"></a>
<!-- #### digits_between:_min_,_max_ -->
#### digits_between:_min_,_max_

<!-- The integer validation must have a length between the given _min_ and _max_. -->
검증 대상 정수의 자릿수는 _min_과 _max_ 사이여야 합니다.

<a name="rule-dimensions"></a>
<!-- #### dimensions -->
#### dimensions

<!-- The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters: -->
검증 대상 파일이 아래 인자 조건을 만족하는 이미지(사진 등)여야 합니다.

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

<!-- Available constraints are: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_. -->
사용 가능한 조건에는: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_ 가 있습니다.

<!-- A _ratio_ constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`: -->
_ratio_ 값은 width(가로)을 height(세로)로 나눈 비율로 표현하며, `3/2` 같은 분수나 `1.5`와 같은 실수 형태 모두 허용됩니다.

```
'avatar' => 'dimensions:ratio=3/2'
```

<!-- Since this rule requires several arguments, you may use the `Rule::dimensions` method to fluently construct the rule: -->
이 규칙은 여러 인자를 필요로 하므로, `Rule::dimensions` 메서드를 사용해 유창하게(rule chaining) 규칙을 정의할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
    ],
]);
```

<a name="rule-distinct"></a>
<!-- #### distinct -->
#### distinct

<!-- When validating arrays, the field under validation must not have any duplicate values: -->
배열을 검증할 때, 해당 필드에는 중복된 값이 없어야 합니다.

```
'foo.*.id' => 'distinct'
```

<!-- Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition: -->
Distinct는 기본적으로 느슨한(==) 비교를 사용합니다. 엄격한(===) 비교를 원한다면 `strict` 파라미터를 추가합니다.

```
'foo.*.id' => 'distinct:strict'
```

<!-- You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences: -->
대소문자 구분을 무시하려면 `ignore_case` 파라미터를 추가할 수 있습니다.

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
<!-- #### doesnt_start_with:_foo_,_bar_,... -->
#### doesnt_start_with:_foo_,_bar_,...

<!-- The field under validation must not start with one of the given values. -->
검증 대상 필드는 지정된 값들 중 하나로 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
<!-- #### doesnt_end_with:_foo_,_bar_,... -->
#### doesnt_end_with:_foo_,_bar_,...

<!-- The field under validation must not end with one of the given values. -->
검증 대상 필드는 지정된 값들 중 하나로 끝나서는 안 됩니다.

<a name="rule-email"></a>
<!-- #### email -->
#### email

<!-- The field under validation must be formatted as an email address. This validation rule utilizes the [`egulias/email-validator`](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well: -->
검증 대상 필드는 이메일 주소 형태여야 합니다. 이 규칙은 이메일 주소를 검증하기 위해 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 방식이 적용되나, 다른 스타일도 선택해 적용할 수 있습니다.

```
'email' => 'email:rfc,dns'
```

<!-- The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply: -->
위 예시는 `RFCValidation`과 `DNSCheckValidation`을 적용합니다. 적용 가능한 모든 검증 스타일은 다음과 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`
- `filter_unicode`: `FilterEmailValidation::unicode()`
-->
- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`
- `filter_unicode`: `FilterEmailValidation::unicode()`

<!-- </div> -->
</div>

<!-- The `filter` validator, which uses PHP's `filter_var` function, ships with Laravel and was Laravel's default email validation behavior prior to Laravel version 5.8. -->
`filter` 검증기는 PHP의 `filter_var` 함수를 활용하며, 이는 Laravel 5.8 이전의 기본 이메일 검증 방식이기도 했습니다.

> [!WARNING]
> `dns`와 `spoof` 검증기는 PHP의 `intl` 확장(extension)이 필요합니다.

<a name="rule-ends-with"></a>
<!-- #### ends_with:_foo_,_bar_,... -->
#### ends_with:_foo_,_bar_,...

<!-- The field under validation must end with one of the given values. -->
검증 대상 필드는 지정된 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
<!-- #### enum -->
#### enum

<!-- The `Enum` rule is a class based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument. When validating primitive values, a backed Enum should be provided to the `Enum` rule: -->
`Enum` 규칙은 클래스 기반 규칙으로, 검증 대상 필드가 올바른 enum(열거형) 값인지 확인합니다. `Enum` 규칙은 생성자 인자로 enum 클래스명을 받습니다. Primitive 값을 검증할 때에는 backed `Enum`을 넘겨주어야 합니다.

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

<!-- The `Enum` rule's `only` and `except` methods may be used to limit which enum cases should be considered valid: -->
`Enum` 규칙의 `only` 및 `except` 메서드를 사용하면 특정 enum case만 유효하도록 한정할 수 있습니다.

```
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

<!-- The `when` method may be used to conditionally modify the `Enum` rule: -->
`when` 메서드는 조건적으로 `Enum` 규칙을 수정할 수 있도록 도와줍니다.

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
<!-- #### exclude -->
#### exclude

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods. -->
검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
<!-- #### exclude_if:_anotherfield_,_value_ -->
#### exclude_if:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_. -->
_anotherfield_ 필드가 _value_와 동일하면, 검증 대상 필드는 `validate` 및 `validated`가 반환하는 요청 데이터에서 제외됩니다.

<!-- If complex conditional exclusion logic is required, you may utilize the `Rule::excludeIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be excluded: -->
복잡한 조건으로 필드를 제외해야 할 경우, `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 혹은 클로저를 인자로 받으며, 클로저의 반환값이 `true`이면 해당 필드는 제외되고, `false`면 유지됩니다.

```
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
<!-- #### exclude_unless:_anotherfield_,_value_ -->
#### exclude_unless:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless _anotherfield_'s field is equal to _value_. If _value_ is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data. -->
_anotherfield_ 필드가 _value_와 같지 않으면, 검증 대상 필드는 `validate` 및 `validated`가 반환하는 요청 데이터에서 제외됩니다. _value_가 `null`(예: `exclude_unless:name,null`)인 경우, 비교 필드가 `null`이거나 요청 데이터에서 해당 필드가 없으면 제외됩니다.

<a name="rule-exclude-with"></a>
<!-- #### exclude_with:_anotherfield_ -->
#### exclude_with:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is present. -->
_anotherfield_ 필드가 존재할 경우, 검증 대상 필드는 `validate` 및 `validated`가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
<!-- #### exclude_without:_anotherfield_ -->
#### exclude_without:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present. -->
_anotherfield_ 필드가 존재하지 않을 경우, 검증 대상 필드는 `validate` 및 `validated`가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
<!-- #### exists:_table_,_column_ -->
#### exists:_table_,_column_

<!-- The field under validation must exist in a given database table. -->
검증 대상 필드의 값이 지정한 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
<!-- #### Basic Usage of Exists Rule -->
#### Basic Usage of Exists Rule

```
'state' => 'exists:states'
```

<!-- If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value. -->
`column` 옵션을 명시하지 않으면, 필드명이 그대로 사용됩니다. 위 예시에서는 `states` 테이블에서 `state` 컬럼 값이 요청의 `state` 속성과 일치하는 레코드가 존재하는지 확인합니다.

<a name="specifying-a-custom-column-name"></a>
<!-- #### Specifying a Custom Column Name -->
#### Specifying a Custom Column Name

<!-- You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name: -->
검증 규칙에서 사용할 데이터베이스 컬럼명을 테이블명 뒤에 명시적으로 작성할 수 있습니다.

```
'state' => 'exists:states,abbreviation'
```

<!-- Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name: -->
특정 데이터베이스 연결을 사용하여 `exists` 쿼리를 실행하고 싶을 때는, 테이블명 앞에 연결명을 추가할 수 있습니다.

```
'email' => 'exists:connection.staff,email'
```

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블명을 직접 작성하는 대신, Eloquent 모델명을 지정해서 테이블명을 결정하게 할 수도 있습니다.

```
'user_id' => 'exists:App\Models\User,id'
```

<!-- If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them: -->
`Rule` 클래스를 사용하면, 쿼리를 직접 커스터마이즈할 수도 있으며, 규칙 배열을 사용해 유효성 검증 규칙을 구분자 `|` 대신 배열로 지정할 수 있습니다.

```
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            return $query->where('account_id', 1);
        }),
    ],
]);
```

<!-- You may explicitly specify the database column name that should be used by the `exists` rule generated by the `Rule::exists` method by providing the column name as the second argument to the `exists` method: -->
`Rule::exists` 메서드가 생성하는 `exists` 규칙에서 사용할 컬럼명은 `exists` 메서드의 두 번째 인자로 명시할 수 있습니다.

```
'state' => Rule::exists('states', 'abbreviation'),
```

<a name="rule-extensions"></a>
<!-- #### extensions:_foo_,_bar_,... -->
#### extensions:_foo_,_bar_,...

<!-- The file under validation must have a user-assigned extension corresponding to one of the listed extensions: -->
검증 대상 파일은 반드시 지정된 확장자 중 하나를 사용해야 합니다.

```
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 사용자 정의 확장자만으로 파일을 검증하는 것은 권장되지 않습니다. 이 규칙은 보통 [`mimes`](#rule-mimes)나 [`mimetypes`](#rule-mimetypes) 규칙과 결합해서 사용하는 것이 바람직합니다.

<a name="rule-file"></a>
<!-- #### file -->
#### file

<!-- The field under validation must be a successfully uploaded file. -->
검증 대상 필드는 정상적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
<!-- #### filled -->
#### filled

<!-- The field under validation must not be empty when it is present. -->
검증 대상 필드는 값이 비어 있지 않아야 합니다(존재할 경우).

<a name="rule-gt"></a>
<!-- #### gt:_field_ -->
#### gt:_field_

<!-- The field under validation must be greater than the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_ 혹은 _value_보다 커야 합니다. 두 필드는 반드시 동일한 타입이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 처리됩니다.

<a name="rule-gte"></a>
<!-- #### gte:_field_ -->
#### gte:_field_

<!-- The field under validation must be greater than or equal to the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_ 혹은 _value_보다 크거나 같아야 합니다. 두 필드는 반드시 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일하게 판단합니다.

<a name="rule-hex-color"></a>
<!-- #### hex_color -->
#### hex_color

<!-- The field under validation must contain a valid color value in [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) format. -->
검증 대상 필드는 [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 올바른 색상 값이어야 합니다.

<a name="rule-image"></a>
<!-- #### image -->
#### image

<!-- The file under validation must be an image (jpg, jpeg, png, bmp, gif, svg, or webp). -->
검증 대상 파일은 이미지이어야 하며, 형식은 jpg, jpeg, png, bmp, gif, svg, webp 중 하나여야 합니다.

<a name="rule-in"></a>
<!-- #### in:_foo_,_bar_,... -->
#### in:_foo_,_bar_,...

<!-- The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule: -->
검증 대상 필드는 지정된 값 목록 중 하나에 포함되어야 합니다. 이 규칙은 배열 값을 `implode`해야 하는 경우가 많기 때문에, `Rule::in` 메서드를 활용해 좀 더 읽기 쉽게 규칙을 작성할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

<!-- When the `in` rule is combined with the `array` rule, each value in the input array must be present within the list of values provided to the `in` rule. In the following example, the `LAS` airport code in the input array is invalid since it is not contained in the list of airports provided to the `in` rule: -->
`in` 규칙이 `array` 규칙과 함께 사용되면, 입력 배열의 각각의 값이 반드시 `in` 규칙에 지정된 값 목록 중 하나에 포함되어야 합니다. 아래 예시에서 입력값 배열 중 `LAS`는 `in` 규칙에 제공된 리스트에 없으므로 유효하지 않습니다.

```
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
<!-- #### in_array:_anotherfield_.* -->
#### in_array:_anotherfield_.*

<!-- The field under validation must exist in _anotherfield_'s values. -->
검증 대상 필드의 값이 _anotherfield_ 배열의 값 중 하나여야 합니다.

<a name="rule-integer"></a>
<!-- #### integer -->
#### integer

<!-- The field under validation must be an integer. -->
검증 대상 필드는 정수여야 합니다.

> [!WARNING]
> 이 유효성 검사 규칙은 인풋이 진짜 '정수' 타입인지까지 확인하지는 않으며, PHP의 `FILTER_VALIDATE_INT` 규칙에서 허용하는 타입이면 모두 허용됩니다. 값을 진짜 숫자로 검증하려면 [the `numeric` validation rule](#rule-numeric)과 함께 사용해야 합니다.

<a name="rule-ip"></a>
<!-- #### ip -->
#### ip

<!-- The field under validation must be an IP address. -->
검증 대상 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
<!-- #### ipv4 -->
#### ipv4

<!-- The field under validation must be an IPv4 address. -->
검증 대상 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
<!-- #### ipv6 -->
#### ipv6

<!-- The field under validation must be an IPv6 address. -->
검증 대상 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
<!-- #### json -->
#### json

<!-- The field under validation must be a valid JSON string. -->
검증 대상 필드는 올바른 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
<!-- #### lt:_field_ -->
#### lt:_field_

<!-- The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_보다 작아야 합니다. 두 필드는 반드시 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size)와 동일한 기준을 적용받습니다.

<a name="rule-lte"></a>
<!-- #### lte:_field_ -->
#### lte:_field_

<!-- The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_보다 작거나 같아야 합니다. 두 필드는 반드시 동일 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-lowercase"></a>
<!-- #### lowercase -->
#### lowercase

<!-- The field under validation must be lowercase. -->
검증 대상 필드는 모두 소문자여야 합니다.

<a name="rule-mac"></a>
<!-- #### mac_address -->
#### mac_address

<!-- The field under validation must be a MAC address. -->
검증 대상 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
<!-- #### max:_value_ -->
#### max:_value_

<!-- The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 최대값(_value_) 이하이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 판단합니다.

<a name="rule-max-digits"></a>
<!-- #### max_digits:_value_ -->
#### max_digits:_value_

<!-- The integer under validation must have a maximum length of _value_. -->
검증 대상 정수(integer)의 자릿수 최대값이 _value_이어야 합니다.

<a name="rule-mimetypes"></a>
<!-- #### mimetypes:_text/plain_,... -->
#### mimetypes:_text/plain_,...

<!-- The file under validation must match one of the given MIME types: -->
검증 대상 파일은 지정된 MIME 타입 중 하나여야 합니다.

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

<!-- To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type. -->
업로드된 파일의 MIME 타입은 파일의 실제 내용을 읽어 추론하며, 클라이언트가 제공한 MIME 타입과는 다를 수 있습니다.

<a name="rule-mimes"></a>
<!-- #### mimes:_foo_,_bar_,... -->
#### mimes:_foo_,_bar_,...

<!-- The file under validation must have a MIME type corresponding to one of the listed extensions: -->
검증 대상 파일은 지정된 확장자에 해당하는 MIME 타입을 가져야 합니다.

```
'photo' => 'mimes:jpg,bmp,png'
```

<!-- Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
실제 지정하는 것은 확장자(예: jpg)이지만, 이 규칙은 파일의 내용을 읽어 MIME 타입을 판별해 검사합니다. 지원되는 전체 MIME 타입과 그에 해당하는 확장자 목록은 다음에서 확인할 수 있습니다.

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
<!-- #### MIME Types and Extensions -->
#### MIME Types and Extensions

<!-- This validation rule does not verify agreement between the MIME type and the extension the user assigned to the file. For example, the `mimes:png` validation rule would consider a file containing valid PNG content to be a valid PNG image, even if the file is named `photo.txt`. If you would like to validate the user-assigned extension of the file, you may use the [`extensions`](#rule-extensions) rule. -->
이 유효성 검사 규칙은 파일의 MIME 타입과 사용자가 지정한 확장자가 일치하는지까지 검사하지는 않습니다. 예를 들어, `mimes:png` 규칙은 내용이 올바른 PNG 형식이라면 파일명이 `photo.txt`이어도 PNG 이미지로 인정합니다. 파일의 확장자를 검증하고 싶다면 [`extensions`](#rule-extensions) 규칙을 이용할 수 있습니다.

<a name="rule-min"></a>
<!-- #### min:_value_ -->
#### min:_value_

<!-- The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 최소값(_value_) 이상이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일하게 적용됩니다.

<a name="rule-min-digits"></a>
<!-- #### min_digits:_value_ -->
#### min_digits:_value_

<!-- The integer under validation must have a minimum length of _value_. -->
검증 대상 정수(integer)의 자릿수 최소값이 _value_이어야 합니다.

<a name="rule-multiple-of"></a>
<!-- #### multiple_of:_value_ -->
#### multiple_of:_value_

<!-- The field under validation must be a multiple of _value_. -->
검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
<!-- #### missing -->
#### missing

<!-- The field under validation must not be present in the input data. -->
검증 대상 필드는 입력 데이터에 존재하지 않아야 합니다.

 <a name="rule-missing-if"></a>
<!-- #### missing_if:_anotherfield_,_value_,... -->
#### missing_if:_anotherfield_,_value_,...

<!--  The field under validation must not be present if the _anotherfield_ field is equal to any _value_. -->
 _anotherfield_ 필드가 _value_ 중 하나와 같으면, 검증 대상 필드는 존재해서는 안 됩니다.

 <a name="rule-missing-unless"></a>
<!-- #### missing_unless:_anotherfield_,_value_ -->
#### missing_unless:_anotherfield_,_value_

<!-- The field under validation must not be present unless the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ 필드가 _value_ 중 하나와 같지 않으면, 검증 대상 필드는 존재해서는 안 됩니다.

 <a name="rule-missing-with"></a>
<!-- #### missing_with:_foo_,_bar_,... -->
#### missing_with:_foo_,_bar_,...

<!--  The field under validation must not be present _only if_ any of the other specified fields are present. -->
 지정된 다른 필드 중 하나라도 존재할 때만, 검증 대상 필드는 존재해서는 안 됩니다.

 <a name="rule-missing-with-all"></a>
<!-- #### missing_with_all:_foo_,_bar_,... -->
#### missing_with_all:_foo_,_bar_,...

<!--  The field under validation must not be present _only if_ all of the other specified fields are present. -->
 지정된 다른 필드들이 모두 존재할 때만, 검증 대상 필드는 존재해서는 안 됩니다.

<a name="rule-not-in"></a>
<!-- #### not_in:_foo_,_bar_,... -->
#### not_in:_foo_,_bar_,...

<!-- The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule: -->
검증 대상 필드는 지정된 값 목록에 포함되어서는 안 됩니다. `Rule::notIn` 메서드를 사용하면 더 유연하게 규칙을 정의할 수 있습니다.

```
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a name="rule-not-regex"></a>

<!-- #### not_regex:_pattern_ -->
#### not_regex:_pattern_

<!-- The field under validation must not match the given regular expression. -->
검증 대상 필드는 지정된 정규 표현식과 **일치하지 않아야** 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`. -->
내부적으로 이 규칙은 PHP의 `preg_match` 함수를 사용합니다. 지정하는 정규식 패턴은 반드시 `preg_match`가 요구하는 형식(유효한 구분자 포함)을 따라야 합니다. 예를 들어, `'email' => 'not_regex:/^.+$/i'`와 같이 작성해야 합니다.

> [!WARNING]
> `regex` 또는 `not_regex` 패턴을 사용할 때, 특히 정규식에 `|` 문자가 포함된 경우에는 파이프(`|`) 구분자 대신 배열 형태로 유효성 검사 규칙을 지정해야 할 수 있습니다.

<a name="rule-nullable"></a>
<!-- #### nullable -->
#### nullable

<!-- The field under validation may be `null`. -->
검증 대상 필드의 값은 `null`일 수 있습니다.

<a name="rule-numeric"></a>
<!-- #### numeric -->
#### numeric

<!-- The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php). -->
검증 대상 필드 값은 [numeric](https://www.php.net/manual/en/function.is-numeric.php)여야 합니다.

<a name="rule-present"></a>
<!-- #### present -->
#### present

<!-- The field under validation must exist in the input data. -->
검증 대상 필드는 입력 데이터에 **존재**해야 합니다.

<a name="rule-present-if"></a>
<!-- #### present_if:_anotherfield_,_value_,... -->
#### present_if:_anotherfield_,_value_,...

<!-- The field under validation must be present if the _anotherfield_ field is equal to any _value_. -->
_다른 필드_가 지정한 _값_ 중 하나와 같을 때 검증 대상 필드는 반드시 포함되어야 합니다.

<a name="rule-present-unless"></a>
<!-- #### present_unless:_anotherfield_,_value_ -->
#### present_unless:_anotherfield_,_value_

<!-- The field under validation must be present unless the _anotherfield_ field is equal to any _value_. -->
_다른 필드_가 지정한 _값_ 중 하나와 같지 않을 때, 검증 대상 필드는 반드시 포함되어야 합니다.

<a name="rule-present-with"></a>
<!-- #### present_with:_foo_,_bar_,... -->
#### present_with:_foo_,_bar_,...

<!-- The field under validation must be present _only if_ any of the other specified fields are present. -->
다른 지정된 필드 중 **하나 이상**이 존재할 경우에만, 검증 대상 필드가 반드시 존재해야 합니다.

<a name="rule-present-with-all"></a>
<!-- #### present_with_all:_foo_,_bar_,... -->
#### present_with_all:_foo_,_bar_,...

<!-- The field under validation must be present _only if_ all of the other specified fields are present. -->
다른 지정된 필드 **모두가 존재할 때에만**, 검증 대상 필드가 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
<!-- #### prohibited -->
#### prohibited

<!-- The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
검증 대상 필드는 **존재하지 않거나 비어 있어야** 합니다. "비어 있음"의 기준은 다음 중 하나를 만족할 때입니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`일 때
- 값이 빈 문자열일 때
- 값이 빈 배열 또는 비어 있는 `Countable` 객체일 때
- 업로드된 파일이지만 경로(path)가 비어 있을 때

<!-- </div> -->
</div>

<a name="rule-prohibited-if"></a>
<!-- #### prohibited_if:_anotherfield_,_value_,... -->
#### prohibited_if:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
_다른 필드_가 지정한 _값_ 중 하나와 같을 때, 검증 대상 필드는 **존재하지 않거나 비어 있어야** 합니다. "비어 있음"의 기준은 다음 중 하나입니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`일 때
- 값이 빈 문자열일 때
- 값이 빈 배열 또는 비어 있는 `Countable` 객체일 때
- 업로드된 파일이지만 경로(path)가 비어 있을 때

<!-- </div> -->
</div>

<!-- If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited: -->
좀 더 복잡한 조건부 금지(prohibition) 로직이 필요하다면, `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 인자로 받으며, 클로저의 반환값이 `true` 또는 `false`면 해당 필드를 금지할지 여부를 나타냅니다:

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::prohibitedIf(fn () => $request->user()->is_admin),
]);
```

<a name="rule-prohibited-unless"></a>
<!-- #### prohibited_unless:_anotherfield_,_value_,... -->
#### prohibited_unless:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty unless the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
_다른 필드_가 지정한 _값_ 중 하나와 **같지 않을 때만**, 검증 대상 필드는 **존재하지 않거나 비어 있어야** 합니다. "비어 있음"의 기준은 다음 중 하나입니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`일 때
- 값이 빈 문자열일 때
- 값이 빈 배열 또는 비어 있는 `Countable` 객체일 때
- 업로드된 파일이지만 경로(path)가 비어 있을 때

<!-- </div> -->
</div>

<a name="rule-prohibits"></a>
<!-- #### prohibits:_anotherfield_,... -->
#### prohibits:_anotherfield_,...

<!-- If the field under validation is not missing or empty, all fields in _anotherfield_ must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
검증 대상 필드가 **존재하거나 비어 있지 않으면**, _anotherfield_에 지정된 모든 필드는 **존재하지 않거나 비어 있어야** 합니다. "비어 있음"의 기준은 아래와 같습니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`일 때
- 값이 빈 문자열일 때
- 값이 빈 배열 또는 비어 있는 `Countable` 객체일 때
- 업로드된 파일이지만 경로(path)가 비어 있을 때

<!-- </div> -->
</div>

<a name="rule-regex"></a>
<!-- #### regex:_pattern_ -->
#### regex:_pattern_

<!-- The field under validation must match the given regular expression. -->
검증 대상 필드는 지정된 정규 표현식과 **일치해야** 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`. -->
이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용하며, 패턴은 반드시 `preg_match`에서 요구하는 올바른 구분자가 포함된 형식이어야 합니다. 예를 들어: `'email' => 'regex:/^.+@.+$/i'`와 같이 지정해야 합니다.

> [!WARNING]
> `regex` 또는 `not_regex` 패턴을 사용할 때, 정규식에 `|` 문자가 포함되면 파이프(`|`) 대신 배열로 규칙을 지정해야 할 수 있습니다.

<a name="rule-required"></a>
<!-- #### required -->
#### required

<!-- The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria: -->
검증 대상 필드는 입력 데이터에 반드시 존재해야 하며, 비어 있지 않아야 합니다. 필드가 "비어 있음"의 기준은 다음과 같습니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.
-->
- 값이 `null`일 때
- 값이 빈 문자열일 때
- 값이 빈 배열 또는 비어 있는 `Countable` 객체일 때
- 업로드된 파일이 경로(path)를 가지지 않을 때

<!-- </div> -->
</div>

<a name="rule-required-if"></a>
<!-- #### required_if:_anotherfield_,_value_,... -->
#### required_if:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_. -->
_다른 필드_가 지정된 _값_ 중 하나와 같을 때, 검증 대상 필드는 **반드시 존재해야 하며 비어 있으면 안 됩니다**.

<!-- If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required: -->
`required_if` 규칙에 더 복잡한 조건을 적용하려면, `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 인자로 받습니다. 클로저의 반환값이 `true` 또는 `false`일 때 해당 필드가 필수인지 여부를 나타냅니다:

```
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
<!-- #### required_if_accepted:_anotherfield_,... -->
#### required_if_accepted:_anotherfield_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. -->
_다른 필드_가 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나의 값과 같을 때, 검증 대상 필드는 반드시 존재해야 하며 비어 있을 수 없습니다.

<a name="rule-required-unless"></a>
<!-- #### required_unless:_anotherfield_,_value_,... -->
#### required_unless:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data. -->
_다른 필드_가 지정된 _값_ 중 하나와 **같지 않을 때만** 검증 대상 필드는 반드시 존재해야 하며 비어 있으면 안 됩니다. 또한 _anotherfield_는 _value_가 `null`이 아닌 한 요청 데이터에 반드시 존재해야 합니다. 만약 _value_가 `null`(`required_unless:name,null`)이라면, 비교 대상 필드 값이 `null`이거나 요청 데이터에 해당 필드가 없을 경우에만 검증 대상 필드가 필수로 간주되지 않습니다.

<a name="rule-required-with"></a>
<!-- #### required_with:_foo_,_bar_,... -->
#### required_with:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty. -->
지정된 다른 필드 중 하나라도 값이 **있고 비어 있지 않으면**, 검증 대상 필드는 반드시 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-with-all"></a>
<!-- #### required_with_all:_foo_,_bar_,... -->
#### required_with_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty. -->
지정된 모든 다른 필드가 **존재하고 비어 있지 않을 때에만** 검증 대상 필드는 필수입니다.

<a name="rule-required-without"></a>
<!-- #### required_without:_foo_,_bar_,... -->
#### required_without:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present. -->
지정된 다른 필드 중 하나라도 **비어 있거나 존재하지 않을 때에만** 검증 대상 필드는 필수입니다.

<a name="rule-required-without-all"></a>
<!-- #### required_without_all:_foo_,_bar_,... -->
#### required_without_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present. -->
지정된 모든 다른 필드가 **비어 있거나 존재하지 않을 때에만** 검증 대상 필드는 필수입니다.

<a name="rule-required-array-keys"></a>
<!-- #### required_array_keys:_foo_,_bar_,... -->
#### required_array_keys:_foo_,_bar_,...

<!-- The field under validation must be an array and must contain at least the specified keys. -->
검증 대상 필드는 반드시 배열이어야 하며, 지정한 key(들)을 **모두 포함**해야 합니다.

<a name="rule-same"></a>
<!-- #### same:_field_ -->
#### same:_field_

<!-- The given _field_ must match the field under validation. -->
지정한 _field_의 값이 검증 대상 필드와 **같아야** 합니다.

<a name="rule-size"></a>
<!-- #### size:_value_ -->
#### size:_value_

<!-- The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples: -->
검증 대상 필드는 지정한 _value_와 **크기가 같아야** 합니다. 문자열 필드의 경우 _value_는 문자 수를 의미합니다. 숫자 필드의 경우 _value_는 특정 정수 값이어야 합니다(이 경우 `numeric` 또는 `integer` 규칙도 함께 적용되어야 합니다). 배열의 경우 _size_는 배열의 `count`를 의미합니다. 파일의 경우 _size_는 파일 크기(킬로바이트 단위)입니다. 예시를 살펴보겠습니다:

```
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
<!-- #### starts_with:_foo_,_bar_,... -->
#### starts_with:_foo_,_bar_,...

<!-- The field under validation must start with one of the given values. -->
검증 대상 필드는 지정한 값 중 **하나로 시작**해야 합니다.

<a name="rule-string"></a>
<!-- #### string -->
#### string

<!-- The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field. -->
검증 대상 필드는 **문자열(string)** 이어야 합니다. 만약 필드 값이 `null`도 허용하려면, 해당 필드에 `nullable` 규칙을 추가하세요.

<a name="rule-timezone"></a>
<!-- #### timezone -->
#### timezone

<!-- The field under validation must be a valid timezone identifier according to the `DateTimeZone::listIdentifiers` method. -->
검증 대상 필드는 `DateTimeZone::listIdentifiers` 메서드 기준의 **유효한 타임존 식별자**여야 합니다.

<!-- The arguments [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php) may also be provided to this validation rule: -->
또한, [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php)를 이 유효성 검사 규칙에 추가로 전달할 수 있습니다.

```
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
<!-- #### unique:_table_,_column_ -->
#### unique:_table_,_column_

<!-- The field under validation must not exist within the given database table. -->
검증 대상 필드 값은 지정된 데이터베이스 테이블에 **이미 존재하면 안 됩니다**.

<!-- **Specifying a Custom Table / Column Name:** -->
**커스텀 테이블/컬럼명 지정하기**

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블명을 직접 입력하는 대신, Eloquent 모델명을 지정해 해당 테이블명을 결정하도록 할 수 있습니다:

```
'email' => 'unique:App\Models\User,email_address'
```

<!-- The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used. -->
`column` 옵션을 사용해 검증하려는 컬럼명을 직접 지정할 수도 있습니다. `column` 옵션을 생략하면 검증 대상 필드명이 컬럼명으로 사용됩니다.

```
'email' => 'unique:users,email_address'
```

<!-- **Specifying a Custom Database Connection** -->
**커스텀 데이터베이스 연결 지정하기**

<!-- Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name: -->
가끔 Validator에서 쿼리를 실행할 때 원하는 데이터베이스 연결을 사용해야 할 때가 있습니다. 이럴 경우, 테이블명 앞에 연결명을 붙여서 지정할 수 있습니다.

```
'email' => 'unique:connection.users,email_address'
```

<!-- **Forcing a Unique Rule to Ignore a Given ID:** -->
**특정 ID를 무시하고 unique 검증하기**

<!-- Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question. -->
가끔 unique 유효성 검증을 하면서 특정 ID값은 **무시**하고 싶을 수도 있습니다. 예를 들어, '프로필 수정' 기능에서 현재 사용자의 이메일을 unique로 검증하되, 자기 자신은 해당 이메일을 가지고 있어도 에러가 발생하지 않게 하고 싶을 때 활용합니다.

<!-- To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules: -->
이를 위해서는, `Rule` 클래스를 사용하여 규칙을 메서드 체이닝 방식으로 정의합니다. 예시에서는 `|` 문자로 구분하는 대신 배열로 규칙을 지정합니다:

```
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
> **사용자가 직접 입력하는 값은 절대로 `ignore` 메서드에 전달해서는 안 됩니다.** 반드시 자동 증가 ID나 UUID 등 시스템에서 관리하는 고유값을 전달해야 하며, 그렇지 않으면 SQL 인젝션 공격에 취약해질 수 있습니다.

<!-- Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model: -->
`ignore` 메서드에 모델의 키 값 대신 **모델 인스턴스 전체**를 전달할 수도 있으며, 이 경우 Laravel이 자동으로 키 값을 추출합니다.

```
Rule::unique('users')->ignore($user)
```

<!-- If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method: -->
테이블에서 기본 키(primary key) 컬럼명이 `id`가 아니라면, `ignore` 메서드를 호출할 때 두 번째 인자로 컬럼명을 지정할 수 있습니다:

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

<!-- By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method: -->
기본적으로 `unique` 규칙은 검증하는 필드명과 동일한 컬럼의 유일성을 검사합니다. 하지만 `unique` 메서드의 두 번째 인자로 컬럼명을 지정해 다르게 설정할 수도 있습니다:

```
Rule::unique('users', 'email_address')->ignore($user->id)
```

<!-- **Adding Additional Where Clauses:** -->
**추가 where 조건 지정하기**

<!-- You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`: -->
쿼리 조건을 추가로 지정하려면 `where` 메서드로 쿼리를 수정할 수도 있습니다. 예를 들어, `account_id`가 `1`인 레코드만 검사하도록 범위를 좁힐 수 있습니다:

```
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

<a name="rule-uppercase"></a>
<!-- #### uppercase -->
#### uppercase

<!-- The field under validation must be uppercase. -->
검증 대상 필드는 **영문 대문자**여야 합니다.

<a name="rule-url"></a>
<!-- #### url -->
#### url

<!-- The field under validation must be a valid URL. -->
검증 대상 필드는 **유효한 URL**이어야 합니다.

<!-- If you would like to specify the URL protocols that should be considered valid, you may pass the protocols as validation rule parameters: -->
특정 URL 프로토콜만 허용하려면 유효성 검사 규칙의 파라미터로 프로토콜을 지정할 수 있습니다:

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
<!-- #### ulid -->
#### ulid

<!-- The field under validation must be a valid [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID). -->
검증 대상 필드는 [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) 형식의 **유효한 ULID**여야 합니다.

<a name="rule-uuid"></a>
<!-- #### uuid -->
#### uuid

<!-- The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID). -->
검증 대상 필드는 RFC 4122(버전 1, 3, 4, 5) 기준의 **유효한 UUID**여야 합니다.

<a name="conditionally-adding-rules"></a>
<!-- ## Conditionally Adding Rules -->
## Conditionally Adding Rules

<a name="skipping-validation-when-fields-have-certain-values"></a>
<!-- #### Skipping Validation When Fields Have Certain Values -->
#### Skipping Validation When Fields Have Certain Values

<!-- You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`: -->
경우에 따라, 특정 필드가 어떤 값을 가질 때 다른 필드의 유효성 검사를 **하지** 않기를 원할 수 있습니다. 이럴 때는 `exclude_if` 유효성 검사 규칙을 사용할 수 있습니다. 아래 예시처럼 `has_appointment`가 `false`일 때는 `appointment_date`와 `doctor_name` 필드 검증이 생략됩니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

<!-- Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value: -->
반대로, 특정 필드가 지정한 값일 때만 검증하고 싶으면 `exclude_unless` 규칙을 사용할 수 있습니다:

```
$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
    'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
]);
```

<a name="validating-when-present"></a>
<!-- #### Validating When Present -->
#### Validating When Present

<!-- In some situations, you may wish to run validation checks against a field **only** if that field is present in the data being validated. To quickly accomplish this, add the `sometimes` rule to your rule list: -->
특정 상황에서는, 어떤 필드가 입력 데이터에 **존재할 때만** 해당 필드의 유효성 검사를 수행하고 싶을 수 있습니다. 이럴 때는 규칙 목록에 `sometimes` 규칙을 추가하면 됩니다:

```
$v = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

<!-- In the example above, the `email` field will only be validated if it is present in the `$data` array. -->
위 예시에서 `$data` 배열에 `email` 필드가 존재할 때에만, 해당 필드에 대해 유효성 검사가 실행됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있어도 되는 필드를 검증하고 싶다면, [this note on optional fields](#a-note-on-optional-fields)를 참고하세요.

<a name="complex-conditional-validation"></a>
<!-- #### Complex Conditional Validation -->
#### Complex Conditional Validation

<!-- Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change: -->
특정 조건에 따라 규칙을 동적으로 추가해야 할 때가 종종 있습니다. 예를 들어, 필드 값이 100 이상일 때만 추가 설명을 요구하거나, 또 다른 필드가 존재할 때에만 두 필드가 특정 값을 가져야 하는 경우 등입니다. `Validator`를 사용하면 이런 복잡한 조건도 손쉽게 처리할 수 있습니다.

먼저, 변하지 않는 **정적(Static) 규칙**으로 Validator 인스턴스를 만듭니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);
```

<!-- Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance. -->
만약 웹 애플리케이션이 게임 수집가를 위한 것이라면, 만약 유저가 100개 이상의 게임을 소유하고 있다면, 소유 이유(reason)를 설명하도록 요구하는 상황을 생각해볼 수 있습니다. 이럴 땐, `Validator` 인스턴스의 `sometimes` 메서드를 활용하여 조건부로 규칙을 추가할 수 있습니다.

```
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

<!-- The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once: -->
`sometimes` 메서드의 첫 번째 인자는 조건부 검증 대상 필드명, 두 번째 인자는 적용할 규칙 목록, 세 번째 인자는 boolean 값을 반환하는 클로저입니다. 클로저가 `true`를 반환하면 해당 규칙이 적용됩니다. 이 방식으로 여러 필드에 조건부 유효성 검증을 한 번에 추가할 수도 있습니다:

```
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent` 인스턴스이며, 검증 중인 입력값과 파일을 참조할 때 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
<!-- #### Complex Conditional Array Validation -->
#### Complex Conditional Array Validation

<!-- Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated: -->
중첩 배열 내에서, 인덱스를 미리 모를 때 다른 필드의 값에 따라 검증 규칙을 적용하고 싶을 수 있습니다. 이럴 때, 클로저의 두 번째 인자로 현재 반복 중인 배열 아이템을 받을 수 있습니다:

```
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

<!-- Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string. -->
여기서 `$item` 역시 `$input`과 마찬가지로 `Illuminate\Support\Fluent`의 인스턴스(입력 데이터가 배열일 경우)이며, 아니라면 단순 문자열입니다.

<a name="validating-arrays"></a>
<!-- ## Validating Arrays -->
## Validating Arrays

<!-- As discussed in the [`array` validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail: -->
[`array` validation rule documentation](#rule-array)에서 설명한 것처럼, `array` 규칙에는 허용할 배열 키 목록을 지정할 수 있습니다. 배열에 다른 키가 더 있으면 유효성 검사에 실패합니다.

```
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

<!-- In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules. -->
일반적으로, 배열 내에 어떤 키들이 존재할 수 있는지 **항상 명시적으로** 지정하는 것이 좋습니다. 그렇지 않으면, Validator의 `validate`, `validated` 메서드는 중첩 배열 검증 규칙에서 검증받지 않은 키까지 포함해서 모든 배열 키의 데이터를 반환합니다.

<a name="validating-nested-array-input"></a>
<!-- ### Validating Nested Array Input -->
### Validating Nested Array Input

<!-- Validating nested array based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so: -->
폼 데이터에 중첩 배열이 있는 필드 유효성 검사도 어렵지 않습니다. "점 표기법(dot notation)"을 사용하면 배열 내부의 필드를 쉽게 검증할 수 있습니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]`이 있다면 다음과 같이 유효성 검사를 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

<!-- You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following: -->
배열의 각 요소에 대해 유효성 검사를 적용하는 것도 가능합니다. 예를 들어, 배열 입력 필드 안의 각 이메일이 유일한지 검사하려면 다음과 같이 작성합니다:

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

<!-- Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array based fields: -->
또한 [custom validation messages in your language files](#custom-messages-for-specific-attributes)를 정의할 때 `*`를 사용할 수 있어, 배열 기반 필드에 단일 메시지 설정도 매우 쉽습니다:

```
'custom' => [
    'person.*.email' => [
        'unique' => 'Each person must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
<!-- #### Accessing Nested Array Data -->
#### Accessing Nested Array Data

<!-- Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element: -->
검증 규칙을 지정하면서 특정 중첩 배열 요소의 값을 참조해야 할 때가 있습니다. 이럴 때는 `Rule::forEach` 메서드를 활용할 수 있습니다. 이 `forEach` 메서드는 검증 중인 배열 필드의 각 요소에 대해 클로저를 호출하며, 해당 요소의 값과 완전히 확장된 속성명을 파라미터로 전달합니다. 클로저는 각 요소에 적용할 규칙들의 배열을 반환해야 합니다:

```
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
<!-- ### Error Message Indexes and Positions -->
### Error Message Indexes and Positions

<!-- When validating arrays, you may want to reference the index or position of a particular item that failed validation within the error message displayed by your application. To accomplish this, you may include the `:index` (starts from `0`) and `:position` (starts from `1`) placeholders within your [custom validation message](#manual-customizing-the-error-messages): -->
배열을 검증할 때는 유효성 검증에 실패한 항목의 인덱스나 위치 정보를 에러 메시지에서 참고하고 싶을 수 있습니다. 이런 경우, [custom validation message](#manual-customizing-the-error-messages) 내에서 `:index`(`0`부터 시작), `:position`(`1`부터 시작) 플레이스홀더를 사용할 수 있습니다:

```
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

<!-- Given the example above, validation will fail and the user will be presented with the following error of _"Please describe photo #2."_ -->
위 예시의 경우, 유효성 검사가 실패하면 사용자는 _"Please describe photo #2."_와 같은 에러 메시지를 보게 됩니다.

<!-- If necessary, you may reference more deeply nested indexes and positions via `second-index`, `second-position`, `third-index`, `third-position`, etc. -->
필요하다면, 더 깊이 중첩된 인덱스 및 위치도 `second-index`, `second-position`, `third-index`, `third-position` 등으로 참조할 수 있습니다.

```
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>

<!-- ## Validating Files -->
## Validating Files

<!-- Laravel provides a variety of validation rules that may be used to validate uploaded files, such as `mimes`, `image`, `min`, and `max`. While you are free to specify these rules individually when validating files, Laravel also offers a fluent file validation rule builder that you may find convenient: -->
Laravel은 업로드된 파일을 검증할 수 있도록 `mimes`, `image`, `min`, `max` 등 다양한 유효성 검사 규칙을 제공합니다. 각각의 규칙을 개별적으로 지정하여 파일을 검증할 수도 있지만, Laravel이 제공하는 유창한(fluid) 파일 유효성 검증 규칙 빌더를 활용하면 더욱 편리합니다:

```
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

<!-- If your application accepts images uploaded by your users, you may use the `File` rule's `image` constructor method to indicate that the uploaded file should be an image. In addition, the `dimensions` rule may be used to limit the dimensions of the image: -->
애플리케이션에서 사용자가 이미지를 업로드하도록 허용한다면, `File` 규칙의 `image` 생성자 메서드를 사용하여 업로드된 파일이 이미지임을 지정할 수 있습니다. 또한 `dimensions` 규칙을 사용하면 이미지의 크기를 제한할 수 있습니다.

```
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
> 이미지 크기(dimensions) 검증에 대한 추가 정보는 [dimension rule documentation](#rule-dimensions)에서 확인할 수 있습니다.

<a name="validating-files-file-sizes"></a>
<!-- #### File Sizes -->
#### File Sizes

<!-- For convenience, minimum and maximum file sizes may be specified as a string with a suffix indicating the file size units. The `kb`, `mb`, `gb`, and `tb` suffixes are supported: -->
편의를 위해, 최소 및 최대 파일 크기는 파일 크기 단위를 나타내는 접미사를 포함한 문자열로 지정할 수 있습니다. `kb`, `mb`, `gb`, `tb` 접미사를 지원합니다:

```php
File::image()
    ->min('1kb')
    ->max('10mb')
```

<a name="validating-files-file-types"></a>
<!-- #### File Types -->
#### File Types

<!-- Even though you only need to specify the extensions when invoking the `types` method, this method actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
`types` 메서드를 사용할 때는 확장자만 지정하지만, 내부적으로는 실제로 파일의 내용을 읽어서 MIME 타입을 추정한 뒤 해당 MIME 타입을 검사합니다. MIME 타입과 이와 대응되는 확장자 전체 목록은 아래 링크에서 확인할 수 있습니다.

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-passwords"></a>
<!-- ## Validating Passwords -->
## Validating Passwords

<!-- To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object: -->
비밀번호가 적절한 수준의 복잡성을 갖추도록 보장하려면, Laravel의 `Password` 규칙 객체를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

<!-- The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing: -->
`Password` 규칙 객체를 사용하면 비밀번호에 최소 하나 이상의 영문자, 숫자, 특수문자 또는 대·소문자 혼합과 같은 복잡성 요구사항을 손쉽게 지정할 수 있습니다.

```
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

<!-- In addition, you may ensure that a password has not been compromised in a public password data breach leak using the `uncompromised` method: -->
또한, `uncompromised` 메서드를 사용하면 비밀번호가 공개된 비밀번호 데이터 유출에 포함된 적이 있는지 확인할 수 있습니다.

```
Password::min(8)->uncompromised()
```

<!-- Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security. -->
내부적으로 `Password` 규칙 객체는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 서비스를 활용하며, [haveibeenpwned.com](https://haveibeenpwned.com) 모델을 통해 사용자의 프라이버시와 보안을 해치지 않고 유출 여부를 판단합니다.

<!-- By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method: -->
기본적으로 비밀번호가 데이터 유출에 한 번이라도 등장하면 유출된 것으로 간주합니다. 이 임계값(threshold)은 `uncompromised` 메서드의 첫 번째 인수를 통해 지정할 수 있습니다.

```
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

<!-- Of course, you may chain all the methods in the examples above: -->
물론, 위에서 소개한 모든 메서드를 체이닝하여 동시에 사용할 수도 있습니다.

```
Password::min(8)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<a name="defining-default-password-rules"></a>
<!-- #### Defining Default Password Rules -->
#### Defining Default Password Rules

<!-- You may find it convenient to specify the default validation rules for passwords in a single location of your application. You can easily accomplish this using the `Password::defaults` method, which accepts a closure. The closure given to the `defaults` method should return the default configuration of the Password rule. Typically, the `defaults` rule should be called within the `boot` method of one of your application's service providers: -->
비밀번호에 대한 기본 유효성 검사 규칙을 애플리케이션의 한 곳에서 지정해두면 편리합니다. 이를 위해 `Password::defaults` 메서드(클로저를 인수로 받음)를 사용할 수 있습니다. 이 `defaults` 메서드에 전달하는 클로저는 Password 규칙의 기본 구성을 반환해야 합니다. 일반적으로 `defaults` 규칙은 애플리케이션 서비스 프로바이더의 `boot` 메서드 내부에서 호출하면 좋습니다.

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

<!-- Then, when you would like to apply the default rules to a particular password undergoing validation, you may invoke the `defaults` method with no arguments: -->
이후 특정 비밀번호가 검증될 때 기본 규칙을 적용하고 싶다면, 인자 없이 `defaults` 메서드를 호출하면 됩니다.

```
'password' => ['required', Password::defaults()],
```

<!-- Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this: -->
때로는 기본 비밀번호 유효성 검증 규칙에 추가 규칙을 연결하고 싶을 수 있습니다. 이 경우 `rules` 메서드를 사용하면 됩니다.

```
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
<!-- ## Custom Validation Rules -->
## Custom Validation Rules

<a name="using-rule-objects"></a>
<!-- ### Using Rule Objects -->
### Using Rule Objects

<!-- Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using rule objects. To generate a new rule object, you may use the `make:rule` Artisan command. Let's use this command to generate a rule that verifies a string is uppercase. Laravel will place the new rule in the `app/Rules` directory. If this directory does not exist, Laravel will create it when you execute the Artisan command to create your rule: -->
Laravel에는 유용한 유효성 검증 규칙이 다양하게 포함되어 있지만, 직접 정의한 규칙이 필요할 때도 있습니다. 커스텀 유효성 검증 규칙을 등록하는 한 가지 방법은 규칙 객체(rule object)를 사용하는 것입니다. 새 규칙 객체를 생성하려면 `make:rule` 아티즌 명령어를 사용할 수 있습니다. 예를 들어, 입력 문자열이 모두 대문자인지 확인하는 규칙을 아래와 같이 생성할 수 있습니다. Laravel은 생성된 규칙을 `app/Rules` 디렉터리에 위치시키며, 이 디렉터리가 없다면 명령어 실행 시 자동으로 생성해줍니다.

```shell
php artisan make:rule Uppercase
```

<!-- Once the rule has been created, we are ready to define its behavior. A rule object contains a single method: `validate`. This method receives the attribute name, its value, and a callback that should be invoked on failure with the validation error message: -->
규칙을 생성했다면, 이제 동작을 정의할 차례입니다. 규칙 객체는 하나의 메서드(`validate`)를 가집니다. 이 메서드는 속성명, 값, 실패할 경우 호출해야 할 콜백(검증 오류 메시지 전달용)을 인수로 받습니다.

```
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

<!-- Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules: -->
규칙 정의가 끝나면, 유효성 검사 시 다른 규칙들과 함께 규칙 객체의 인스턴스를 전달하여 적용할 수 있습니다.

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

<!-- #### Translating Validation Messages -->
#### Translating Validation Messages

<!-- Instead of providing a literal error message to the `$fail` closure, you may also provide a [translation string key](/docs/10.x/localization) and instruct Laravel to translate the error message: -->
`$fail` 콜백에 오류 메시지를 직접 전달하는 대신, [translation string key](/docs/10.x/localization)를 지정하여 Laravel이 해당 메시지를 번역하도록 할 수도 있습니다.

```
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

<!-- If necessary, you may provide placeholder replacements and the preferred language as the first and second arguments to the `translate` method: -->
필요하다면 `translate` 메서드에 플레이스홀더 치환값과 원하는 언어를 첫 번째, 두 번째 인수로 전달할 수 있습니다.

```
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr')
```

<!-- #### Accessing Additional Data -->
#### Accessing Additional Data

<!-- If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation: -->
커스텀 유효성 검증 규칙 클래스에서 현재 검증 중인 모든 데이터를 참조해야 할 경우, 클래스가 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하게 하면 됩니다. 이 인터페이스를 구현할 때는 `setData` 메서드를 반드시 정의해야 하며, 해당 메서드는 Laravel이 유효성 검사 시작 전에 자동으로 호출하면서 모든 검증 데이터를 전달해줍니다.

```
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

<!-- Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface: -->
또는, 유효성 검증을 실제로 수행하는 밸리데이터 인스턴스에 접근해야 하는 경우 `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

```
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
<!-- ### Using Closures -->
### Using Closures

<!-- If you only need the functionality of a custom rule once throughout your application, you may use a closure instead of a rule object. The closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails: -->
특정 커스텀 규칙이 애플리케이션 내에서 한 번만 필요하다면, 규칙 객체 대신 클로저(익명 함수)를 사용할 수 있습니다. 이 클로저는 속성명, 값, 검증 실패 시 호출할 `$fail` 콜백을 인수로 전달받습니다.

```
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
<!-- ### Implicit Rules -->
### Implicit Rules

<!-- By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the [`unique`](#rule-unique) rule will not be run against an empty string: -->
기본적으로, 유효성 검사가 수행될 때 해당 속성이 존재하지 않거나 빈 문자열인 경우에는 기본 규칙과 커스텀 규칙을 포함한 일반 유효성 규칙이 실행되지 않습니다. 예를 들어, [`unique`](#rule-unique) 규칙은 빈 문자열에 대해 실행되지 않습니다.

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

<!-- For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To quickly generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option: -->
속성이 비어 있더라도 커스텀 규칙이 실행되기를 바란다면, 해당 규칙이 암묵적으로 해당 속성이 required임을 내포해야 합니다. 이 때는 `make:rule` 아티즌 명령어에 `--implicit` 옵션을 추가하여 암묵적 규칙 객체를 빠르게 생성할 수 있습니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙이란, 단순히 해당 속성이 required임을 _내포_ 한다는 뜻입니다. 실제로 속성 누락 또는 빈 값에 대해 유효성 검사를 실패 처리할지는 여러분이 규칙 내에서 직접 정의해야 합니다.
