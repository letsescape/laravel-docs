<!-- # Validation -->
# Validation

- [Introduction](#introduction)
- [Validation Quickstart](#validation-quickstart)
    - [Defining The Routes](#quick-defining-the-routes)
    - [Creating The Controller](#quick-creating-the-controller)
    - [Writing The Validation Logic](#quick-writing-the-validation-logic)
    - [Displaying The Validation Errors](#quick-displaying-the-validation-errors)
    - [Repopulating Forms](#repopulating-forms)
    - [A Note On Optional Fields](#a-note-on-optional-fields)
    - [Validation Error Response Format](#validation-error-response-format)
- [Form Request Validation](#form-request-validation)
    - [Creating Form Requests](#creating-form-requests)
    - [Authorizing Form Requests](#authorizing-form-requests)
    - [Customizing The Error Messages](#customizing-the-error-messages)
    - [Preparing Input For Validation](#preparing-input-for-validation)
- [Manually Creating Validators](#manually-creating-validators)
    - [Automatic Redirection](#automatic-redirection)
    - [Named Error Bags](#named-error-bags)
    - [Customizing The Error Messages](#manual-customizing-the-error-messages)
    - [After Validation Hook](#after-validation-hook)
- [Working With Validated Input](#working-with-validated-input)
- [Working With Error Messages](#working-with-error-messages)
    - [Specifying Custom Messages In Language Files](#specifying-custom-messages-in-language-files)
    - [Specifying Attributes In Language Files](#specifying-attribute-in-language-files)
    - [Specifying Values In Language Files](#specifying-values-in-language-files)
- [Available Validation Rules](#available-validation-rules)
- [Conditionally Adding Rules](#conditionally-adding-rules)
- [Validating Arrays](#validating-arrays)
    - [Validating Nested Array Input](#validating-nested-array-input)
    - [Error Message Indexes & Positions](#error-message-indexes-and-positions)
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
Laravel은 애플리케이션으로 들어오는 데이터를 검증하는 다양한 방법을 제공합니다. 가장 일반적으로는, 모든 HTTP 요청 객체에서 사용할 수 있는 `validate` 메서드를 활용하게 됩니다. 이 밖에도 여러 유효성 검증 방식을 다루고 있으니 함께 살펴보겠습니다.

<!-- Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features. -->
Laravel은 매우 다양한 편리한 유효성 검증 규칙을 내장하고 있습니다. 예를 들어, 특정 데이터베이스 테이블에서 값의 중복 여부까지 검증할 수 있습니다. 본 문서를 통해 각각의 유효성 검증 규칙과 Laravel이 제공하는 모든 유효성 검증 기능을 상세히 익혀보시기 바랍니다.

<a name="validation-quickstart"></a>
<!-- ## Validation Quickstart -->
## Validation Quickstart

<!-- To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel: -->
Laravel의 강력한 유효성 검증 기능을 배우기 위해, 실제 폼을 검증하고 오류 메시지를 사용자에게 표시하는 완성 예제를 먼저 살펴보겠습니다. 이 하이레벨 개요를 읽으며 요청 데이터를 어떻게 검증하고, 결과를 처리하는지 전체적인 흐름을 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
<!-- ### Defining The Routes -->
### Defining The Routes

<!-- First, let's assume we have the following routes defined in our `routes/web.php` file: -->
먼저, `routes/web.php` 파일에 다음과 같은 라우트를 정의했다고 가정하겠습니다.

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

<!-- The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database. -->
여기서 `GET` 라우트는 사용자가 새 블로그 포스트를 작성할 수 있는 폼을 보여주고, `POST` 라우트는 새로운 블로그 포스트를 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
<!-- ### Creating The Controller -->
### Creating The Controller

<!-- Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now: -->
다음으로, 이 라우트로 들어오는 요청을 처리할 간단한 컨트롤러를 살펴보겠습니다. 우선 `store` 메서드는 비워둡니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     *
     * @return \Illuminate\View\View
     */
    public function create()
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // Validate and store the blog post...
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
<!-- ### Writing The Validation Logic -->
### Writing The Validation Logic

<!-- Now we are ready to fill in our `store` method with the logic to validate the new blog post. To do this, we will use the `validate` method provided by the `Illuminate\Http\Request` object. If the validation rules pass, your code will keep executing normally; however, if validation fails, an `Illuminate\Validation\ValidationException` exception will be thrown and the proper error response will automatically be sent back to the user. -->
이제, 새로운 블로그 포스트를 검증하는 로직을 `store` 메서드에 추가해봅니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검증에 성공하면 코드가 정상적으로 계속 실행됩니다. 그러나 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하며, 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

<!-- If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a [JSON response containing the validation error messages](#validation-error-response-format) will be returned. -->
전통적인 HTTP 요청에서 검증에 실패하면 이전 URL로 자동으로 리디렉션됩니다. 만약 들어오는 요청이 XHR(비동기 JavaScript) 요청이라면, [JSON response containing the validation error messages](#validation-error-response-format)이 반환됩니다.

<!-- To get a better understanding of the `validate` method, let's jump back into the `store` method: -->
`validate` 메서드가 어떻게 동작하는지 좀 더 자세히 알아보기 위해, 다시 `store` 메서드로 돌아가 보겠습니다.

```
/**
 * Store a new blog post.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ]);

    // The blog post is valid...
}
```

<!-- As you can see, the validation rules are passed into the `validate` method. Don't worry - all available validation rules are [documented](#available-validation-rules). Again, if the validation fails, the proper response will automatically be generated. If the validation passes, our controller will continue executing normally. -->
보시다시피, 유효성 검증 규칙은 `validate` 메서드의 인수로 전달됩니다. 걱정하지 마세요. 사용 가능한 유효성 검증 규칙 목록은 [documented](#available-validation-rules)에서 확인할 수 있습니다. 다시 한 번, 검증에 실패하면 Laravel이 자동으로 적절한 응답을 생성합니다. 검증에 성공하면 컨트롤러의 다음 코드가 정상적으로 실행됩니다.

<!-- Alternatively, validation rules may be specified as arrays of rules instead of a single `|` delimited string: -->
또한, 단일 `|`로 구분된 문자열 대신 유효성 검증 규칙을 배열로 지정할 수도 있습니다.

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<!-- In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a [named error bag](#named-error-bags): -->
또한, `validateWithBag` 메서드를 사용하면 요청을 검증하고, 오류 메시지를 [named error bag](#named-error-bags)으로 저장할 수 있습니다.

```
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
<!-- #### Stopping On First Validation Failure -->
#### Stopping On First Validation Failure

<!-- Sometimes you may wish to stop running validation rules on an attribute after the first validation failure. To do so, assign the `bail` rule to the attribute: -->
때로는 특정 속성에 대해 유효성 검증을 하다가 첫 번째 실패가 발생했을 때 이후 규칙을 실행하지 않고 검증을 멈추고 싶을 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가하면 됩니다.

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

<!-- In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned. -->
이 예시에서, 만약 `title` 속성에 대한 `unique` 규칙이 실패하면, `max` 규칙은 검증하지 않습니다. 규칙은 정의한 순서대로 차례차례 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
<!-- #### A Note On Nested Attributes -->
#### A Note On Nested Attributes

<!-- If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax: -->
들어오는 HTTP 요청에 "중첩된" 필드 데이터가 있을 경우, 유효성 검증 규칙에서 "dot" 표기법을 사용해 해당 필드를 지정할 수 있습니다.

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

<!-- On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash: -->
반대로, 필드명에 실제로 마침표( . )가 들어간 경우에는 백슬래시( \ )로 이스케이프 처리하여 "dot" 표기법이 적용되지 않도록 할 수 있습니다.

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
<!-- ### Displaying The Validation Errors -->
### Displaying The Validation Errors

<!-- So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/9.x/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/9.x/session#flash-data). -->
들어오는 요청 필드가 정해진 검증 규칙을 통과하지 못할 경우는 어떻게 될까요? 앞서 언급했듯이, Laravel은 자동으로 사용자를 이전 위치로 리디렉션합니다. 또한 모든 유효성 검증 오류와 [request input](/docs/9.x/requests#retrieving-old-input)이 [flashed to the session](/docs/9.x/session#flash-data).

<!-- An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages). -->
`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어는 모든 뷰에 `$errors` 변수를 공유해 줍니다. 이 미들웨어는 기본적으로 `web` 미들웨어 그룹에 포함되어 있습니다. 이 덕분에 뷰에서는 `$errors` 변수를 항상 사용할 수 있고, `$errors` 변수가 정의되어 있다고 가정하고 안전하게 사용할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 방법에 대해서는 [check out its documentation](#working-with-error-messages)를 참고하세요.

<!-- So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view: -->
예를 들어, 검증에 실패하면 사용자는 컨트롤러의 `create` 메서드로 리디렉션되며, 뷰에서 다음과 같이 오류 메시지를 보여줄 수 있습니다.

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
<!-- #### Customizing The Error Messages -->
#### Customizing The Error Messages

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. Within this file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
Laravel이 제공하는 기본 유효성 검증 규칙 각각에 대한 오류 메시지는 애플리케이션의 `lang/en/validation.php` 파일에 위치합니다. 이 파일에서 각 유효성 검증 규칙에 대해 번역 가능한 텍스트가 정의되어 있습니다. 필요에 따라 이 메시지들을 자유롭게 수정하거나 변경할 수 있습니다.

<!-- In addition, you may copy this file to another translation language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/9.x/localization). -->
또한, 이 파일을 다른 언어 디렉터리로 복사하여 애플리케이션 언어에 맞게 메시지를 번역할 수도 있습니다. Laravel의 다국어 지원(Localization)에 대해서는 [localization documentation](/docs/9.x/localization)를 참고하시기 바랍니다.

<a name="quick-xhr-requests-and-validation"></a>
<!-- #### XHR Requests & Validation -->
#### XHR Requests & Validation

<!-- In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a [JSON response containing all of the validation errors](#validation-error-response-format). This JSON response will be sent with a 422 HTTP status code. -->
앞서 예제에서는 전통적인 폼을 통해 데이터를 애플리케이션으로 전송했습니다. 하지만 실제로는 많은 애플리케이션이 자바스크립트 기반의 프런트엔드에서 XHR(비동기 HTTP) 요청을 발송합니다. XHR 요청 시 `validate` 메서드를 사용하면, Laravel은 리디렉션 응답을 생성하지 않습니다. 대신, [JSON response containing all of the validation errors](#validation-error-response-format)을 반환합니다. 이 JSON 응답의 HTTP 상태 코드는 422입니다.

<a name="the-at-error-directive"></a>
<!-- #### The `@error` Directive -->
#### The `@error` Directive

<!-- You may use the `@error` [Blade](/docs/9.x/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
Blade 템플릿에서 특정 속성에 대한 유효성 오류 메시지가 있는지 빠르게 확인하려면, `@error` [Blade](/docs/9.x/blade) 디렉티브를 사용할 수 있습니다. `@error` 블록 내부에서는 `$message` 변수를 출력하여 해당 속성의 오류 메시지를 보여줄 수 있습니다.

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
[named error bags](#named-error-bags)를 사용하는 경우, `@error` 디렉티브의 두 번째 인수로 에러백 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
<!-- ### Repopulating Forms -->
### Repopulating Forms

<!-- When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/9.x/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit. -->
유효성 검증 오류로 인해 Laravel이 리디렉션 응답을 생성하면, 프레임워크는 해당 요청의 모든 입력값을 자동으로 [flash all of the request's input to the session](/docs/9.x/session#flash-data)합니다. 이렇게 하면 다음 요청에서 이전 입력값을 쉽게 가져와, 사용자가 시도했던 폼을 다시 채울 수 있습니다.

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/9.x/session): -->
직전 요청에서 플래시된 입력 데이터를 가져오려면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하세요. 이 `old` 메서드는 [session](/docs/9.x/session)에 저장된 이전 입력값을 불러옵니다.

```
$title = $request->old('title');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/9.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel은 전역 `old` 헬퍼 함수도 제공합니다. [Blade template](/docs/9.x/blade)에서 이전 입력값을 표시할 때는 `old` 헬퍼를 사용하는 것이 더 편리합니다. 해당 필드에 이전 입력값이 없으면 `null`을 반환합니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
<!-- ### A Note On Optional Fields -->
### A Note On Optional Fields

<!-- By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware are listed in the stack by the `App\Http\Kernel` class. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example: -->
기본적으로 Laravel은 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 애플리케이션의 전역 미들웨어 스택에 포함시킵니다. 이 미들웨어들은 `App\Http\Kernel` 클래스의 미들웨어 스택에 정의되어 있습니다. 이로 인해, 선택 입력값이 null이 될 수 있다는 점에 유의해야 하며, 이런 필드는 검증 규칙에 `nullable` 키워드를 반드시 추가해야 합니다. 그렇지 않으면, 검증기는 `null` 값을 올바르지 않은 값으로 처리합니다. 예를 들어 다음과 같습니다.

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

<!-- In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date. -->
위 예시에서 `publish_at` 필드는 `null` 값이거나, 올바른 날짜 형식이어야 합니다. 만약 `nullable` 제한자를 추가하지 않으면, 검증기는 `null` 값을 유효한 날짜로 간주하지 않습니다.

<a name="validation-error-response-format"></a>
<!-- ### Validation Error Response Format -->
### Validation Error Response Format

<!-- When your application throws a `Illuminate\Validation\ValidationException` exception and the incoming HTTP request is expecting a JSON response, Laravel will automatically format the error messages for you and return a `422 Unprocessable Entity` HTTP response. -->
애플리케이션이 `Illuminate\Validation\ValidationException` 예외를 발생시키고, 들어온 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 자동으로 오류 메시지를 포맷하여 `422 Unprocessable Entity` HTTP 응답으로 반환합니다.

<!-- Below, you can review an example of the JSON response format for validation errors. Note that nested error keys are flattened into "dot" notation format: -->
아래는 유효성 검증 실패 시 반환되는 JSON 응답의 예시입니다. 중첩된 오류 키는 모두 "dot" 표기법으로 평탄화됩니다.

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
보다 복잡한 유효성 검증 시나리오에서는 "폼 리퀘스트(Form Request)"라는 커스텀 요청 클래스를 생성하는 것이 좋습니다. 폼 리퀘스트는 자체적인 검증 및 인가 로직을 캡슐화하는 사용자 정의 요청 클래스입니다. 폼 리퀘스트 클래스를 생성하려면 `make:request` 아티즌 명령어를 사용하세요.

```shell
php artisan make:request StorePostRequest
```

<!-- The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`. -->
생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 해당 디렉터리가 없다면, `make:request` 명령어를 실행할 때 자동으로 생성됩니다. Laravel이 생성하는 각 폼 리퀘스트 클래스에는 `authorize`와 `rules`라는 두 개의 메서드가 포함됩니다.

<!-- As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data: -->
예상하셨겠지만, `authorize` 메서드는 현재 인증된 사용자가 요청에서 표현된 동작을 수행할 수 있는지 판단하는 역할을 하고, `rules` 메서드는 해당 요청 데이터에 적용될 유효성 검증 규칙을 반환합니다.

```
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
public function rules()
{
    return [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ];
}
```

> [!NOTE]
> `rules` 메서드의 시그니처에 필요로 하는 의존성을 타입힌트로 명시하면, Laravel의 [service container](/docs/9.x/container)를 통해 자동으로 주입받을 수 있습니다.

<!-- So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic: -->
그렇다면 검증 규칙은 언제 평가될까요? 컨트롤러 메서드에서 요청 객체의 타입힌트로 폼 리퀘스트를 명시하기만 하면 됩니다. 요청이 컨트롤러에 전달되기 전에 이미 유효성 검증이 완료되므로, 컨트롤러 내부가 검증 로직으로 복잡해질 필요가 없습니다.

```
/**
 * Store a new blog post.
 *
 * @param  \App\Http\Requests\StorePostRequest  $request
 * @return Illuminate\Http\Response
 */
public function store(StorePostRequest $request)
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);
}
```

<!-- If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a [JSON representation of the validation errors](#validation-error-response-format). -->
만약 검증에 실패하면, 사용자는 이전 위치로 자동 리디렉션되고 오류들은 세션에 플래시되어 뷰에서 표시할 수 있습니다. 요청이 XHR 요청이라면 422 상태 코드와 함께 [JSON representation of the validation errors](#validation-error-response-format)가 반환됩니다.

<a name="adding-after-hooks-to-form-requests"></a>
<!-- #### Adding After Hooks To Form Requests -->
#### Adding After Hooks To Form Requests

<!-- If you would like to add an "after" validation hook to a form request, you may use the `withValidator` method. This method receives the fully constructed validator, allowing you to call any of its methods before the validation rules are actually evaluated: -->
폼 리퀘스트에 유효성 검증 후 추가 작업을 수행하고 싶다면, `withValidator` 메서드를 사용할 수 있습니다. 이 메서드는 생성된 Validator 인스턴스를 전달받으므로, 실제 검증 규칙이 평가되기 전에 원하는 Validator의 메서드를 호출할 수 있습니다.

```
/**
 * Configure the validator instance.
 *
 * @param  \Illuminate\Validation\Validator  $validator
 * @return void
 */
public function withValidator($validator)
{
    $validator->after(function ($validator) {
        if ($this->somethingElseIsInvalid()) {
            $validator->errors()->add('field', 'Something is wrong with this field!');
        }
    });
}
```

<a name="request-stopping-on-first-validation-rule-failure"></a>
<!-- #### Stopping On First Validation Failure Attribute -->
#### Stopping On First Validation Failure Attribute

<!-- By adding a `stopOnFirstFailure` property to your request class, you may inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
폼 리퀘스트 클래스에 `stopOnFirstFailure` 속성을 추가하면, 하나의 검증 실패 발생 시 모든 속성의 검증을 중지하도록 Validator에게 설정할 수 있습니다.

```
/**
 * Indicates if the validator should stop on the first rule failure.
 *
 * @var bool
 */
protected $stopOnFirstFailure = true;
```

<a name="customizing-the-redirect-location"></a>
<!-- #### Customizing The Redirect Location -->
#### Customizing The Redirect Location

<!-- As previously discussed, a redirect response will be generated to send the user back to their previous location when form request validation fails. However, you are free to customize this behavior. To do so, define a `$redirect` property on your form request: -->
앞에서 설명한 대로, 폼 리퀘스트 유효성 검증에 실패하면 사용자는 기본적으로 이전 위치로 리디렉션됩니다. 하지만, 이 동작은 자유롭게 커스터마이즈할 수 있습니다. 이를 위해, 폼 리퀘스트에 `$redirect` 속성을 정의하세요.

```
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

<!-- Or, if you would like to redirect users to a named route, you may define a `$redirectRoute` property instead: -->
또한, named route로 리디렉션하고 싶다면 `$redirectRoute` 속성을 대신 정의할 수 있습니다.

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

<!-- The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/9.x/authorization) within this method: -->
폼 리퀘스트 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드에서는 인증된 사용자가 실제로 주어진 리소스를 수정할 권한이 있는지를 판단할 수 있습니다. 예를 들어, 사용자가 자신이 소유한 블로그 댓글만 수정할 수 있도록 제한할 수 있습니다. 일반적으로 이 메서드에서는 [authorization gates and policies](/docs/9.x/authorization)을 활용하게 됩니다.

```
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 *
 * @return bool
 */
public function authorize()
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

<!-- Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also, note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below: -->
모든 폼 리퀘스트는 Laravel 기본 Request 클래스를 상속하므로, 현재 인증된 사용자에 접근할 땐 `user` 메서드를 사용할 수 있습니다. 위의 예제에서 `route` 메서드를 호출하는 것도 주목하세요. 이 메서드는 호출된 라우트의 URI 파라미터에 접근할 수 있게 해줍니다. 예를 들면, 아래 라우트에서 `{comment}` 파라미터가 해당합니다.

```
Route::post('/comment/{comment}');
```

<!-- Therefore, if your application is taking advantage of [route model binding](/docs/9.x/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request: -->
만약 [route model binding](/docs/9.x/routing#route-model-binding)을 활용하고 있다면, 요청의 속성으로 바인딩된 모델에 더 간단하게 접근할 수도 있습니다.

```
return $this->user()->can('update', $this->comment);
```

<!-- If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute. -->
만약 `authorize` 메서드가 `false`를 반환한다면, Laravel은 자동으로 403 상태코드 HTTP 응답을 반환하며 컨트롤러 메서드는 실행되지 않습니다.

<!-- If you plan to handle authorization logic for the request in another part of your application, you may simply return `true` from the `authorize` method: -->
인증 관련 로직을 애플리케이션의 다른 부분에서 처리할 계획이라면, `authorize` 메서드에서 단순히 `true`를 반환해도 됩니다.

```
/**
 * Determine if the user is authorized to make this request.
 *
 * @return bool
 */
public function authorize()
{
    return true;
}
```

> [!NOTE]
> `authorize` 메서드 시그니처에도 필요한 의존성을 타입힌트로 선언하면, Laravel [service container](/docs/9.x/container)를 통해 자동으로 주입받을 수 있습니다.

<a name="customizing-the-error-messages"></a>
<!-- ### Customizing The Error Messages -->
### Customizing The Error Messages

<!-- You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages: -->
폼 리퀘스트에서 사용하는 오류 메시지를 커스터마이즈하려면 `messages` 메서드를 오버라이딩하면 됩니다. 이 메서드는 속성 / 규칙 조합과 그에 대응하는 오류 메시지를 배열로 반환해야 합니다.

```
/**
 * Get the error messages for the defined validation rules.
 *
 * @return array
 */
public function messages()
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
<!-- #### Customizing The Validation Attributes -->
#### Customizing The Validation Attributes

<!-- Many of Laravel's built-in validation rule error messages contain an `:attribute` placeholder. If you would like the `:attribute` placeholder of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs: -->
Laravel이 기본적으로 제공하는 유효성 검증 오류 메시지에는 `:attribute` 플레이스홀더가 포함된 경우가 많습니다. 해당 `:attribute` 플레이스홀더를 실제 검증 메시지에서 원하는 명칭으로 바꾸려면 `attributes` 메서드를 오버라이딩하세요. 이 메서드는 속성 / 명칭 매핑 배열을 반환해야 합니다.

```
/**
 * Get custom attributes for validator errors.
 *
 * @return array
 */
public function attributes()
{
    return [
        'email' => 'email address',
    ];
}
```

<a name="preparing-input-for-validation"></a>
<!-- ### Preparing Input For Validation -->
### Preparing Input For Validation

<!-- If you need to prepare or sanitize any data from the request before you apply your validation rules, you may use the `prepareForValidation` method: -->
검증 규칙을 적용하기 전에 리퀘스트 데이터의 일부를 전처리(preparing)하거나 정제(sanitizing)해야 한다면, `prepareForValidation` 메서드를 사용하세요.

```
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 *
 * @return void
 */
protected function prepareForValidation()
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

<!-- Likewise, if you need to normalize any request data after validation is complete, you may use the `passedValidation` method: -->
마찬가지로, 검증이 완료된 후에 리퀘스트 데이터를 정규화(normalize)할 필요가 있다면 `passedValidation` 메서드를 사용할 수 있습니다.

```
use Illuminate\Support\Str;

/**
 * Handle a passed validation attempt.
 *
 * @return void
 */
protected function passedValidation()
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
<!-- ## Manually Creating Validators -->
## Manually Creating Validators

<!-- If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/9.x/facades). The `make` method on the facade generates a new validator instance: -->
요청 객체의 `validate` 메서드 대신 직접 Validator 인스턴스를 생성하고자 한다면, `Validator` [facade](/docs/9.x/facades)를 사용할 수 있습니다. 파사드의 `make` 메서드는 새로운 Validator 인스턴스를 반환합니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
     *
     * @param  Request  $request
     * @return Response
     */
    public function store(Request $request)
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
    }
}
```

<!-- The first argument passed to the `make` method is the data under validation. The second argument is an array of the validation rules that should be applied to the data. -->
`make` 메서드에 전달되는 첫 번째 인수는 유효성 검증 대상 데이터이고, 두 번째 인수는 데이터에 적용할 유효성 검증 규칙 배열입니다.

<!-- After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`. -->
요청 검증이 실패했는지 확인한 후에는 `withErrors` 메서드를 사용해 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 리디렉션 후 뷰에서 `$errors` 변수를 자동으로 사용할 수 있으므로, 사용자에게 오류 메시지를 쉽게 표시할 수 있습니다. `withErrors` 메서드는 Validator, `MessageBag`, 또는 PHP `array`를 받을 수 있습니다.

<!-- #### Stopping On First Validation Failure -->
#### Stopping On First Validation Failure

<!-- The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`stopOnFirstFailure` 메서드는 유효성 검증에서 첫 번째 실패가 발생하는 즉시, 모든 속성에 대한 추가 검증을 중단하도록 validator에 알립니다.

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
<!-- ### Automatic Redirection -->
### Automatic Redirection

<!-- If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a [JSON response will be returned](#validation-error-response-format): -->
수동으로 validator 인스턴스를 생성했더라도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션 기능을 그대로 활용하고 싶다면, 기존 validator 인스턴스에서 `validate` 메서드를 호출할 수 있습니다. 유효성 검증에 실패하면 사용자가 자동으로 리다이렉트되고, XHR 요청의 경우에는 [JSON response will be returned](#validation-error-response-format)됩니다.

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

<!-- You may use the `validateWithBag` method to store the error messages in a [named error bag](#named-error-bags) if validation fails: -->
유효성 검증에 실패했을 때 에러 메시지를 [named error bag](#named-error-bags)에 저장하고 싶다면, `validateWithBag` 메서드를 사용할 수 있습니다.

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
한 페이지에 여러 개의 폼이 존재하는 경우, 각 폼에 대한 유효성 검증 에러를 별도의 `MessageBag`에 저장하고 싶을 수 있습니다. 이를 위해 `withErrors`의 두 번째 인수로 이름을 전달하면 에러 메시지를 특정 폼에 대해 구분할 수 있습니다.

```
return redirect('register')->withErrors($validator, 'login');
```

<!-- You may then access the named `MessageBag` instance from the `$errors` variable: -->
이후 해당 이름이 지정된 `MessageBag` 인스턴스를 `$errors` 변수에서 사용할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
<!-- ### Customizing The Error Messages -->
### Customizing The Error Messages

<!-- If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method: -->
필요하다면, validator 인스턴스가 사용할 기본 에러 메시지 대신 직접 정의한 커스텀 에러 메시지를 지정할 수 있습니다. 커스텀 메시지를 지정하는 방법에는 여러 가지가 있습니다. 우선, `Validator::make` 메서드의 세 번째 인수로 커스텀 메시지를 배열로 전달할 수 있습니다.

```
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

<!-- In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example: -->
위 예시에서 `:attribute` 플레이스홀더는 실제로 검증 중인 필드명으로 대체됩니다. 또한 다른 플레이스홀더도 유효성 검증 메시지에서 활용할 수 있습니다. 예를 들어:

```
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
<!-- #### Specifying A Custom Message For A Given Attribute -->
#### Specifying A Custom Message For A Given Attribute

<!-- Sometimes you may wish to specify a custom error message only for a specific attribute. You may do so using "dot" notation. Specify the attribute's name first, followed by the rule: -->
특정 속성에만 커스텀 에러 메시지를 지정하고 싶을 때가 있습니다. 이 경우 "dot" 표기법을 사용하면 됩니다. 먼저 속성명을 적고 그 뒤에 규칙명을 지정합니다.

```
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
<!-- #### Specifying Custom Attribute Values -->
#### Specifying Custom Attribute Values

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method: -->
Laravel의 기본 에러 메시지 중 다수는 검증 중인 속성명을 `:attribute` 플레이스홀더로 출력합니다. 특정 필드에 대해 이 플레이스홀더에 들어갈 값을 커스터마이즈하고 싶다면, `Validator::make`의 네 번째 인수로 커스텀 속성 배열을 전달하면 됩니다.

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="after-validation-hook"></a>
<!-- ### After Validation Hook -->
### After Validation Hook

<!-- You may also attach callbacks to be run after validation is completed. This allows you to easily perform further validation and even add more error messages to the message collection. To get started, call the `after` method on a validator instance: -->
유효성 검증이 끝난 후 실행할 콜백을 추가할 수도 있습니다. 이를 통해 추가적인 검증 작업을 쉽게 수행하거나, 메시지 컬렉션에 에러 메시지를 더할 수 있습니다. 사용 방법은 validator 인스턴스에서 `after` 메서드를 호출하면 됩니다.

```
$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    //
}
```

<a name="working-with-validated-input"></a>
<!-- ## Working With Validated Input -->
## Working With Validated Input

<!-- After validating incoming request data using a form request or a manually created validator instance, you may wish to retrieve the incoming request data that actually underwent validation. This can be accomplished in several ways. First, you may call the `validated` method on a form request or validator instance. This method returns an array of the data that was validated: -->
폼 리퀘스트나 직접 생성한 validator 인스턴스로 요청 데이터를 검증한 후에는, 실제로 검증이 진행된 데이터를 가져오고 싶을 때가 많습니다. 이 작업은 여러 방법으로 가능합니다. 우선, 폼 리퀘스트나 validator 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 검증된 데이터를 배열로 반환합니다.

```
$validated = $request->validated();

$validated = $validator->validated();
```

<!-- Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data: -->
또는, 폼 리퀘스트나 validator 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환하며, 이 객체는 `only`, `except`, `all` 메서드를 제공하여 검증된 데이터의 일부 또는 전체를 원하는 형태로 가져올 수 있습니다.

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

<!-- In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array: -->
또한, `Illuminate\Support\ValidatedInput` 인스턴스는 반복문으로 순회하거나 배열처럼 접근할 수도 있습니다.

```
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    //
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

<!-- If you would like to add additional fields to the validated data, you may call the `merge` method: -->
만약 검증된 데이터에 추가 필드를 더하고 싶다면, `merge` 메서드를 사용할 수 있습니다.

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

<!-- If you would like to retrieve the validated data as a [collection](/docs/9.x/collections) instance, you may call the `collect` method: -->
[collection](/docs/9.x/collections) 인스턴스로 검증된 데이터를 받고 싶다면, `collect` 메서드를 사용할 수 있습니다.

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
<!-- ## Working With Error Messages -->
## Working With Error Messages

<!-- After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class. -->
`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 여러 가지 편리한 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 또한, 뷰에서 자동으로 사용할 수 있는 `$errors` 변수도 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
<!-- #### Retrieving The First Error Message For A Field -->
#### Retrieving The First Error Message For A Field

<!-- To retrieve the first error message for a given field, use the `first` method: -->
특정 필드에 대한 첫 번째 에러 메시지를 가져오려면, `first` 메서드를 사용합니다.

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
<!-- #### Retrieving All Error Messages For A Field -->
#### Retrieving All Error Messages For A Field

<!-- If you need to retrieve an array of all the messages for a given field, use the `get` method: -->
특정 필드에 대해 메시지 전체 배열을 가져와야 할 때는, `get` 메서드를 사용합니다.

```
foreach ($errors->get('email') as $message) {
    //
}
```

<!-- If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character: -->
배열 형태의 폼 필드를 검증할 경우, `*` 문자를 사용해 배열 각 요소의 모든 메시지를 가져올 수 있습니다.

```
foreach ($errors->get('attachments.*') as $message) {
    //
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
<!-- #### Retrieving All Error Messages For All Fields -->
#### Retrieving All Error Messages For All Fields

<!-- To retrieve an array of all messages for all fields, use the `all` method: -->
모든 필드에 대한 에러 메시지 배열을 얻고 싶다면 `all` 메서드를 사용하세요.

```
foreach ($errors->all() as $message) {
    //
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
<!-- #### Determining If Messages Exist For A Field -->
#### Determining If Messages Exist For A Field

<!-- The `has` method may be used to determine if any error messages exist for a given field: -->
`has` 메서드를 사용하면 특정 필드에 에러 메시지가 존재하는지 확인할 수 있습니다.

```
if ($errors->has('email')) {
    //
}
```

<a name="specifying-custom-messages-in-language-files"></a>
<!-- ### Specifying Custom Messages In Language Files -->
### Specifying Custom Messages In Language Files

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. Within this file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
Laravel 기본 유효성 검증 규칙들은 각각의 에러 메시지가 애플리케이션의 `lang/en/validation.php` 파일에 정의되어 있습니다. 이 파일에는 각 유효성 검증 규칙에 해당하는 번역 항목이 존재합니다. 필요에 따라 이 메시지들을 변경하거나 수정하여 애플리케이션의 요구 사항에 맞게 사용할 수 있습니다.

<!-- In addition, you may copy this file to another translation language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/9.x/localization). -->
또한, 이 파일을 다른 언어의 번역 디렉터리로 복사하여 애플리케이션에서 사용할 언어로 메시지를 번역할 수 있습니다. Laravel의 로컬라이제이션 기능에 대한 자세한 내용은 [localization documentation](/docs/9.x/localization)를 참고하십시오.

<a name="custom-messages-for-specific-attributes"></a>
<!-- #### Custom Messages For Specific Attributes -->
#### Custom Messages For Specific Attributes

<!-- You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file: -->
애플리케이션의 유효성 검증 언어 파일에서 특정 속성-규칙 조합에 대한 에러 메시지도 커스터마이즈할 수 있습니다. 이를 위해, `lang/xx/validation.php` 언어 파일의 `custom` 배열에 커스텀 메시지를 추가하세요.

```
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
<!-- ### Specifying Attributes In Language Files -->
### Specifying Attributes In Language Files

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. If you would like the `:attribute` portion of your validation message to be replaced with a custom value, you may specify the custom attribute name in the `attributes` array of your `lang/xx/validation.php` language file: -->
Laravel의 기본 에러 메시지 다수에는 검증 중인 속성명을 나타내는 `:attribute` 플레이스홀더가 포함되어 있습니다. 만약 유효성 메시지의 `:attribute` 부분을 원하는 값으로 바꿔서 보여주고 싶다면, `lang/xx/validation.php` 파일의 `attributes` 배열에 원하는 속성명을 추가하여 지정할 수 있습니다.

```
'attributes' => [
    'email' => 'email address',
],
```

<a name="specifying-values-in-language-files"></a>
<!-- ### Specifying Values In Language Files -->
### Specifying Values In Language Files

<!-- Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`: -->
일부 Laravel 기본 유효성 검증 규칙은 `:value` 플레이스홀더를 포함합니다. 이 플레이스홀더는 현재 요청 속성의 실제 값으로 대체되지만, 경우에 따라 `:value` 부분을 더 사용자 친화적인 용어로 바꾸고 싶을 수 있습니다. 예를 들어, `payment_type`이 `cc`인 경우에 신용카드 번호 입력을 필수로 지정하는 규칙을 다음과 같이 설정할 수 있습니다.

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

<!-- If this validation rule fails, it will produce the following error message: -->
이 검증 규칙이 실패하면 아래와 같은 에러 메시지가 출력됩니다.

```none
The credit card number field is required when payment type is cc.
```

<!-- Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `lang/xx/validation.php` language file by defining a `values` array: -->
이때 `cc` 대신 좀 더 읽기 쉬운 값을 표시하고 싶다면, `lang/xx/validation.php` 언어 파일의 `values` 배열에 값을 지정할 수 있습니다.

```
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

<!-- After defining this value, the validation rule will produce the following error message: -->
이렇게 값을 지정하면 유효성 검증 실패 시 아래와 같은 보다 읽기 쉬운 메시지가 출력됩니다.

```none
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
<!-- ## Available Validation Rules -->
## Available Validation Rules

<!-- Below is a list of all available validation rules and their function: -->
아래는 사용 가능한 모든 유효성 검증 규칙과 각 규칙의 역할을 정리한 목록입니다.



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
[File](#rule-file)
[Filled](#rule-filled)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
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
[Password](#rule-password)
[Present](#rule-present)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Regular Expression](#rule-regex)
[Required](#rule-required)
[Required If](#rule-required-if)
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
[File](#rule-file)
[Filled](#rule-filled)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
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
[Password](#rule-password)
[Present](#rule-present)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Regular Expression](#rule-regex)
[Required](#rule-required)
[Required If](#rule-required-if)
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

<!-- The field under validation must be `"yes"`, `"on"`, `1`, or `true`. This is useful for validating "Terms of Service" acceptance or similar fields. -->
해당 필드는 값이 `"yes"`, `"on"`, `1`, 또는 `true`여야 합니다. 보통 "약관 동의"와 같은 필드의 유효성 검증에 유용하게 쓸 수 있습니다.

<a name="rule-accepted-if"></a>
<!-- #### accepted_if:anotherfield,value,... -->
#### accepted_if:anotherfield,value,...

<!-- The field under validation must be `"yes"`, `"on"`, `1`, or `true` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields. -->
해당 필드는, 다른 검증 대상 필드가 지정한 값과 동일할 때, 값이 `"yes"`, `"on"`, `1`, 또는 `true`여야 합니다. 이 규칙 역시 "약관 동의" 등과 같은 케이스에 활용할 수 있습니다.

<a name="rule-active-url"></a>
<!-- #### active_url -->
#### active_url

<!-- The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`. -->
해당 필드는 PHP의 `dns_get_record` 함수 기준으로 유효한 A 또는 AAAA 레코드를 갖는 URL이어야 합니다. 제공된 URL의 호스트명은 사전에 PHP의 `parse_url` 함수로 추출한 후 `dns_get_record`로 전달됩니다.

<a name="rule-after"></a>
<!-- #### after:_date_ -->
#### after:_date_

<!-- The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance: -->
해당 필드는 지정한 날짜 이후의 값이어야 합니다. 날짜 값은 PHP의 `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다.

```
'start_date' => 'required|date|after:tomorrow'
```

<!-- Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date: -->
`strtotime`으로 평가할 날짜 문자열 대신, 비교 대상으로 다른 필드를 지정할 수도 있습니다.

```
'finish_date' => 'required|date|after:start_date'
```

<a name="rule-after-or-equal"></a>
<!-- #### after\_or\_equal:_date_ -->
#### after\_or\_equal:_date_

<!-- The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule. -->
해당 필드는 지정한 날짜 이후 또는 같은 날짜여야 합니다. 자세한 내용은 [after](#rule-after) 규칙 설명을 참고하세요.

<a name="rule-alpha"></a>
<!-- #### alpha -->
#### alpha

<!-- The field under validation must be entirely Unicode alphabetic characters contained in [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) and [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=). -->
해당 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) 집합에 속하는 유니코드 알파벳 문자로만 구성되어야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
만약 ASCII 범위(`a-z`, `A-Z`)로 제한하고 싶다면, 검증 규칙에 `ascii` 옵션을 추가할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
<!-- #### alpha_dash -->
#### alpha_dash

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), as well as ASCII dashes (`-`) and ASCII underscores (`_`). -->
해당 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) 집합에 속하는 유니코드 영문, 숫자, 그리고 ASCII 대시(`-`), 언더스코어(`_`) 문자로만 구성되어야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
역시 문자 집합을 ASCII 값(`a-z`, `A-Z`)으로만 제한하려면, `ascii` 옵션을 추가하면 됩니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
<!-- #### alpha_num -->
#### alpha_num

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), and [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=). -->
해당 필드는 [`\p{L}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [`\p{M}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [`\p{N}`](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) 집합에 속하는 유니코드 알파벳 또는 숫자만 사용할 수 있습니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
ASCII 범위(`a-z` 및 `A-Z`)로만 제한하고 싶을 때는, `ascii` 옵션을 추가하세요.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
<!-- #### array -->
#### array

<!-- The field under validation must be a PHP `array`. -->
해당 필드는 PHP의 `array` 여야 합니다.

<!-- When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule: -->
`array` 규칙에 값을 추가로 지정하면, 입력 배열의 각 키가 지정값 목록에 포함되어 있어야 합니다. 예를 들어 아래 코드에서 입력 배열의 `admin` 키는 `array` 규칙에 지정된 값 목록에 없으므로 유효하지 않습니다.

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
일반적으로, 배열 내에 허용할 키를 명확하게 지정하는 것이 좋습니다.

<a name="rule-ascii"></a>
<!-- #### ascii -->
#### ascii

<!-- The field under validation must be entirely 7-bit ASCII characters. -->
해당 필드는 7비트 ASCII 문자로만 구성되어야 합니다.

<a name="rule-bail"></a>
<!-- #### bail -->
#### bail

<!-- Stop running validation rules for the field after the first validation failure. -->
해당 필드에서 첫 번째 유효성 검증 실패가 발생한 경우 이후 나머지 유효성 검증 규칙은 실행하지 않고 중단합니다.

<!-- While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`bail` 규칙은 특정 필드에 대해서만 유효성 검증 실패 시 추가 검증을 중단하지만, `stopOnFirstFailure` 메서드는 어느 필드에서든 유효성 검증에 실패하면 모든 속성의 검증 자체를 즉시 중단합니다.

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
<!-- #### before:_date_ -->
#### before:_date_

<!-- The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
해당 필드는 지정한 날짜 이전의 값이어야 합니다. 날짜들은 PHP `strtotime` 함수에 전달되어 올바른 `DateTime` 인스턴스로 변환됩니다. 또한, [`after`](#rule-after) 규칙과 마찬가지로 검증 대상이 되는 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

<a name="rule-before-or-equal"></a>
<!-- #### before\_or\_equal:_date_ -->
#### before\_or\_equal:_date_

<!-- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
해당 필드는 지정한 날짜 이전 또는 같은 값이어야 합니다. 날짜 값은 PHP의 `strtotime` 함수에 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한, [`after`](#rule-after) 규칙과 마찬가지로 검증에 사용할 다른 필드명을 `date` 값으로 지정할 수도 있습니다.

<a name="rule-between"></a>
<!-- #### between:_min_,_max_ -->
#### between:_min_,_max_

<!-- The field under validation must have a size between the given _min_ and _max_ (inclusive). Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
해당 필드는 _min_과 _max_(포함) 사이의 크기를 가져야 합니다. 문자열, 숫자, 배열, 파일의 경우, [`size`](#rule-size) 규칙과 동일한 방식으로 크기가 측정됩니다.

<a name="rule-boolean"></a>
<!-- #### boolean -->
#### boolean

<!-- The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`. -->
해당 필드는 불리언으로 변환될 수 있어야 합니다. 가능한 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<a name="rule-confirmed"></a>
<!-- #### confirmed -->
#### confirmed

<!-- The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input. -->
해당 필드와 `{field}_confirmation` 입력값이 일치해야 합니다. 예를 들어, 검증 대상 필드가 `password`라면 입력 데이터에 `password_confirmation` 필드도 있어야 합니다.

<a name="rule-current-password"></a>
<!-- #### current_password -->
#### current_password

<!-- The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/9.x/authentication) using the rule's first parameter: -->
해당 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 파라미터로 [authentication guard](/docs/9.x/authentication)를 지정할 수도 있습니다.

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
<!-- #### date -->
#### date

<!-- The field under validation must be a valid, non-relative date according to the `strtotime` PHP function. -->
해당 필드는 PHP `strtotime` 함수 기준으로 유효한(상대적이지 않은) 날짜여야 합니다.

<a name="rule-date-equals"></a>
<!-- #### date_equals:_date_ -->
#### date_equals:_date_

<!-- The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. -->
해당 필드는 지정한 날짜와 동일해야 합니다. 입력 날짜는 PHP `strtotime` 함수에 전달되어 올바른 `DateTime` 인스턴스로 변환됩니다.

<a name="rule-date-format"></a>
<!-- #### date_format:_format_,... -->
#### date_format:_format_,...

<!-- The field under validation must match one of the given _formats_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class. -->
해당 필드는 지정 포맷과 일치해야 합니다. 하나의 필드를 검증할 때는 `date` 또는 `date_format` 중 하나만 사용해야 합니다. 이 검증 규칙은 PHP [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 포맷을 지원합니다.

<a name="rule-decimal"></a>
<!-- #### decimal:_min_,_max_ -->
#### decimal:_min_,_max_

<!-- The field under validation must be numeric and must contain the specified number of decimal places: -->
해당 필드는 숫자 형식이어야 하며, 지정된 소수 자릿수를 가져야 합니다.

```
// Must have exactly two decimal places (9.99)...
'price' => 'decimal:2'

// Must have between 2 and 4 decimal places...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>

<!-- #### declined -->
#### declined

<!-- The field under validation must be `"no"`, `"off"`, `0`, or `false`. -->
검증 대상 필드는 `"no"`, `"off"`, `0`, 또는 `false` 중 하나여야 합니다.

<a name="rule-declined-if"></a>
<!-- #### declined_if:anotherfield,value,... -->
#### declined_if:anotherfield,value,...

<!-- The field under validation must be `"no"`, `"off"`, `0`, or `false` if another field under validation is equal to a specified value. -->
만약 또 다른 검증 대상 필드가 지정한 값과 같다면, 검증 대상 필드는 `"no"`, `"off"`, `0`, 또는 `false` 중 하나여야 합니다.

<a name="rule-different"></a>
<!-- #### different:_field_ -->
#### different:_field_

<!-- The field under validation must have a different value than _field_. -->
검증 대상 필드의 값은 _field_와 달라야 합니다.

<a name="rule-digits"></a>
<!-- #### digits:_value_ -->
#### digits:_value_

<!-- The integer under validation must have an exact length of _value_. -->
검증 대상 정수는 _value_ 자리 수여야 합니다.

<a name="rule-digits-between"></a>
<!-- #### digits_between:_min_,_max_ -->
#### digits_between:_min_,_max_

<!-- The integer validation must have a length between the given _min_ and _max_. -->
검증 대상 정수의 자리 수는 _min_보다 크거나 같고 _max_보다 작거나 같아야 합니다.

<a name="rule-dimensions"></a>
<!-- #### dimensions -->
#### dimensions

<!-- The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters: -->
검증 대상 파일은 아래와 같이 규칙의 파라미터로 지정된 이미지 크기 제약 조건을 충족하는 이미지여야 합니다.

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

<!-- Available constraints are: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_. -->
사용 가능한 제약 조건은 다음과 같습니다: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

<!-- A _ratio_ constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`: -->
_ratio_ 제약 조건은 가로/세로 비율로 입력하며, 분수(`3/2`) 또는 실수(`1.5`) 형식으로 지정할 수 있습니다.

```
'avatar' => 'dimensions:ratio=3/2'
```

<!-- Since this rule requires several arguments, you may use the `Rule::dimensions` method to fluently construct the rule: -->
이 규칙은 여러 인자가 필요하므로, `Rule::dimensions` 메서드를 사용해 규칙을 좀 더 유연하게 작성할 수 있습니다.

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
배열을 검증할 때, 값이 중복되면 안 됩니다.

```
'foo.*.id' => 'distinct'
```

<!-- Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition: -->
distinct는 기본적으로 느슨한(값 중심의) 비교를 사용합니다. 엄격한 비교를 적용하려면, 검증 규칙 정의에 `strict` 파라미터를 추가할 수 있습니다.

```
'foo.*.id' => 'distinct:strict'
```

<!-- You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences: -->
대소문자 차이를 무시하고 싶다면, `ignore_case`를 검증 규칙 인수에 추가하세요.

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
<!-- #### doesnt_start_with:_foo_,_bar_,... -->
#### doesnt_start_with:_foo_,_bar_,...

<!-- The field under validation must not start with one of the given values. -->
검증 대상 필드는 주어진 값들 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
<!-- #### doesnt_end_with:_foo_,_bar_,... -->
#### doesnt_end_with:_foo_,_bar_,...

<!-- The field under validation must not end with one of the given values. -->
검증 대상 필드는 주어진 값들 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
<!-- #### email -->
#### email

<!-- The field under validation must be formatted as an email address. This validation rule utilizes the [`egulias/email-validator`](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well: -->
검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 검증 규칙은 이메일 형식 검증을 위해 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 방식이 적용되지만, 다음과 같이 여러 종류의 검증 스타일을 선택할 수 있습니다.

```
'email' => 'email:rfc,dns'
```

<!-- The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply: -->
위 예시는 `RFCValidation`과 `DNSCheckValidation` 검사를 동시에 적용합니다. 사용할 수 있는 모든 검증 스타일 목록은 다음과 같습니다.

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
`filter` 검증기는 PHP의 `filter_var` 함수를 사용하며, Laravel 5.8 이전까지 기본 이메일 검증 방식으로 사용되었습니다.

> [!WARNING]
> `dns`와 `spoof` 검증기는 PHP의 `intl` 확장이 필요합니다.

<a name="rule-ends-with"></a>
<!-- #### ends_with:_foo_,_bar_,... -->
#### ends_with:_foo_,_bar_,...

<!-- The field under validation must end with one of the given values. -->
검증 대상 필드는 주어진 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
<!-- #### enum -->
#### enum

<!-- The `Enum` rule is a class based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument: -->
`Enum` 규칙은, 검증 대상 필드 값이 지정한 Enum(열거형) 값 중 하나인지 확인하는 클래스 기반 규칙입니다. 이 `Enum` 규칙은 Enum의 이름을 생성자 인수로 받습니다.

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rules\Enum;

$request->validate([
    'status' => [new Enum(ServerStatus::class)],
]);
```

> [!WARNING]
> Enum은 PHP 8.1 이상에서만 사용할 수 있습니다.

<a name="rule-exclude"></a>
<!-- #### exclude -->
#### exclude

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods. -->
검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
<!-- #### exclude_if:_anotherfield_,_value_ -->
#### exclude_if:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_. -->
만약 _anotherfield_ 필드가 _value_와 같으면, 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<!-- If complex conditional exclusion logic is required, you may utilize the `Rule::excludeIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be excluded: -->
복잡한 조건으로 제외해야 할 경우, `Rule::excludeIf` 메서드를 사용하세요. 이 메서드는 불리언 값이나 클로저(익명 함수)를 인수로 받습니다. 클로저를 사용할 경우, 해당 클로저에서는 필드를 제외할지 `true` 또는 `false`를 반환하면 됩니다.

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
_ anotherfield_ 필드가 _value_와 같지 않으면, 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다. _value_가 `null` (`exclude_unless:name,null`)일 때는, 비교할 필드가 `null`이거나 요청 데이터에서 누락된 경우 필드는 제외되지 않습니다.

<a name="rule-exclude-with"></a>
<!-- #### exclude_with:_anotherfield_ -->
#### exclude_with:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is present. -->
_ anotherfield_ 필드가 존재하면, 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
<!-- #### exclude_without:_anotherfield_ -->
#### exclude_without:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present. -->
_ anotherfield_ 필드가 존재하지 않으면, 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
<!-- #### exists:_table_,_column_ -->
#### exists:_table_,_column_

<!-- The field under validation must exist in a given database table. -->
검증 대상 필드의 값은 지정한 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
<!-- #### Basic Usage Of Exists Rule -->
#### Basic Usage Of Exists Rule

```
'state' => 'exists:states'
```

<!-- If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value. -->
`column` 옵션을 지정하지 않으면 필드명이 사용됩니다. 위 예시에서는 요청 데이터의 `state` 속성 값과 같은 `state` 컬럼 값을 가진 레코드가 `states` 테이블에 존재하는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
<!-- #### Specifying A Custom Column Name -->
#### Specifying A Custom Column Name

<!-- You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name: -->
테이블명 뒤에 사용할 컬럼명을 직접 지정할 수 있습니다.

```
'state' => 'exists:states,abbreviation'
```

<!-- Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name: -->
간혹 `exists` 쿼리를 특정 데이터베이스 연결에서 실행해야 할 경우, 테이블명 앞에 연결 이름을 붙여 지정할 수 있습니다.

```
'email' => 'exists:connection.staff,email'
```

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블명을 직접 지정하는 대신, 해당 테이블명을 사용하는 Eloquent 모델명을 지정할 수도 있습니다.

```
'user_id' => 'exists:App\Models\User,id'
```

<!-- If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them: -->
`Rule` 클래스를 사용하면 쿼리를 더욱 유연하게 커스터마이징할 수 있습니다. 아래 예시에서는 `|` 문자를 구분자로 사용하는 대신 검증 규칙도 배열로 나열하고 있습니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function ($query) {
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

<a name="rule-file"></a>
<!-- #### file -->
#### file

<!-- The field under validation must be a successfully uploaded file. -->
검증 대상 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
<!-- #### filled -->
#### filled

<!-- The field under validation must not be empty when it is present. -->
검증 대상 필드가 존재한다면 값이 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
<!-- #### gt:_field_ -->
#### gt:_field_

<!-- The field under validation must be greater than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_ 값보다 커야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 비교됩니다.

<a name="rule-gte"></a>
<!-- #### gte:_field_ -->
#### gte:_field_

<!-- The field under validation must be greater than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_ 값보다 크거나 같아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 비교됩니다.

<a name="rule-image"></a>
<!-- #### image -->
#### image

<!-- The file under validation must be an image (jpg, jpeg, png, bmp, gif, svg, or webp). -->
검증 대상 파일은 이미지 파일이어야 합니다(jpg, jpeg, png, bmp, gif, svg, webp).

<a name="rule-in"></a>
<!-- #### in:_foo_,_bar_,... -->
#### in:_foo_,_bar_,...

<!-- The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule: -->
검증 대상 필드는 지정된 값 목록 중 하나에 포함되어야 합니다. 종종 배열을 `implode` 해서 사용해야 하므로, `Rule::in` 메서드를 활용하면 더욱 유연하게 규칙을 정의할 수 있습니다.

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
`in` 규칙을 `array` 규칙과 함께 쓰면, 입력 배열의 각 값이 `in` 규칙의 목록에 모두 포함되어야 합니다. 아래 예시에서 입력 배열에 포함된 `LAS` 공항 코드는, `in` 규칙에 제공된 공항 코드 목록에 포함되지 않으므로 유효하지 않습니다.

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
검증 대상 필드는 _anotherfield_의 값 목록 중 하나여야 합니다.

<a name="rule-integer"></a>
<!-- #### integer -->
#### integer

<!-- The field under validation must be an integer. -->
검증 대상 필드는 정수여야 합니다.

> [!WARNING]
> 이 검증 규칙은 입력값이 "정수형" 변수 타입인지까지는 검사하지 않습니다. 단지 입력값이 PHP의 `FILTER_VALIDATE_INT` 규칙에 허용되는 타입이면 통과합니다. 입력값이 숫자인지까지 엄격하게 검사하려면 [the `numeric` validation rule](#rule-numeric)과 함께 사용하세요.

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
검증 대상 필드는 지정된 _field_보다 작아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 비교됩니다.

<a name="rule-lte"></a>
<!-- #### lte:_field_ -->
#### lte:_field_

<!-- The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
검증 대상 필드는 지정된 _field_보다 작거나 같아야 합니다. 두 필드는 같은 타입이어야 하며, 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일한 방식으로 비교됩니다.

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
검증 대상 필드는 최대 _value_ 이하여야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-max-digits"></a>
<!-- #### max_digits:_value_ -->
#### max_digits:_value_

<!-- The integer under validation must have a maximum length of _value_. -->
검증 대상 정수의 자리 수는 _value_ 이하여야 합니다.

<a name="rule-mimetypes"></a>
<!-- #### mimetypes:_text/plain_,... -->
#### mimetypes:_text/plain_,...

<!-- The file under validation must match one of the given MIME types: -->
검증 대상 파일은 주어진 MIME 타입 목록 중 하나와 일치해야 합니다.

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

<!-- To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type. -->
업로드된 파일의 MIME 타입을 판별하기 위해, 파일 내용을 읽어서 프레임워크가 MIME 타입을 추정합니다. 이 결과는 클라이언트가 전송한 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
<!-- #### mimes:_foo_,_bar_,... -->
#### mimes:_foo_,_bar_,...

<!-- The file under validation must have a MIME type corresponding to one of the listed extensions. -->
검증 대상 파일의 MIME 타입이 나열된 확장자 중 하나와 일치해야 합니다.

<a name="basic-usage-of-mime-rule"></a>
<!-- #### Basic Usage Of MIME Rule -->
#### Basic Usage Of MIME Rule

```
'photo' => 'mimes:jpg,bmp,png'
```

<!-- Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
여기에는 확장자만 지정하지만, 실제로는 파일 내용을 읽고 MIME 타입을 추정해서 확장자와 일치하는지 확인합니다. MIME 타입과 그에 해당하는 확장자 전체 목록은 다음에서 확인할 수 있습니다.

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
<!-- #### min:_value_ -->
#### min:_value_

<!-- The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
검증 대상 필드는 최소 _value_보다 크거나 같아야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="rule-min-digits"></a>
<!-- #### min_digits:_value_ -->
#### min_digits:_value_

<!-- The integer under validation must have a minimum length of _value_. -->
검증 대상 정수의 자리 수는 _value_ 이상이어야 합니다.

<a name="rule-multiple-of"></a>
<!-- #### multiple_of:_value_ -->
#### multiple_of:_value_

<!-- The field under validation must be a multiple of _value_. -->
검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
<!-- #### missing -->
#### missing

<!-- The field under validation must not be present in the input data. -->
검증 대상 필드는 입력 데이터에 존재하면 안 됩니다.

 <a name="rule-missing-if"></a>
<!-- #### missing_if:_anotherfield_,_value_,... -->
 #### missing_if:_anotherfield_,_value_,...

<!--  The field under validation must not be present if the _anotherfield_ field is equal to any _value_. -->
 _anotherfield_ 필드가 _value_ 값 중 하나와 같으면, 검증 대상 필드는 존재하면 안 됩니다.

 <a name="rule-missing-unless"></a>
<!-- #### missing_unless:_anotherfield_,_value_ -->
 #### missing_unless:_anotherfield_,_value_

<!-- The field under validation must not be present unless the _anotherfield_ field is equal to any _value_. -->
_ anotherfield_ 필드가 _value_ 값 중 하나와 같지 않으면, 검증 대상 필드는 존재하면 안 됩니다.

 <a name="rule-missing-with"></a>
<!-- #### missing_with:_foo_,_bar_,... -->
 #### missing_with:_foo_,_bar_,...

<!--  The field under validation must not be present _only if_ any of the other specified fields are present. -->
 지정된 다른 필드들 중 하나라도 존재할 경우에만, 검증 대상 필드는 존재하면 안 됩니다.

 <a name="rule-missing-with-all"></a>
<!-- #### missing_with_all:_foo_,_bar_,... -->
 #### missing_with_all:_foo_,_bar_,...

<!--  The field under validation must not be present _only if_ all of the other specified fields are present. -->
 지정된 다른 필드들이 모두 존재할 경우에만, 검증 대상 필드는 존재하면 안 됩니다.

<a name="rule-not-in"></a>
<!-- #### not_in:_foo_,_bar_,... -->
#### not_in:_foo_,_bar_,...

<!-- The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule: -->
검증 대상 필드의 값은 지정된 값 목록에 포함되면 안 됩니다. `Rule::notIn` 메서드를 사용하면 규칙을 유연하게 정의할 수 있습니다.

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
검증 대상 필드는 지정한 정규 표현식 패턴과 일치하지 않아야 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`. -->
이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 지정한 패턴은 `preg_match`가 요구하는 형식과 동일하게, 올바른 구분자를 포함해야 합니다. 예시: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, `|` 구분자를 사용하는 대신 규칙을 배열로 지정해야 할 수 있습니다. 특히 정규식에 `|` 문자가 포함된 경우 그렇습니다.

<a name="rule-nullable"></a>
<!-- #### nullable -->
#### nullable

<!-- The field under validation may be `null`. -->
검증 대상 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
<!-- #### numeric -->
#### numeric

<!-- The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php). -->
검증 대상 필드는 [numeric](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<a name="rule-password"></a>
<!-- #### password -->
#### password

<!-- The field under validation must match the authenticated user's password. -->
검증 대상 필드는 인증된 사용자의 비밀번호와 일치해야 합니다.

> [!WARNING]
> 이 규칙은 Laravel 9에서 제거될 예정이며, `current_password`로 이름이 변경되었습니다. [Current Password](#rule-current-password) 규칙을 대신 사용하세요.

<a name="rule-present"></a>
<!-- #### present -->
#### present

<!-- The field under validation must exist in the input data. -->
검증 대상 필드는 입력 데이터에 반드시 존재해야 합니다.

<a name="rule-prohibited"></a>
<!-- #### prohibited -->
#### prohibited

<!-- The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
검증 대상 필드는 입력 데이터에 존재하지 않거나 "비어 있어야" 합니다. "비어 있음"의 기준은 다음 중 하나를 만족하면 됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일인데 파일 경로가 비어 있는 경우

<!-- </div> -->
</div>

<a name="rule-prohibited-if"></a>
<!-- #### prohibited_if:_anotherfield_,_value_,... -->
#### prohibited_if:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
_ anotherfield_ 필드가 _value_ 값 중 하나와 같으면, 검증 대상 필드는 존재하지 않거나 "비어 있어야" 합니다. "비어 있음"의 기준은 다음과 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일인데 파일 경로가 비어 있는 경우

<!-- </div> -->
</div>

<!-- If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited: -->
복잡한 조건에 따라 필드를 금지해야 한다면, `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 인수로 받으며, 클로저를 사용할 때는 필드를 금지할지 `true` 또는 `false`를 반환해야 합니다.

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
_ anotherfield_ 필드가 _value_ 값 중 하나와 같지 않으면, 검증 대상 필드는 존재하지 않거나 "비어 있어야" 합니다. "비어 있음"의 기준은 다음과 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일인데 파일 경로가 비어 있는 경우

<!-- </div> -->
</div>

<a name="rule-prohibits"></a>
<!-- #### prohibits:_anotherfield_,... -->
#### prohibits:_anotherfield_,...

<!-- If the field under validation is not missing or empty, all fields in _anotherfield_ must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
검증 대상 필드가 존재하고 비어 있지 않다면, _anotherfield_에 나열된 모든 필드는 존재하지 않거나 "비어 있어야" 합니다. "비어 있음"의 기준은 다음 중 하나를 만족하면 됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일인데 파일 경로가 비어 있는 경우

<!-- </div> -->
</div>

<a name="rule-regex"></a>
<!-- #### regex:_pattern_ -->
#### regex:_pattern_

<!-- The field under validation must match the given regular expression. -->
검증 대상 필드는 지정한 정규 표현식과 일치해야 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`. -->
이 규칙은 내부적으로 PHP의 `preg_match` 함수를 사용합니다. 지정한 패턴은 `preg_match`와 동일한 포맷 및 구분자를 포함해야 합니다. 예시: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, `|` 구분자를 사용하는 대신 규칙을 배열로 지정해야 합니다. 특히 정규식에 `|` 문자가 포함된 경우 그렇습니다.

<a name="rule-required"></a>
<!-- #### required -->
#### required

<!-- The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria: -->
검증 대상 필드는 입력 데이터에 반드시 존재해야 하며, 빈 값이어서는 안 됩니다. "비어 있음"의 기준은 다음 중 하나를 만족하면 됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.
-->
- 값이 `null`인 경우
- 값이 빈 문자열인 경우
- 값이 빈 배열이거나 빈 `Countable` 객체인 경우
- 업로드된 파일인데 파일 경로가 없는 경우

<!-- </div> -->
</div>

<a name="rule-required-if"></a>

<!-- #### required_if:_anotherfield_,_value_,... -->
#### required_if:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_. -->
유효성 검증 대상 필드는, _anotherfield_ 필드가 _value_ 값과 같을 때 반드시 존재해야 하며 비어 있지 않아야 합니다.

<!-- If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required: -->
`required_if` 규칙에 더 복잡한 조건을 사용하고 싶다면, `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불린 값이나 클로저를 인자로 받을 수 있습니다. 클로저가 전달된 경우, 해당 클로저는 해당 필드의 필수 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

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

<a name="rule-required-unless"></a>
<!-- #### required_unless:_anotherfield_,_value_,... -->
#### required_unless:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data. -->
유효성 검증 대상 필드는, _anotherfield_ 필드가 _value_ 값과 같지 않을 때 반드시 존재해야 하며 비어 있지 않아야 합니다. 이는 _anotherfield_ 필드는 _value_가 `null`이 아닌 한 요청 데이터에 반드시 포함되어야 함을 의미합니다. 만약 _value_가 `null`인 경우(`required_unless:name,null`), 비교 대상 필드가 `null`이거나 요청 데이터에 없는 경우에는 해당 필드가 필수가 아닙니다.

<a name="rule-required-with"></a>
<!-- #### required_with:_foo_,_bar_,... -->
#### required_with:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty. -->
지정된 다른 필드 중 하나라도 존재하고 비어 있지 않다면, 유효성 검증 대상 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-with-all"></a>
<!-- #### required_with_all:_foo_,_bar_,... -->
#### required_with_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty. -->
지정된 다른 모든 필드가 존재하고 비어 있지 않은 경우에만, 유효성 검증 대상 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without"></a>
<!-- #### required_without:_foo_,_bar_,... -->
#### required_without:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present. -->
지정된 다른 필드 중 하나라도 비어 있거나 존재하지 않을 때에만, 유효성 검증 대상 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-without-all"></a>
<!-- #### required_without_all:_foo_,_bar_,... -->
#### required_without_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present. -->
지정된 다른 모든 필드가 비어 있거나 존재하지 않을 때에만, 유효성 검증 대상 필드는 반드시 존재하고 비어 있지 않아야 합니다.

<a name="rule-required-array-keys"></a>
<!-- #### required_array_keys:_foo_,_bar_,... -->
#### required_array_keys:_foo_,_bar_,...

<!-- The field under validation must be an array and must contain at least the specified keys. -->
유효성 검증 대상 필드는 배열이어야 하며, 지정된 키들이 최소한 반드시 포함되어 있어야 합니다.

<a name="rule-same"></a>
<!-- #### same:_field_ -->
#### same:_field_

<!-- The given _field_ must match the field under validation. -->
지정된 _field_의 값이 유효성 검증 대상 필드의 값과 일치해야 합니다.

<a name="rule-size"></a>
<!-- #### size:_value_ -->
#### size:_value_

<!-- The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples: -->
유효성 검증 대상 필드는 지정한 _value_와 동일한 크기를 가져야 합니다. 문자열의 경우 _value_는 문자 개수를 의미합니다. 숫자 데이터의 경우 _value_는 지정한 정수 값이고(이때 필드는 `numeric` 또는 `integer` 규칙도 적용되어야 합니다), 배열의 경우 크기는 배열의 `count`와 같습니다. 파일의 경우, 크기는 킬로바이트(KB) 단위의 파일 크기입니다. 몇 가지 예시를 보겠습니다.

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
유효성 검증 대상 필드는 지정한 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
<!-- #### string -->
#### string

<!-- The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field. -->
유효성 검증 대상 필드는 문자열이어야 합니다. 이 필드에 `null` 값도 허용하려면 `nullable` 규칙을 같이 지정하십시오.

<a name="rule-timezone"></a>
<!-- #### timezone -->
#### timezone

<!-- The field under validation must be a valid timezone identifier according to the `timezone_identifiers_list` PHP function. -->
유효성 검증 대상 필드는 PHP 함수 `timezone_identifiers_list` 기준으로 올바른 타임존 식별자여야 합니다.

<a name="rule-unique"></a>
<!-- #### unique:_table_,_column_ -->
#### unique:_table_,_column_

<!-- The field under validation must not exist within the given database table. -->
유효성 검증 대상 필드 값은 지정한 데이터베이스 테이블 내에 존재하지 않아야 합니다.

<!-- **Specifying A Custom Table / Column Name:** -->
**커스텀 테이블/컬럼명 지정하기:**

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블명을 직접 입력하는 대신, Eloquent 모델을 지정하여 해당 테이블명을 사용할 수도 있습니다.

```
'email' => 'unique:App\Models\User,email_address'
```

<!-- The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used. -->
`column` 옵션을 사용하여 필드가 데이터베이스에서 매칭되어야 할 컬럼명을 지정할 수 있습니다. 만약 `column` 옵션을 지정하지 않으면, 유효성 검증 대상 필드명이 사용됩니다.

```
'email' => 'unique:users,email_address'
```

<!-- **Specifying A Custom Database Connection** -->
**커스텀 데이터베이스 커넥션 지정**

<!-- Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name: -->
Validator가 수행하는 데이터베이스 쿼리에 커스텀 커넥션을 사용해야 하는 경우, 테이블명 앞에 커넥션명을 붙이면 됩니다.

```
'email' => 'unique:connection.users,email_address'
```

<!-- **Forcing A Unique Rule To Ignore A Given ID:** -->
**특정 ID를 무시하도록 Unique 규칙 강제하기:**

<!-- Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question. -->
경우에 따라 unique 유효성 검증 시 특정 ID를 무시해야 할 때가 있습니다. 예를 들어, "프로필 수정" 화면에서 사용자의 이름, 이메일 주소, 위치 정보를 업데이트할 때, 이메일 주소가 고유한지 확인하되, 이미 본인 이메일이라면 에러가 발생하지 않아야 합니다.

<!-- To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules: -->
이처럼 사용자의 ID를 무시하도록 validator에 지시하려면 `Rule` 클래스를 활용하여 규칙을 유창하게(fluent) 정의할 수 있습니다. 또한, 이 예시에서는 규칙을 배열로 지정하고 각각의 규칙을 `|` 문자 대신 배열 요소로 구분합니다.

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
> `ignore` 메서드에 사용자 입력값을 그대로 넘겨서는 절대 안 됩니다. 반드시 auto-increment ID, Eloquent 모델의 UUID 등 시스템에서 생성한 고유 식별자만 넘겨야 하며, 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해질 수 있습니다.

<!-- Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model: -->
모델의 키 값을 `ignore` 메서드에 직접 넘기는 대신, 전체 모델 인스턴스를 넘길 수도 있습니다. 그러면 Laravel이 자동으로 키 값을 추출합니다.

```
Rule::unique('users')->ignore($user)
```

<!-- If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method: -->
만약 테이블의 기본 키 컬럼명이 `id`가 아니라면, `ignore` 호출 시 두 번째 인자로 해당 컬럼명을 지정할 수 있습니다.

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

<!-- By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method: -->
기본적으로, `unique` 규칙은 유효성 검증을 실행하는 필드명과 동일한 컬럼의 유일성을 체크합니다. 그러나 `unique` 메서드의 두 번째 인자에 다른 컬럼명을 지정할 수도 있습니다.

```
Rule::unique('users', 'email_address')->ignore($user->id),
```

<!-- **Adding Additional Where Clauses:** -->
**추가 where 조건 지정하기:**

<!-- You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`: -->
쿼리에 추가적인 조건을 붙이고 싶을 경우, `where` 메서드를 사용해 쿼리를 커스터마이즈할 수 있습니다. 예를 들어, `account_id` 컬럼이 `1`인 레코드에서만 유일성을 검사하고 싶다면 다음과 같이 작성할 수 있습니다.

```
'email' => Rule::unique('users')->where(fn ($query) => $query->where('account_id', 1))
```

<a name="rule-uppercase"></a>
<!-- #### uppercase -->
#### uppercase

<!-- The field under validation must be uppercase. -->
유효성 검증 대상 필드는 반드시 모두 대문자여야 합니다.

<a name="rule-url"></a>
<!-- #### url -->
#### url

<!-- The field under validation must be a valid URL. -->
유효성 검증 대상 필드는 올바른 URL이어야 합니다.

<a name="rule-ulid"></a>
<!-- #### ulid -->
#### ulid

<!-- The field under validation must be a valid [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID). -->
유효성 검증 대상 필드는 [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) 형식이어야 합니다.

<a name="rule-uuid"></a>
<!-- #### uuid -->
#### uuid

<!-- The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID). -->
유효성 검증 대상 필드는 RFC 4122 (버전 1, 3, 4, 5) 규격의 UUID 형식이어야 합니다.

<a name="conditionally-adding-rules"></a>
<!-- ## Conditionally Adding Rules -->
## Conditionally Adding Rules

<a name="skipping-validation-when-fields-have-certain-values"></a>
<!-- #### Skipping Validation When Fields Have Certain Values -->
#### Skipping Validation When Fields Have Certain Values

<!-- You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`: -->
다른 필드가 특정 값을 갖는 경우, 해당 필드의 유효성 검증을 건너뛰고 싶을 때가 있습니다. 이럴 때는 `exclude_if` 유효성 검증 규칙을 사용할 수 있습니다. 아래 예시에서는 `has_appointment` 필드가 `false`이면 `appointment_date`와 `doctor_name` 필드는 유효성 검증을 하지 않습니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

<!-- Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value: -->
반대로, `exclude_unless` 규칙을 사용해 특정 값이 아닐 경우에만 유효성 검증을 수행하지 않을 수도 있습니다.

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
특정 필드가 데이터에 존재할 때만 유효성 검증을 실행하고 싶을 때가 있습니다. 이럴 때는 규칙에 `sometimes`를 추가하면 간편하게 구현할 수 있습니다.

```
$v = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

<!-- In the example above, the `email` field will only be validated if it is present in the `$data` array. -->
위 예시에서 `email` 필드는 `$data` 배열에 있을 때만 유효성 검증이 작동합니다.

> [!NOTE]
> 항상 존재하지만 비어있을 수 있는 필드에 대해 유효성 검증을 시도하는 경우에는 [this note on optional fields](#a-note-on-optional-fields)를 확인하시기 바랍니다.

<a name="complex-conditional-validation"></a>
<!-- #### Complex Conditional Validation -->
#### Complex Conditional Validation

<!-- Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change: -->
다소 복잡한 조건에 따라 유효성 검증 규칙을 추가하고 싶은 경우가 있습니다. 예를 들어, 어떤 필드는 다른 필드 값이 100 초과일 때만 필수로 만들고 싶거나, 특정 필드가 존재할 때 두 개 이상의 필드에 대해 동일한 값을 요구하고 싶을 수 있습니다. 이러한 조건부 검증도 어렵지 않게 구현할 수 있습니다. 먼저, 항상 고정되어 적용할 _static 규칙_으로 `Validator` 인스턴스를 만듭니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);
```

<!-- Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance. -->
예를 들어, 웹 애플리케이션이 게임 수집가용이고, 사용자가 100개 이상의 게임을 소유한다고 등록할 때는 그 이유도 설명하게 하고 싶다고 가정해봅시다(예: 게임 리셀 샵을 운영하거나, 순수히 수집 자체를 즐기는 경우 등). 이 조건부 필수 항목은 `Validator` 인스턴스의 `sometimes` 메서드를 이용해 쉽게 추가할 수 있습니다.

```
$validator->sometimes('reason', 'required|max:500', function ($input) {
    return $input->games >= 100;
});
```

<!-- The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once: -->
`sometimes` 메서드의 첫 번째 인자는 조건부 검증할 필드명, 두 번째는 추가할 규칙 목록입니다. 세 번째 인자로 전달되는 클로저가 `true`를 반환하면 해당 규칙이 추가됩니다. 이 방식으로 복잡한 조건부 유효성 검증을 매우 쉽게 구현할 수 있습니다. 또한 여러 필드에 한 번에 조건부 검증을 적용할 수도 있습니다.

```
$validator->sometimes(['reason', 'cost'], 'required', function ($input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저로 전달된 `$input` 인자는 `Illuminate\Support\Fluent` 인스턴스로, 검증 중인 입력값 및 파일에 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
<!-- #### Complex Conditional Array Validation -->
#### Complex Conditional Array Validation

<!-- Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated: -->
중첩 배열 내에서, 인덱스를 모르는 또 다른 필드에 따라 특정 필드를 검증하고 싶을 때가 있습니다. 이런 경우에는 클로저에 두 번째 인자로 현재 배열 항목(개별 아이템)이 전달되도록 할 수 있습니다.

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

$validator->sometimes('channels.*.address', 'email', function ($input, $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function ($input, $item) {
    return $item->type !== 'email';
});
```

<!-- Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string. -->
클로저로 전달되는 `$input` 파라미터와 마찬가지로, 배열 데이터일 경우 `$item` 역시 `Illuminate\Support\Fluent` 인스턴스입니다. 배열이 아닌 단일 값일 경우에는 단순 문자열을 받게 됩니다.

<a name="validating-arrays"></a>
<!-- ## Validating Arrays -->
## Validating Arrays

<!-- As discussed in the [`array` validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail: -->
[`array` validation rule documentation](#rule-array)에서 설명한 것처럼, `array` 규칙은 허용되는 배열 키 목록을 받을 수 있습니다. 해당 배열 내에 허용된 키 외의 추가 키가 존재한다면, 유효성 검증은 실패합니다.

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
    'user' => 'array:username,locale',
]);
```

<!-- In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules. -->
일반적으로 배열 내에 포함될 수 있는 키를 항상 명시적으로 지정해야 합니다. 그렇지 않으면 validator의 `validate` 및 `validated` 메서드가 배열과 모든 키(다른 중첩 배열 검증 규칙으로 검증하지 않은 키 포함)까지 검증된 데이터로 반환하게 됩니다.

<a name="validating-nested-array-input"></a>
<!-- ### Validating Nested Array Input -->
### Validating Nested Array Input

<!-- Validating nested array based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so: -->
중첩 배열 기반 폼 입력 필드 유효성 검증도 어렵지 않습니다. 배열 내부 속성을 검증할 때는 "점 표기법(dot notation)"을 사용하면 됩니다. 예를 들어, 요청에 `photos[profile]` 필드가 있다면 다음처럼 검증할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

<!-- You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following: -->
배열의 각 항목도 쉽게 검증할 수 있습니다. 예를 들어, 배열 입력 필드의 각 이메일이 유일한 값이어야 한다면 다음과 같이 작성할 수 있습니다.

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

<!-- Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array based fields: -->
마찬가지로, [custom validation messages in your language files](#custom-messages-for-specific-attributes) 지정 시에도 `*` 문자를 사용할 수 있으므로, 배열 기반 필드에 대해 단일 유효성 메시지를 쉽게 사용할 수 있습니다.

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
어떤 중첩 배열 항목의 값에 따라 유효성 검증 규칙을 지정할 필요가 있을 때가 있습니다. 이럴 때는 `Rule::forEach` 메서드를 사용할 수 있습니다. `forEach` 메서드는 배열 속성의 각 항목마다 실행될 클로저를 받고, 배열 요소의 값과 전체 확장된(fully-expanded) 속성명을 인자로 넘겨줍니다. 클로저는 해당 항목에 할당할 규칙 배열을 반환해야 합니다.

```
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function ($value, $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="error-message-indexes-and-positions"></a>
<!-- ### Error Message Indexes & Positions -->
### Error Message Indexes & Positions

<!-- When validating arrays, you may want to reference the index or position of a particular item that failed validation within the error message displayed by your application. To accomplish this, you may include the `:index` (starts from `0`) and `:position` (starts from `1`) placeholders within your [custom validation message](#manual-customizing-the-error-messages): -->
배열을 검증할 때, 특정 항목의 인덱스나 위치 정보를 에러 메시지에 포함하고 싶을 수 있습니다. 이런 경우 [custom validation message](#manual-customizing-the-error-messages)에서 `:index`(`0`부터 시작)와 `:position`(`1`부터 시작) 플레이스홀더를 사용할 수 있습니다.

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
위 예시에서는 두 번째 항목에서 유효성 검증이 실패하므로, 사용자에게는 _"Please describe photo #2."_라는 오류 메시지가 표시됩니다.

<a name="validating-files"></a>
<!-- ## Validating Files -->
## Validating Files

<!-- Laravel provides a variety of validation rules that may be used to validate uploaded files, such as `mimes`, `image`, `min`, and `max`. While you are free to specify these rules individually when validating files, Laravel also offers a fluent file validation rule builder that you may find convenient: -->
Laravel은 업로드된 파일을 검증하기 위한 다양한 유효성 검증 규칙(`mimes`, `image`, `min`, `max` 등)을 제공합니다. 이러한 규칙을 파일 검증 시 각각 개별적으로 지정할 수도 있지만, Laravel에서는 유창한(fluent) 파일 검증 규칙 빌더도 제공하므로 더욱 편리하게 검증할 수 있습니다.

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
애플리케이션에서 사용자가 이미지를 업로드할 수 있도록 하고 싶다면 `File` 규칙의 `image` 생성자를 사용할 수 있습니다. 더불어, `dimensions` 규칙을 함께 적용해 이미지의 크기도 제한할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;
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
> 이미지 크기 검증에 대한 더욱 자세한 정보는 [dimension rule documentation](#rule-dimensions)를 참고하세요.

<a name="validating-files-file-types"></a>
<!-- #### File Types -->
#### File Types

<!-- Even though you only need to specify the extensions when invoking the `types` method, this method actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
`types` 메서드를 사용할 때에는 확장자만 지정하면 되지만, 실제로는 해당 파일의 내용을 읽어서 MIME 타입을 유추하고 파일의 MIME 타입을 검사합니다. 전체 MIME 타입과 그에 대응하는 확장자 목록은 아래에서 확인할 수 있습니다.

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-passwords"></a>
<!-- ## Validating Passwords -->
## Validating Passwords

<!-- To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object: -->
비밀번호의 복잡도가 충분하도록 검사하려면 Laravel의 `Password` 규칙 객체를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

<!-- The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing: -->
`Password` 규칙 객체는 비밀번호의 최소 길이, 문자, 숫자, 기호, 대소문자 조합과 같은 복잡도 조건을 매우 자유롭게 커스터마이즈할 수 있습니다.

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
또한, 입력된 비밀번호가 이미 공공 데이터 유출 등에서 유출된 적이 없는지 `uncompromised` 메서드로 검증할 수도 있습니다.

```
Password::min(8)->uncompromised()
```

<!-- Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security. -->
내부적으로 `Password` 규칙 객체는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 모델을 사용해서 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 활용하되, 사용자의 프라이버시와 보안을 해치지 않습니다.

<!-- By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method: -->
기본적으로 데이터 유출 내에서 1회라도 발견된 비밀번호는 compromised로 간주하지만, 유출 허용 횟수를 `uncompromised` 메서드의 첫 번째 파라미터로 수정할 수도 있습니다.

```
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

<!-- Of course, you may chain all the methods in the examples above: -->
물론 위 예시의 여러 메서드를 모두 체이닝해서 사용할 수도 있습니다.

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
애플리케이션에서 비밀번호 유효성 검증 기본 규칙을 한 곳에 공통적으로 정의하면 편리할 수 있습니다. `Password::defaults` 메서드를 사용하면 손쉽게 설정할 수 있으며, 이 `defaults` 메서드에는 기본 규칙을 반환하는 클로저를 전달하면 됩니다. 일반적으로 `defaults` 규칙은 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다.

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
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
이후 비밀번호 검증 시 기본 규칙을 적용하려면, 별도의 인자 없이 `defaults` 메서드를 호출하면 됩니다.

```
'password' => ['required', Password::defaults()],
```

<!-- Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this: -->
경우에 따라 기본 비밀번호 규칙에 추가 검증 조건을 붙이고 싶을 수도 있습니다. 이럴 땐 `rules` 메서드를 사용할 수 있습니다.

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
Laravel은 다양한 기본 유효성 규칙을 제공하지만, 직접 커스텀 규칙을 만들어 사용하고 싶을 수도 있습니다. 커스텀 유효성 규칙 등록 방법 중 하나는 규칙 객체(rule object)를 이용하는 것입니다. 새 규칙 객체를 생성하려면 `make:rule` 아티즌 명령어를 사용합니다. 아래 예시처럼 문자열이 모두 대문자인지 확인하는 규칙을 만들어 보겠습니다. Laravel은 새 규칙 클래스를 `app/Rules` 디렉토리에 생성하며, 이 디렉토리가 없을 경우 명령어 실행 시 자동으로 만듭니다.

```shell
php artisan make:rule Uppercase --invokable
```

<!-- Once the rule has been created, we are ready to define its behavior. A rule object contains a single method: `__invoke`. This method receives the attribute name, its value, and a callback that should be invoked on failure with the validation error message: -->
규칙이 생성되었으면, 이제 동작을 정의해봅니다. 규칙 객체는 하나의 메서드 `__invoke`만을 포함하며, 이 메서드는 속성명, 값, 검증 실패 시 호출할 콜백(에러 메시지)을 받습니다.

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\InvokableRule;

class Uppercase implements InvokableRule
{
    /**
     * Run the validation rule.
     *
     * @param  string  $attribute
     * @param  mixed  $value
     * @param  \Closure  $fail
     * @return void
     */
    public function __invoke($attribute, $value, $fail)
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

<!-- Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules: -->
이제, 정의한 규칙 객체 인스턴스를 다른 유효성 규칙과 함께 validator에 전달하여 사용할 수 있습니다.

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

<!-- #### Translating Validation Messages -->
#### Translating Validation Messages

<!-- Instead of providing a literal error message to the `$fail` closure, you may also provide a [translation string key](/docs/9.x/localization) and instruct Laravel to translate the error message: -->
`$fail` 클로저에 직접 오류 메시지를 전달하는 대신, [translation string key](/docs/9.x/localization)를 지정하여 Laravel이 해당 오류 메시지를 번역하도록 할 수 있습니다.

```
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

<!-- If necessary, you may provide placeholder replacements and the preferred language as the first and second arguments to the `translate` method: -->
필요하다면, `translate` 메서드의 첫 번째와 두 번째 인수로 각각 플레이스홀더 치환 값과 원하는 언어를 전달할 수 있습니다.

```
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr')
```

<!-- #### Accessing Additional Data -->
#### Accessing Additional Data

<!-- If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation: -->
커스텀 유효성 검사 규칙 클래스에서 검증 대상이 되는 모든 데이터를 접근해야 한다면, 해당 클래스에서 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스는 클래스에 `setData` 메서드 정의를 요구합니다. Laravel은 유효성 검사 전에 자동으로 이 메서드를 호출하여, 검증 대상이 되는 모든 데이터를 전달합니다.

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\InvokableRule;

class Uppercase implements DataAwareRule, InvokableRule
{
    /**
     * All of the data under validation.
     *
     * @var array
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array  $data
     * @return $this
     */
    public function setData($data)
    {
        $this->data = $data;

        return $this;
    }
}
```

<!-- Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface: -->
또한 유효성 검사를 수행하는 validator 인스턴스에 접근이 필요한 경우, `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\InvokableRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;

class Uppercase implements InvokableRule, ValidatorAwareRule
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
     *
     * @param  \Illuminate\Validation\Validator  $validator
     * @return $this
     */
    public function setValidator($validator)
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
애플리케이션에서 단 한 번만 사용할 커스텀 규칙이라면, 규칙 객체 대신 클로저를 사용할 수 있습니다. 이 클로저는 속성의 이름, 속성 값, 그리고 검증 실패 시 호출해야 하는 `$fail` 콜백을 인수로 받습니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function ($attribute, $value, $fail) {
            if ($value === 'foo') {
                $fail('The '.$attribute.' is invalid.');
            }
        },
    ],
]);
```

<a name="implicit-rules"></a>
<!-- ### Implicit Rules -->
### Implicit Rules

<!-- By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the [`unique`](#rule-unique) rule will not be run against an empty string: -->
기본적으로, 검증 대상 속성이 존재하지 않거나 빈 문자열인 경우 일반 유효성 검사 규칙은커녕, 커스텀 규칙조차 실행되지 않습니다. 예를 들어, [`unique`](#rule-unique) 규칙은 빈 문자열에 대해서는 실행되지 않습니다.

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

<!-- For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To quickly generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option: -->
빈 값이더라도 커스텀 규칙이 반드시 실행되도록 하려면, 해당 규칙이 속성이 필수임을 _암묵적으로_ 지정해야 합니다. 새로운 암묵적 규칙 객체를 빠르게 생성하기 위해서는, `--implicit` 옵션을 사용하여 `make:rule` 아티즌 명령어를 실행합니다.

```shell
php artisan make:rule Uppercase --invokable --implicit
```

> [!WARNING]
> "암묵적(implicit)" 규칙이란, 해당 속성이 필수임을 _암시_ 한다는 의미일 뿐입니다. 실제로 값이 없거나 비어 있을 때 검증에 실패 처리할지는 개발자가 규칙 클래스에서 직접 정의해야 합니다.
