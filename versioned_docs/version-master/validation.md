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
Laravel은 애플리케이션으로 들어오는 데이터를 유효성 검증하기 위한 여러 가지 방법을 제공합니다. 가장 일반적으로는 들어오는 모든 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 사용합니다. 하지만 이 문서에서는 유효성 검증을 수행하는 다른 방법도 함께 살펴보겠습니다.

<!-- Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features. -->
Laravel에는 데이터에 적용할 수 있는 편리한 유효성 검증 규칙이 다양하게 포함되어 있으며, 특정 데이터베이스 테이블에서 값이 고유한지 검증하는 기능도 제공합니다. Laravel의 모든 유효성 검증 기능을 익힐 수 있도록 이러한 유효성 검증 규칙을 하나씩 자세히 다루겠습니다.

<a name="validation-quickstart"></a>
<!-- ## Validation Quickstart -->
## Validation Quickstart

<!-- To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel: -->
Laravel의 강력한 유효성 검증 기능을 알아보기 위해, 폼을 유효성 검증하고 오류 메시지를 사용자에게 다시 표시하는 전체 예제를 살펴보겠습니다. 이 개요를 읽으면 Laravel을 사용해 들어오는 요청 데이터를 유효성 검증하는 방법을 전반적으로 이해할 수 있습니다.

<a name="quick-defining-the-routes"></a>
<!-- ### Defining the Routes -->
### Defining the Routes

<!-- First, let's assume we have the following routes defined in our `routes/web.php` file: -->
먼저 `routes/web.php` 파일에 다음 라우트가 정의되어 있다고 가정하겠습니다.

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

<!-- The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database. -->
`GET` 라우트는 사용자가 새 블로그 게시물을 작성할 수 있는 폼을 표시하고, `POST` 라우트는 새 블로그 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
<!-- ### Creating the Controller -->
### Creating the Controller

<!-- Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now: -->
다음으로 이 라우트로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 지금은 `store` 메서드를 비워 두겠습니다.

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
<!-- ### Writing the Validation Logic -->
### Writing the Validation Logic

<!-- Now we are ready to fill in our `store` method with the logic to validate the new blog post. To do this, we will use the `validate` method provided by the `Illuminate\Http\Request` object. If the validation rules pass, your code will keep executing normally; however, if validation fails, an `Illuminate\Validation\ValidationException` exception will be thrown and the proper error response will automatically be sent back to the user. -->
이제 새 블로그 게시물을 유효성 검증하는 로직으로 `store` 메서드를 채울 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용합니다. 유효성 검증 규칙을 통과하면 코드는 정상적으로 계속 실행됩니다. 하지만 유효성 검증에 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고, 적절한 오류 응답이 사용자에게 자동으로 다시 전송됩니다.

<!-- If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a [JSON response containing the validation error messages](#validation-error-response-format) will be returned. -->
전통적인 HTTP 요청 중에 유효성 검증이 실패하면 이전 URL로 리다이렉트 응답이 생성됩니다. 들어오는 요청이 XHR 요청이라면 [JSON response containing the validation error messages](#validation-error-response-format)이 반환됩니다.

<!-- To get a better understanding of the `validate` method, let's jump back into the `store` method: -->
`validate` 메서드를 더 잘 이해하기 위해 다시 `store` 메서드로 돌아가 보겠습니다.

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

<!-- As you can see, the validation rules are passed into the `validate` method. Don't worry - all available validation rules are [documented](#available-validation-rules). Again, if the validation fails, the proper response will automatically be generated. If the validation passes, our controller will continue executing normally. -->
보시다시피 유효성 검증 규칙은 `validate` 메서드에 전달됩니다. 걱정하지 마십시오. 사용 가능한 모든 유효성 검증 규칙은 [documented](#available-validation-rules). 다시 말해 유효성 검증에 실패하면 적절한 응답이 자동으로 생성됩니다. 유효성 검증을 통과하면 컨트롤러는 정상적으로 계속 실행됩니다.

<!-- Alternatively, validation rules may be specified as arrays of rules instead of a single `|` delimited string: -->
또는 유효성 검증 규칙을 하나의 `|` 구분 문자열 대신 규칙 배열로 지정할 수도 있습니다.

```php
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<!-- In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a [named error bag](#named-error-bags): -->
또한 `validateWithBag` 메서드를 사용하여 요청을 유효성 검증하고, 오류 메시지를 [named error bag](#named-error-bags)에 저장할 수 있습니다.

```php
$validatedData = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
<!-- #### Stopping on First Validation Failure -->
#### Stopping on First Validation Failure

<!-- Sometimes you may wish to stop running validation rules on an attribute after the first validation failure. To do so, assign the `bail` rule to the attribute: -->
때로는 어떤 속성에서 첫 번째 유효성 검증 실패가 발생한 뒤 해당 속성에 대한 나머지 유효성 검증 규칙 실행을 중단하고 싶을 수 있습니다. 그렇게 하려면 해당 속성에 `bail` 규칙을 지정합니다.

```php
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

<!-- In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned. -->
이 예제에서 `title` 속성의 `unique` 규칙이 실패하면 `max` 규칙은 검사되지 않습니다. 규칙은 지정된 순서대로 유효성 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
<!-- #### A Note on Nested Attributes -->
#### A Note on Nested Attributes

<!-- If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax: -->
들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있다면, "점" 문법을 사용하여 유효성 검증 규칙에서 이러한 필드를 지정할 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

<!-- On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash: -->
반대로 필드 이름에 실제 마침표가 포함되어 있다면, 마침표를 백슬래시로 이스케이프하여 이것이 "점" 문법으로 해석되지 않도록 명시적으로 막을 수 있습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
<!-- ### Displaying the Validation Errors -->
### Displaying the Validation Errors

<!-- So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/master/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/master/session#flash-data). -->
그렇다면 들어오는 요청 필드가 주어진 유효성 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞서 언급했듯이 Laravel은 사용자를 이전 위치로 자동 리다이렉트합니다. 또한 모든 유효성 검증 오류와 [request input](/docs/master/requests#retrieving-old-input)이 자동으로 [flashed to the session](/docs/master/session#flash-data).

<!-- An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages). -->
`$errors` 변수는 `web` 미들웨어 그룹에서 제공하는 `Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어에 의해 애플리케이션의 모든 뷰와 공유됩니다. 이 미들웨어가 적용되면 `$errors` 변수는 항상 뷰에서 사용할 수 있으므로, `$errors` 변수가 항상 정의되어 있으며 안전하게 사용할 수 있다고 편리하게 가정할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag` 인스턴스입니다. 이 객체를 다루는 방법에 대한 자세한 내용은 [check out its documentation](#working-with-error-messages)를 확인하십시오.

<!-- So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view: -->
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
<!-- #### Customizing the Error Messages -->
#### Customizing the Error Messages

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command. -->
Laravel의 내장 유효성 검증 규칙에는 각각 애플리케이션의 `lang/en/validation.php` 파일에 위치한 오류 메시지가 있습니다. 애플리케이션에 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어를 사용하여 Laravel이 해당 디렉터리를 생성하도록 지시할 수 있습니다.

<!-- Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이러한 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

<!-- In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/master/localization). -->
또한 이 파일을 다른 언어 디렉터리로 복사하여 애플리케이션의 언어에 맞게 메시지를 번역할 수 있습니다. Laravel 현지화에 대해 더 알아보려면 전체 [localization documentation](/docs/master/localization)를 확인하십시오.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="quick-xhr-requests-and-validation"></a>
<!-- #### XHR Requests and Validation -->
#### XHR Requests and Validation

<!-- In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a [JSON response containing all of the validation errors](#validation-error-response-format). This JSON response will be sent with a 422 HTTP status code. -->
이 예제에서는 전통적인 폼을 사용하여 애플리케이션에 데이터를 전송했습니다. 하지만 많은 애플리케이션은 JavaScript 기반 프런트엔드에서 XHR 요청을 받습니다. XHR 요청 중에 `validate` 메서드를 사용하면 Laravel은 리다이렉트 응답을 생성하지 않습니다. 대신 Laravel은 [JSON response containing all of the validation errors](#validation-error-response-format)을 생성합니다. 이 JSON 응답은 422 HTTP 상태 코드와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
<!-- #### The `@error` Directive -->
#### The `@error` Directive

<!-- You may use the `@error` [Blade](/docs/master/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
`@error` [Blade](/docs/master/blade) 지시어를 사용하면 특정 속성에 대한 유효성 검증 오류 메시지가 있는지 빠르게 확인할 수 있습니다. `@error` 지시어 안에서는 `$message` 변수를 출력하여 오류 메시지를 표시할 수 있습니다.

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

<!-- If you are using [named error bags](#named-error-bags), you may pass the name of the error bag as the second argument to the `@error` directive: -->
[named error bags](#named-error-bags)을 사용하고 있다면, `@error` 지시어의 두 번째 인수로 오류 백의 이름을 전달할 수 있습니다.

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
<!-- ### Repopulating Forms -->
### Repopulating Forms

<!-- When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/master/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit. -->
Laravel이 유효성 검증 오류 때문에 리다이렉트 응답을 생성하면, 프레임워크는 자동으로 [flash all of the request's input to the session](/docs/master/session#flash-data). 이렇게 하는 이유는 다음 요청에서 해당 입력에 편리하게 접근하여 사용자가 제출하려고 했던 폼을 다시 채울 수 있도록 하기 위해서입니다.

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/master/session): -->
이전 요청에서 플래시된 입력을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다. `old` 메서드는 이전에 플래시된 입력 데이터를 [session](/docs/master/session)에서 가져옵니다.

```php
$title = $request->old('title');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/master/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade template](/docs/master/blade) 안에서 이전 입력을 표시하는 경우, `old` 헬퍼를 사용하면 폼을 더 편리하게 다시 채울 수 있습니다. 주어진 필드에 대한 이전 입력이 없으면 `null`이 반환됩니다.

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
<!-- ### A Note on Optional Fields -->
### A Note on Optional Fields

<!-- By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example: -->
기본적으로 Laravel은 애플리케이션의 전역 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 때문에 `null` 값을 유효하지 않은 값으로 간주하지 않도록 하려면 "선택 사항" 요청 필드를 `nullable`로 표시해야 하는 경우가 많습니다. 예를 들면 다음과 같습니다.

```php
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

<!-- In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date. -->
이 예제에서는 `publish_at` 필드가 `null`이거나 유효한 날짜 표현일 수 있다고 지정하고 있습니다. 규칙 정의에 `nullable` 수정자를 추가하지 않으면 Validator는 `null`을 유효하지 않은 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
<!-- ### Validation Error Response Format -->
### Validation Error Response Format

<!-- When your application throws a `Illuminate\Validation\ValidationException` exception and the incoming HTTP request is expecting a JSON response, Laravel will automatically format the error messages for you and return a `422 Unprocessable Entity` HTTP response. -->
애플리케이션에서 `Illuminate\Validation\ValidationException` 예외가 발생하고 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 오류 메시지를 자동으로 형식화하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

<!-- Below, you can review an example of the JSON response format for validation errors. Note that nested error keys are flattened into "dot" notation format: -->
아래에서 유효성 검증 오류에 대한 JSON 응답 형식 예제를 확인할 수 있습니다. 중첩된 오류 키는 "점" 표기법 형식으로 평탄화된다는 점에 유의하십시오.

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
더 복잡한 유효성 검증 시나리오에서는 "폼 요청"을 만들고 싶을 수 있습니다. 폼 요청은 자체 유효성 검증 로직과 인가 로직을 캡슐화하는 사용자 정의 요청 클래스입니다. 폼 요청 클래스를 생성하려면 `make:request` Artisan CLI 명령어를 사용할 수 있습니다.

```shell
php artisan make:request StorePostRequest
```

<!-- The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`. -->
생성된 폼 요청 클래스는 `app/Http/Requests` 디렉터리에 배치됩니다. 이 디렉터리가 존재하지 않으면 `make:request` 명령어를 실행할 때 생성됩니다. Laravel이 생성하는 각 폼 요청에는 `authorize`와 `rules` 두 메서드가 있습니다.

<!-- As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data: -->
짐작했듯이 `authorize` 메서드는 현재 인증된 사용자가 해당 요청이 나타내는 동작을 수행할 수 있는지 판단하는 역할을 하며, `rules` 메서드는 요청 데이터에 적용할 유효성 검증 규칙을 반환합니다.

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
> `rules` 메서드의 시그니처 안에서 필요한 의존성을 타입 힌트할 수 있습니다. 해당 의존성은 Laravel [service container](/docs/master/container)를 통해 자동으로 해결됩니다.

<!-- So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic: -->
그렇다면 유효성 검증 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 해당 요청을 타입 힌트하기만 하면 됩니다. 들어오는 폼 요청은 컨트롤러 메서드가 호출되기 전에 유효성 검증되므로, 컨트롤러에 유효성 검증 로직을 복잡하게 넣을 필요가 없습니다.

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

<!-- If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a [JSON representation of the validation errors](#validation-error-response-format). -->
유효성 검증에 실패하면 사용자를 이전 위치로 돌려보내기 위한 리다이렉트 응답이 생성됩니다. 오류도 세션에 플래시되어 표시할 수 있게 됩니다. 요청이 XHR 요청이었다면, [JSON representation of the validation errors](#validation-error-response-format)을 포함한 422 상태 코드의 HTTP 응답이 사용자에게 반환됩니다.

> [!NOTE]
> Inertia 기반 Laravel 프런트엔드에 실시간 폼 요청 유효성 검증을 추가해야 하나요? [Laravel Precognition](/docs/master/precognition)을 확인하십시오.

<a name="performing-additional-validation-on-form-requests"></a>
<!-- #### Performing Additional Validation -->
#### Performing Additional Validation

<!-- Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the form request's `after` method. -->
초기 유효성 검증이 완료된 뒤 추가 유효성 검증을 수행해야 할 때가 있습니다. 이는 폼 요청의 `after` 메서드를 사용하여 처리할 수 있습니다.

<!-- The `after` method should return an array of callables or closures which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary: -->
`after` 메서드는 유효성 검증이 완료된 뒤 호출될 호출 가능 항목 또는 클로저의 배열을 반환해야 합니다. 전달된 호출 가능 항목은 `Illuminate\Validation\Validator` 인스턴스를 받으므로, 필요한 경우 추가 오류 메시지를 발생시킬 수 있습니다.

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
<!-- As noted, the array returned by the `after` method may also contain invokable classes. The `__invoke` method of these classes will receive an `Illuminate\Validation\Validator` instance: -->
앞서 언급했듯이, `after` 메서드가 반환하는 배열에는 호출 가능한 클래스도 포함될 수 있습니다. 이러한 클래스의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받습니다.

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

<!-- By adding the `StopOnFirstFailure` attribute to your request class, you may inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
요청 클래스에 `StopOnFirstFailure` 속성을 추가하면, 단 하나의 유효성 검증 실패가 발생하는 즉시 모든 속성에 대한 검증을 중단해야 한다고 validator에 알릴 수 있습니다.

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

<a name="customizing-the-redirect-location"></a>
<!-- #### Customizing the Redirect Location -->
#### Customizing the Redirect Location

<!-- When form request validation fails, a redirect response will be generated to send the user back to their previous location. However, you are free to customize this behavior. To do so, you may use the `RedirectTo` attribute on your form request: -->
폼 요청 유효성 검증에 실패하면, 사용자를 이전 위치로 되돌려 보내기 위한 리다이렉트 응답이 생성됩니다. 하지만 이 동작은 자유롭게 커스터마이징할 수 있습니다. 이를 위해 폼 요청에서 `RedirectTo` 속성을 사용할 수 있습니다.

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

<!-- Or, if you would like to redirect users to a named route, you may use the `RedirectToRoute` attribute instead: -->
또는 사용자를 이름이 지정된 라우트로 리다이렉트하려면, 대신 `RedirectToRoute` 속성을 사용할 수 있습니다.

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
<!-- #### Customizing the Error Bag -->
#### Customizing the Error Bag

<!-- When form request validation fails, the errors are flashed to the `default` error bag. If you need to store the errors in a different [named error bag](#named-error-bags), you may use the `ErrorBag` attribute on your form request: -->
폼 요청 유효성 검증에 실패하면, 에러는 `default` 에러 백에 플래시됩니다. 에러를 다른 [named error bag](#named-error-bags)에 저장해야 한다면, 폼 요청에서 `ErrorBag` 속성을 사용할 수 있습니다.

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
<!-- ### Authorizing Form Requests -->
### Authorizing Form Requests

<!-- The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/master/authorization) within this method: -->
폼 요청 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 안에서 인증된 사용자가 특정 리소스를 업데이트할 권한이 실제로 있는지 판단할 수 있습니다. 예를 들어, 사용자가 업데이트하려는 블로그 댓글을 실제로 소유하고 있는지 확인할 수 있습니다. 대부분의 경우 이 메서드 안에서 [authorization gates and policies](/docs/master/authorization)을 사용하게 됩니다.

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

<!-- Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also, note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below: -->
모든 폼 요청은 기본 Laravel 요청 클래스를 확장하므로, `user` 메서드를 사용해 현재 인증된 사용자에 접근할 수 있습니다. 또한 위 예제에서 `route` 메서드를 호출한 부분도 주목하세요. 이 메서드를 사용하면 아래 예제의 `{comment}` 매개변수처럼 호출된 라우트에 정의된 URI 매개변수에 접근할 수 있습니다.

```php
Route::post('/comment/{comment}');
```

<!-- Therefore, if your application is taking advantage of [route model binding](/docs/master/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request: -->
따라서 애플리케이션에서 [route model binding](/docs/master/routing#route-model-binding)을 활용하고 있다면, 해결된 모델을 요청의 속성으로 접근하여 코드를 더 간결하게 만들 수 있습니다.

```php
return $this->user()->can('update', $this->comment);
```

<!-- If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute. -->
`authorize` 메서드가 `false`를 반환하면, 403 상태 코드가 포함된 HTTP 응답이 자동으로 반환되며 컨트롤러 메서드는 실행되지 않습니다.

<!-- If you plan to handle authorization logic for the request in another part of your application, you may remove the `authorize` method completely, or simply return `true`: -->
요청에 대한 인가 로직을 애플리케이션의 다른 부분에서 처리할 계획이라면, `authorize` 메서드를 완전히 제거하거나 단순히 `true`를 반환할 수 있습니다.

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
> `authorize` 메서드의 시그니처에는 필요한 모든 의존성을 타입 힌트할 수 있습니다. 해당 의존성은 Laravel [service container](/docs/master/container)를 통해 자동으로 해결됩니다.

<a name="customizing-the-error-messages"></a>
<!-- ### Customizing the Error Messages -->
### Customizing the Error Messages

<!-- You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages: -->
`messages` 메서드를 오버라이드하여 폼 요청에서 사용하는 에러 메시지를 커스터마이징할 수 있습니다. 이 메서드는 속성 / 규칙 쌍과 그에 해당하는 에러 메시지의 배열을 반환해야 합니다.

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
<!-- #### Customizing the Validation Attributes -->
#### Customizing the Validation Attributes

<!-- Many of Laravel's built-in validation rule error messages contain an `:attribute` placeholder. If you would like the `:attribute` placeholder of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs: -->
Laravel에 내장된 많은 유효성 검증 규칙 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있습니다. 유효성 검증 메시지의 `:attribute` 플레이스홀더를 커스텀 속성 이름으로 바꾸고 싶다면, `attributes` 메서드를 오버라이드하여 커스텀 이름을 지정할 수 있습니다. 이 메서드는 속성 / 이름 쌍의 배열을 반환해야 합니다.

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
<!-- ### Preparing Input for Validation -->
### Preparing Input for Validation

<!-- If you need to prepare or sanitize any data from the request before you apply your validation rules, you may use the `prepareForValidation` method: -->
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

<!-- Likewise, if you need to normalize any request data after validation is complete, you may use the `passedValidation` method: -->
마찬가지로 유효성 검증이 완료된 후 요청 데이터를 정규화해야 한다면, `passedValidation` 메서드를 사용할 수 있습니다.

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
<!-- ## Manually Creating Validators -->
## Manually Creating Validators

<!-- If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/master/facades). The `make` method on the facade generates a new validator instance: -->
요청에서 `validate` 메서드를 사용하고 싶지 않다면, `Validator` [facade](/docs/master/facades)를 사용해 validator 인스턴스를 수동으로 생성할 수 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 생성합니다.

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

<!-- The first argument passed to the `make` method is the data under validation. The second argument is an array of the validation rules that should be applied to the data. -->
`make` 메서드에 전달되는 첫 번째 인수는 유효성 검증 대상 데이터입니다. 두 번째 인수는 데이터에 적용할 유효성 검증 규칙 배열입니다.

<!-- After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`. -->
요청 유효성 검증이 실패했는지 판단한 후에는 `withErrors` 메서드를 사용해 에러 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용하면 리다이렉션 후 `$errors` 변수가 자동으로 뷰와 공유되므로, 사용자에게 에러를 쉽게 표시할 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP `array`를 받을 수 있습니다.

<!-- #### Stopping on First Validation Failure -->
#### Stopping on First Validation Failure

<!-- The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`stopOnFirstFailure` 메서드는 단 하나의 유효성 검증 실패가 발생하는 즉시 모든 속성에 대한 검증을 중단해야 한다고 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
<!-- ### Automatic Redirection -->
### Automatic Redirection

<!-- If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a [JSON response will be returned](#validation-error-response-format): -->
validator 인스턴스를 수동으로 생성하되 HTTP 요청의 `validate` 메서드가 제공하는 자동 리다이렉션도 활용하고 싶다면, 기존 validator 인스턴스에서 `validate` 메서드를 호출할 수 있습니다. 유효성 검증에 실패하면 사용자는 자동으로 리다이렉트되며, XHR 요청인 경우 [JSON response will be returned](#validation-error-response-format).

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

<!-- You may use the `validateWithBag` method to store the error messages in a [named error bag](#named-error-bags) if validation fails: -->
유효성 검증에 실패했을 때 에러 메시지를 [named error bag](#named-error-bags)에 저장하려면 `validateWithBag` 메서드를 사용할 수 있습니다.

```php
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
<!-- ### Named Error Bags -->
### Named Error Bags

<!-- If you have multiple forms on a single page, you may wish to name the `MessageBag` containing the validation errors, allowing you to retrieve the error messages for a specific form. To achieve this, pass a name as the second argument to `withErrors`: -->
하나의 페이지에 여러 폼이 있다면, 특정 폼의 에러 메시지만 가져올 수 있도록 유효성 검증 에러를 담고 있는 `MessageBag`에 이름을 지정하고 싶을 수 있습니다. 이를 위해 `withErrors`의 두 번째 인수로 이름을 전달하세요.

```php
return redirect('/register')->withErrors($validator, 'login');
```

<!-- You may then access the named `MessageBag` instance from the `$errors` variable: -->
그런 다음 `$errors` 변수에서 이름이 지정된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
<!-- ### Customizing the Error Messages -->
### Customizing the Error Messages

<!-- If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method: -->
필요하다면 Laravel이 제공하는 기본 에러 메시지 대신 validator 인스턴스가 사용할 커스텀 에러 메시지를 제공할 수 있습니다. 커스텀 메시지를 지정하는 방법은 여러 가지가 있습니다. 먼저, 커스텀 메시지를 `Validator::make` 메서드의 세 번째 인수로 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

<!-- In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example: -->
이 예제에서 `:attribute` 플레이스홀더는 유효성 검증 대상 필드의 실제 이름으로 대체됩니다. 유효성 검증 메시지에서 다른 플레이스홀더도 활용할 수 있습니다. 예를 들면 다음과 같습니다.

```php
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
때로는 특정 속성에 대해서만 커스텀 에러 메시지를 지정하고 싶을 수 있습니다. 이 경우 "dot" 표기법을 사용할 수 있습니다. 먼저 속성 이름을 지정한 다음 규칙을 지정하세요.

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
<!-- #### Specifying Custom Attribute Values -->
#### Specifying Custom Attribute Values

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method: -->
Laravel에 내장된 많은 에러 메시지에는 `:attribute` 플레이스홀더가 포함되어 있으며, 이 플레이스홀더는 유효성 검증 대상 필드 또는 속성의 이름으로 대체됩니다. 특정 필드에서 이 플레이스홀더를 대체하는 데 사용할 값을 커스터마이징하려면, `Validator::make` 메서드의 네 번째 인수로 커스텀 속성 배열을 전달할 수 있습니다.

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
<!-- ### Performing Additional Validation -->
### Performing Additional Validation

<!-- Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the validator's `after` method. The `after` method accepts a closure or an array of callables which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary: -->
초기 유효성 검증이 완료된 후 추가 유효성 검증을 수행해야 할 때가 있습니다. 이는 validator의 `after` 메서드를 사용해 처리할 수 있습니다. `after` 메서드는 유효성 검증이 완료된 후 호출될 클로저 또는 호출 가능한 항목의 배열을 받습니다. 전달된 호출 가능한 항목은 `Illuminate\Validation\Validator` 인스턴스를 받으므로, 필요한 경우 추가 에러 메시지를 발생시킬 수 있습니다.

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

<!-- As noted, the `after` method also accepts an array of callables, which is particularly convenient if your "after validation" logic is encapsulated in invokable classes, which will receive an `Illuminate\Validation\Validator` instance via their `__invoke` method: -->
앞서 언급했듯이, `after` 메서드는 호출 가능한 항목의 배열도 받을 수 있습니다. 이는 "after validation" 로직이 호출 가능한 클래스에 캡슐화되어 있을 때 특히 편리합니다. 이 클래스들은 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받습니다.

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
폼 요청 또는 수동으로 생성한 validator 인스턴스를 사용해 들어오는 요청 데이터를 검증한 후에는, 실제로 유효성 검증을 거친 요청 데이터를 가져오고 싶을 수 있습니다. 이를 수행하는 방법은 여러 가지가 있습니다. 먼저, 폼 요청 또는 validator 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 유효성 검증된 데이터의 배열을 반환합니다.
```php
$validated = $request->validated();

$validated = $validator->validated();
```

<!-- Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data: -->
또는 폼 요청이나 validator 인스턴스에서 `safe` 메서드를 호출할 수 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체는 유효성 검증된 데이터의 일부 또는 전체 배열을 가져올 수 있도록 `only`, `except`, `all` 메서드를 제공합니다.

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

<!-- In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array: -->
또한 `Illuminate\Support\ValidatedInput` 인스턴스는 반복할 수 있으며 배열처럼 접근할 수도 있습니다.

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

<!-- If you would like to add additional fields to the validated data, you may call the `merge` method: -->
유효성 검증된 데이터에 추가 필드를 더하고 싶다면 `merge` 메서드를 호출할 수 있습니다.

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

<!-- If you would like to retrieve the validated data as a [collection](/docs/master/collections) instance, you may call the `collect` method: -->
유효성 검증된 데이터를 [collection](/docs/master/collections) 인스턴스로 가져오고 싶다면 `collect` 메서드를 호출할 수 있습니다.

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
<!-- ## Working With Error Messages -->
## Working With Error Messages

<!-- After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class. -->
`Validator` 인스턴스에서 `errors` 메서드를 호출하면 `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. 이 인스턴스는 오류 메시지를 다루기 위한 여러 편리한 메서드를 제공합니다. 모든 뷰에서 자동으로 사용할 수 있는 `$errors` 변수도 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
<!-- #### Retrieving the First Error Message for a Field -->
#### Retrieving the First Error Message for a Field

<!-- To retrieve the first error message for a given field, use the `first` method: -->
특정 필드의 첫 번째 오류 메시지를 가져오려면 `first` 메서드를 사용합니다.

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
<!-- #### Retrieving All Error Messages for a Field -->
#### Retrieving All Error Messages for a Field

<!-- If you need to retrieve an array of all the messages for a given field, use the `get` method: -->
특정 필드에 대한 모든 메시지 배열을 가져와야 한다면 `get` 메서드를 사용합니다.

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

<!-- If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character: -->
배열 폼 필드를 유효성 검증하는 경우, `*` 문자를 사용하여 배열의 각 요소에 대한 모든 메시지를 가져올 수 있습니다.

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
<!-- #### Retrieving All Error Messages for All Fields -->
#### Retrieving All Error Messages for All Fields

<!-- To retrieve an array of all messages for all fields, use the `all` method: -->
모든 필드에 대한 모든 메시지 배열을 가져오려면 `all` 메서드를 사용합니다.

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
<!-- #### Determining if Messages Exist for a Field -->
#### Determining if Messages Exist for a Field

<!-- The `has` method may be used to determine if any error messages exist for a given field: -->
`has` 메서드를 사용하여 특정 필드에 오류 메시지가 있는지 확인할 수 있습니다.

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
<!-- ### Specifying Custom Messages in Language Files -->
### Specifying Custom Messages in Language Files

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command. -->
Laravel의 내장 유효성 검증 규칙은 각각 애플리케이션의 `lang/en/validation.php` 파일에 위치한 오류 메시지를 가지고 있습니다. 애플리케이션에 `lang` 디렉터리가 없다면 `lang:publish` Artisan 명령어를 사용하여 Laravel이 해당 디렉터리를 생성하도록 지시할 수 있습니다.

<!-- Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
`lang/en/validation.php` 파일 안에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 애플리케이션의 필요에 따라 이 메시지를 자유롭게 변경하거나 수정할 수 있습니다.

<!-- In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/master/localization). -->
또한 이 파일을 다른 언어 디렉터리로 복사하여 애플리케이션 언어에 맞게 메시지를 번역할 수 있습니다. Laravel 현지화에 대해 더 알아보려면 전체 [localization documentation](/docs/master/localization)를 확인하십시오.

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="custom-messages-for-specific-attributes"></a>
<!-- #### Custom Messages for Specific Attributes -->
#### Custom Messages for Specific Attributes

<!-- You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file: -->
애플리케이션의 유효성 검증 언어 파일 안에서 지정한 속성과 규칙 조합에 사용되는 오류 메시지를 사용자 정의할 수 있습니다. 이렇게 하려면 애플리케이션의 `lang/xx/validation.php` 언어 파일에 있는 `custom` 배열에 사용자 정의 메시지를 추가합니다.

```php
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
Laravel의 여러 내장 오류 메시지에는 유효성 검증 중인 필드 또는 속성 이름으로 대체되는 `:attribute` 플레이스홀더가 포함되어 있습니다. 유효성 검증 메시지의 `:attribute` 부분을 사용자 정의 값으로 대체하고 싶다면 `lang/xx/validation.php` 언어 파일의 `attributes` 배열에서 사용자 정의 속성 이름을 지정할 수 있습니다.

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<a name="specifying-values-in-language-files"></a>
<!-- ### Specifying Values in Language Files -->
### Specifying Values in Language Files

<!-- Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`: -->
Laravel의 일부 내장 유효성 검증 규칙 오류 메시지에는 요청 속성의 현재 값으로 대체되는 `:value` 플레이스홀더가 포함되어 있습니다. 그러나 때때로 유효성 검증 메시지의 `:value` 부분을 해당 값의 사용자 정의 표현으로 대체해야 할 수 있습니다. 예를 들어, `payment_type`의 값이 `cc`일 때 신용카드 번호가 필수임을 지정하는 다음 규칙을 살펴보겠습니다.

```php
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

<!-- If this validation rule fails, it will produce the following error message: -->
이 유효성 검증 규칙이 실패하면 다음 오류 메시지가 생성됩니다.

```text
The credit card number field is required when payment type is cc.
```

<!-- Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `lang/xx/validation.php` language file by defining a `values` array: -->
결제 유형 값으로 `cc`를 표시하는 대신, `lang/xx/validation.php` 언어 파일에서 `values` 배열을 정의하여 더 사용자 친화적인 값 표현을 지정할 수 있습니다.

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령어를 통해 게시할 수 있습니다.

<!-- After defining this value, the validation rule will produce the following error message: -->
이 값을 정의한 뒤에는 유효성 검증 규칙이 다음 오류 메시지를 생성합니다.

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
<!-- ## Available Validation Rules -->
## Available Validation Rules

<!-- Below is a list of all available validation rules and their function: -->
아래는 사용 가능한 모든 유효성 검증 규칙과 그 기능 목록입니다.

<!-- #### Booleans -->
#### Booleans

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)
-->
[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

<!-- </div> -->
</div>

<!-- #### Strings -->
#### Strings

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Active URL](#rule-active-url)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Different](#rule-different)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Hex Color](#rule-hex-color)
[In](#rule-in)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Min](#rule-min)
[Not In](#rule-not-in)
[Regular Expression](#rule-regex)
[Not Regular Expression](#rule-not-regex)
[Same](#rule-same)
[Size](#rule-size)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)
-->
[Active URL](#rule-active-url)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Different](#rule-different)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Hex Color](#rule-hex-color)
[In](#rule-in)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Min](#rule-min)
[Not In](#rule-not-in)
[Regular Expression](#rule-regex)
[Not Regular Expression](#rule-not-regex)
[Same](#rule-same)
[Size](#rule-size)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

<!-- </div> -->
</div>

<!-- #### Numbers -->
#### Numbers

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Between](#rule-between)
[Decimal](#rule-decimal)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Integer](#rule-integer)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Multiple Of](#rule-multiple-of)
[Numeric](#rule-numeric)
[Same](#rule-same)
[Size](#rule-size)
-->
[Between](#rule-between)
[Decimal](#rule-decimal)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Integer](#rule-integer)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Multiple Of](#rule-multiple-of)
[Numeric](#rule-numeric)
[Same](#rule-same)
[Size](#rule-size)

<!-- </div> -->
</div>

<!-- #### Arrays -->
#### Arrays

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Array](#rule-array)
[Between](#rule-between)
[Contains](#rule-contains)
[Doesnt Contain](#rule-doesnt-contain)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)
-->
[Array](#rule-array)
[Between](#rule-between)
[Contains](#rule-contains)
[Doesnt Contain](#rule-doesnt-contain)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)

<!-- </div> -->
</div>

<!-- #### Dates -->
#### Dates

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[After](#rule-after)
[After Or Equal](#rule-after-or-equal)
[Before](#rule-before)
[Before Or Equal](#rule-before-or-equal)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Timezone](#rule-timezone)
-->
[After](#rule-after)
[After Or Equal](#rule-after-or-equal)
[Before](#rule-before)
[Before Or Equal](#rule-before-or-equal)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Timezone](#rule-timezone)

<!-- </div> -->
</div>

<!-- #### Files -->
#### Files

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Between](#rule-between)
[Dimensions](#rule-dimensions)
[Encoding](#rule-encoding)
[Extensions](#rule-extensions)
[File](#rule-file)
[Image](#rule-image)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Size](#rule-size)
-->
[Between](#rule-between)
[Dimensions](#rule-dimensions)
[Encoding](#rule-encoding)
[Extensions](#rule-extensions)
[File](#rule-file)
[Image](#rule-image)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Size](#rule-size)

<!-- </div> -->
</div>

<!-- #### Database -->
#### Database

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Exists](#rule-exists)
[Unique](#rule-unique)
-->
[Exists](#rule-exists)
[Unique](#rule-unique)

<!-- </div> -->
</div>

<!-- #### Utilities -->
#### Utilities

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[Any Of](#rule-anyof)
[Bail](#rule-bail)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Filled](#rule-filled)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Nullable](#rule-nullable)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited If Accepted](#rule-prohibited-if-accepted)
[Prohibited If Declined](#rule-prohibited-if-declined)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required If Declined](#rule-required-if-declined)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Sometimes](#validating-when-present)
-->
[Any Of](#rule-anyof)
[Bail](#rule-bail)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Filled](#rule-filled)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Nullable](#rule-nullable)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited If Accepted](#rule-prohibited-if-accepted)
[Prohibited If Declined](#rule-prohibited-if-declined)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required If Declined](#rule-required-if-declined)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Sometimes](#validating-when-present)

<!-- </div> -->
</div>

<a name="rule-accepted"></a>
<!-- #### accepted -->
#### accepted

<!-- The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. This is useful for validating "Terms of Service" acceptance or similar fields. -->
유효성 검증 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 이는 "Terms of Service" 동의나 이와 비슷한 필드를 유효성 검증할 때 유용합니다.

<a name="rule-accepted-if"></a>
<!-- #### accepted_if:anotherfield,value,... -->
#### accepted_if:anotherfield,value,...

<!-- The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields. -->
유효성 검증 중인 다른 필드가 지정한 값과 같다면, 유효성 검증 중인 필드는 `"yes"`, `"on"`, `1`, `"1"`, `true`, `"true"` 중 하나여야 합니다. 이는 "Terms of Service" 동의나 이와 비슷한 필드를 유효성 검증할 때 유용합니다.

<a name="rule-active-url"></a>
<!-- #### active_url -->
#### active_url

<!-- The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`. -->
유효성 검증 중인 필드는 PHP 함수 `dns_get_record` 기준으로 유효한 A 또는 AAAA 레코드를 가져야 합니다. 제공된 URL의 호스트명은 PHP 함수 `parse_url`을 사용해 추출된 뒤 `dns_get_record`에 전달됩니다.

<a name="rule-after"></a>
<!-- #### after:_date_ -->
#### after:_date_

<!-- The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance: -->
유효성 검증 중인 필드는 주어진 날짜 이후의 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되도록 PHP 함수 `strtotime`에 전달됩니다.

```php
'start_date' => 'required|date|after:tomorrow'
```

<!-- Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date: -->
`strtotime`으로 평가할 날짜 문자열을 전달하는 대신, 비교할 다른 필드를 지정할 수도 있습니다.

```php
'finish_date' => 'required|date|after:start_date'
```
<!-- For convenience, date-based rules may be constructed using the fluent `date` rule builder: -->
편의를 위해 날짜 기반 규칙은 유연한 `date` 규칙 빌더를 사용하여 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

<!-- The `afterToday` and `todayOrAfter` methods may be used to fluently express the date and must be after today, or today or after, respectively: -->
`afterToday`와 `todayOrAfter` 메서드를 사용하면 날짜가 각각 오늘 이후여야 함, 또는 오늘이거나 그 이후여야 함을 유연하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
<!-- #### after\_or\_equal:_date_ -->
#### after\_or\_equal:_date_

<!-- The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule. -->
유효성 검증 대상 필드는 주어진 날짜 이후이거나 같은 값이어야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참고하십시오.

<!-- For convenience, date-based rules may be constructed using the fluent `date` rule builder: -->
편의를 위해 날짜 기반 규칙은 유연한 `date` 규칙 빌더를 사용하여 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
<!-- #### anyOf -->
#### anyOf

<!-- The `Rule::anyOf` validation rule allows you to specify that the field under validation must satisfy any of the given validation rulesets. For example, the following rule will validate that the `username` field is either an email address or an alpha-numeric string (including dashes) that is at least 6 characters long: -->
`Rule::anyOf` 유효성 검증 규칙을 사용하면 유효성 검증 대상 필드가 주어진 유효성 검증 규칙 집합 중 하나라도 만족해야 한다고 지정할 수 있습니다. 예를 들어, 다음 규칙은 `username` 필드가 이메일 주소이거나, 최소 6자 이상인 알파벳과 숫자로 이루어진 문자열(대시 포함)인지 검증합니다.

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
<!-- #### alpha -->
#### alpha

<!-- The field under validation must be entirely Unicode alphabetic characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) and [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=). -->
유효성 검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함된 Unicode 알파벳 문자로만 이루어져야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
이 유효성 검증 규칙을 ASCII 범위 문자(`a-z` 및 `A-Z`)로 제한하려면 유효성 검증 규칙에 `ascii` 옵션을 제공할 수 있습니다.

```php
'username' => 'alpha:ascii',
```

<a name="rule-alpha-dash"></a>
<!-- #### alpha_dash -->
#### alpha_dash

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), as well as ASCII dashes (`-`) and ASCII underscores (`_`). -->
유효성 검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 Unicode 알파벳 및 숫자 문자와 ASCII 대시(`-`), ASCII 밑줄(`_`)로만 이루어져야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule: -->
이 유효성 검증 규칙을 ASCII 범위 문자(`a-z`, `A-Z`, `0-9`)로 제한하려면 유효성 검증 규칙에 `ascii` 옵션을 제공할 수 있습니다.

```php
'username' => 'alpha_dash:ascii',
```

<a name="rule-alpha-num"></a>
<!-- #### alpha_num -->
#### alpha_num

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), and [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=). -->
유효성 검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 Unicode 알파벳 및 숫자 문자로만 이루어져야 합니다.

<!-- To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule: -->
이 유효성 검증 규칙을 ASCII 범위 문자(`a-z`, `A-Z`, `0-9`)로 제한하려면 유효성 검증 규칙에 `ascii` 옵션을 제공할 수 있습니다.

```php
'username' => 'alpha_num:ascii',
```

<a name="rule-array"></a>
<!-- #### array -->
#### array

<!-- The field under validation must be a PHP `array`. -->
유효성 검증 대상 필드는 PHP `array`여야 합니다.

<!-- When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule: -->
`array` 규칙에 추가 값이 제공되면, 입력 배열의 각 키는 규칙에 제공된 값 목록 안에 있어야 합니다. 다음 예제에서는 입력 배열의 `admin` 키가 `array` 규칙에 제공된 값 목록에 포함되어 있지 않으므로 유효하지 않습니다.

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

<!-- In general, you should always specify the array keys that are allowed to be present within your array. -->
일반적으로 배열 안에 존재할 수 있는 배열 키를 항상 명시해야 합니다.

<a name="rule-ascii"></a>
<!-- #### ascii -->
#### ascii

<!-- The field under validation must be entirely 7-bit ASCII characters. -->
유효성 검증 대상 필드는 7비트 ASCII 문자로만 이루어져야 합니다.

<a name="rule-bail"></a>
<!-- #### bail -->
#### bail

<!-- Stop running validation rules for the field after the first validation failure. -->
필드에서 첫 번째 유효성 검증 실패가 발생하면 해당 필드의 유효성 검증 규칙 실행을 중단합니다.

<!-- While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`bail` 규칙은 유효성 검증 실패가 발생한 특정 필드의 검증만 중단하지만, `stopOnFirstFailure` 메서드는 하나의 유효성 검증 실패가 발생하는 즉시 모든 속성의 검증을 중단해야 한다고 validator에 알립니다.

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
<!-- #### before:_date_ -->
#### before:_date_

<!-- The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [after](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
유효성 검증 대상 필드는 주어진 날짜보다 앞선 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되도록 PHP `strtotime` 함수에 전달됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 유효성 검증 대상인 다른 필드의 이름을 `date` 값으로 제공할 수 있습니다.

<!-- For convenience, date-based rules may also be constructed using the fluent `date` rule builder: -->
편의를 위해 날짜 기반 규칙은 유연한 `date` 규칙 빌더를 사용하여 구성할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

<!-- The `beforeToday` and `todayOrBefore` methods may be used to fluently express the date and must be before today, or today or before, respectively: -->
`beforeToday`와 `todayOrBefore` 메서드를 사용하면 날짜가 각각 오늘 이전이어야 함, 또는 오늘이거나 그 이전이어야 함을 유연하게 표현할 수 있습니다.

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
<!-- #### before\_or\_equal:_date_ -->
#### before\_or\_equal:_date_

<!-- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [after](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
유효성 검증 대상 필드는 주어진 날짜보다 앞서거나 같은 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되도록 PHP `strtotime` 함수에 전달됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 유효성 검증 대상인 다른 필드의 이름을 `date` 값으로 제공할 수 있습니다.

<!-- For convenience, date-based rules may also be constructed using the fluent `date` rule builder: -->
편의를 위해 날짜 기반 규칙은 유연한 `date` 규칙 빌더를 사용하여 구성할 수도 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
<!-- #### between:_min_,_max_ -->
#### between:_min_,_max_

<!-- The field under validation must have a size between the given _min_ and _max_ (inclusive). Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 주어진 _min_과 _max_ 사이의 크기여야 합니다(양끝 포함). 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 같은 방식으로 평가됩니다.

<a name="rule-boolean"></a>
<!-- #### boolean -->
#### boolean

<!-- The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`. -->
유효성 검증 대상 필드는 boolean으로 casting될 수 있어야 합니다. 허용되는 입력은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

<!-- You may use the `strict` parameter to only consider the field valid if its value is `true` or `false`: -->
필드 값이 `true` 또는 `false`인 경우에만 유효하다고 판단하려면 `strict` 매개변수를 사용할 수 있습니다.

```php
'foo' => 'boolean:strict'
```

<a name="rule-confirmed"></a>
<!-- #### confirmed -->
#### confirmed

<!-- The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input. -->
유효성 검증 대상 필드에는 `{field}_confirmation` 형식의 일치하는 필드가 있어야 합니다. 예를 들어 유효성 검증 대상 필드가 `password`라면, 입력에 일치하는 `password_confirmation` 필드가 있어야 합니다.

<!-- You may also pass a custom confirmation field name. For example, `confirmed:repeat_username` will expect the field `repeat_username` to match the field under validation. -->
사용자 정의 확인 필드 이름을 전달할 수도 있습니다. 예를 들어 `confirmed:repeat_username`은 `repeat_username` 필드가 유효성 검증 대상 필드와 일치해야 한다고 기대합니다.

<a name="rule-contains"></a>
<!-- #### contains:_foo_,_bar_,... -->
#### contains:_foo_,_bar_,...

<!-- The field under validation must be an array that contains all of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::contains` method may be used to fluently construct the rule: -->
유효성 검증 대상 필드는 주어진 모든 매개변수 값을 포함하는 배열이어야 합니다. 이 규칙은 배열을 `implode`해야 하는 경우가 많기 때문에, `Rule::contains` 메서드를 사용하여 규칙을 유연하게 구성할 수 있습니다.

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
<!-- #### doesnt_contain:_foo_,_bar_,... -->
#### doesnt_contain:_foo_,_bar_,...

<!-- The field under validation must be an array that does not contain any of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::doesntContain` method may be used to fluently construct the rule: -->
유효성 검증 대상 필드는 주어진 매개변수 값을 하나도 포함하지 않는 배열이어야 합니다. 이 규칙은 배열을 `implode`해야 하는 경우가 많기 때문에, `Rule::doesntContain` 메서드를 사용하여 규칙을 유연하게 구성할 수 있습니다.

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
<!-- #### current_password -->
#### current_password

<!-- The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/master/authentication) using the rule's first parameter: -->
유효성 검증 대상 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 매개변수를 사용하여 [authentication guard](/docs/master/authentication)를 지정할 수 있습니다.

```php
'password' => 'current_password:api'
```

<a name="rule-date"></a>
<!-- #### date -->
#### date

<!-- The field under validation must be a valid, non-relative date according to the `strtotime` PHP function. -->
유효성 검증 대상 필드는 PHP `strtotime` 함수 기준으로 유효한 비상대 날짜여야 합니다.

<a name="rule-date-equals"></a>
<!-- #### date_equals:_date_ -->
#### date_equals:_date_

<!-- The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. -->
유효성 검증 대상 필드는 주어진 날짜와 같아야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되도록 PHP `strtotime` 함수에 전달됩니다.

<a name="rule-date-format"></a>
<!-- #### date_format:_format_,... -->
#### date_format:_format_,...

<!-- The field under validation must match one of the given _formats_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class. -->
유효성 검증 대상 필드는 주어진 _formats_ 중 하나와 일치해야 합니다. 필드를 검증할 때는 `date` 또는 `date_format` 중 **하나만** 사용해야 하며, 둘 다 사용해서는 안 됩니다. 이 유효성 검증 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스가 지원하는 모든 형식을 지원합니다.

<!-- For convenience, date-based rules may be constructed using the fluent `date` rule builder: -->
편의를 위해 날짜 기반 규칙은 유연한 `date` 규칙 빌더를 사용하여 구성할 수 있습니다.

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
<!-- #### decimal:_min_,_max_ -->
#### decimal:_min_,_max_

<!-- The field under validation must be numeric and must contain the specified number of decimal places: -->
유효성 검증 대상 필드는 숫자여야 하며, 지정된 소수 자릿수를 포함해야 합니다.

```php
// Must have exactly two decimal places (9.99)...
'price' => 'decimal:2'

// Must have between 2 and 4 decimal places...
'price' => 'decimal:2,4'
```

<a name="rule-declined"></a>
<!-- #### declined -->
#### declined

<!-- The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
유효성 검증 대상 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`여야 합니다.

<a name="rule-declined-if"></a>
<!-- #### declined_if:anotherfield,value,... -->
#### declined_if:anotherfield,value,...

<!-- The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"` if another field under validation is equal to a specified value. -->
유효성 검증 대상 필드는 유효성 검증 대상인 다른 필드가 지정된 값과 같을 때 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`여야 합니다.

<a name="rule-different"></a>
<!-- #### different:_field_ -->
#### different:_field_

<!-- The field under validation must have a different value than _field_. -->
유효성 검증 대상 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
<!-- #### digits:_value_ -->
#### digits:_value_

<!-- The integer under validation must have an exact length of _value_. -->
유효성 검증 대상 정수는 정확히 _value_ 길이를 가져야 합니다.

<a name="rule-digits-between"></a>
<!-- #### digits_between:_min_,_max_ -->
#### digits_between:_min_,_max_

<!-- The integer under validation must have a length between the given _min_ and _max_. -->
유효성 검증 대상 정수는 주어진 _min_과 _max_ 사이의 길이를 가져야 합니다.

<a name="rule-dimensions"></a>
<!-- #### dimensions -->
#### dimensions

<!-- The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters: -->
유효성 검증 대상 파일은 규칙의 매개변수로 지정된 크기 제약 조건을 만족하는 이미지여야 합니다.

```php
'avatar' => 'dimensions:min_width=100,min_height=200'
```

<!-- Available constraints are: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_. -->
사용 가능한 제약 조건은 _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_입니다.

<!-- A _ratio_ constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`: -->
_ratio_ 제약 조건은 너비를 높이로 나눈 값으로 표현해야 합니다. 이는 `3/2` 같은 분수 또는 `1.5` 같은 실수로 지정할 수 있습니다.

```php
'avatar' => 'dimensions:ratio=3/2'
```

<!-- Since this rule requires several arguments, it is often more convenient to use the `Rule::dimensions` method to fluently construct the rule: -->
이 규칙은 여러 인수를 필요로 하므로, `Rule::dimensions` 메서드를 사용하여 규칙을 유연하게 구성하는 것이 더 편리한 경우가 많습니다.

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
<!-- #### distinct -->
#### distinct

<!-- When validating arrays, the field under validation must not have any duplicate values: -->
배열을 검증할 때 유효성 검증 대상 필드에는 중복 값이 없어야 합니다.

```php
'foo.*.id' => 'distinct'
```

<!-- Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition: -->
distinct는 기본적으로 느슨한 변수 비교를 사용합니다. 엄격한 비교를 사용하려면 유효성 검증 규칙 정의에 `strict` 매개변수를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:strict'
```

<!-- You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences: -->
대소문자 차이를 무시하도록 하려면 유효성 검증 규칙의 인수에 `ignore_case`를 추가할 수 있습니다.

```php
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-doesnt-start-with"></a>
<!-- #### doesnt_start_with:_foo_,_bar_,... -->
#### doesnt_start_with:_foo_,_bar_,...

<!-- The field under validation must not start with one of the given values. -->
유효성 검증 대상 필드는 주어진 값 중 하나로 시작해서는 안 됩니다.

<a name="rule-doesnt-end-with"></a>
<!-- #### doesnt_end_with:_foo_,_bar_,... -->
#### doesnt_end_with:_foo_,_bar_,...

<!-- The field under validation must not end with one of the given values. -->
유효성 검증 대상 필드는 주어진 값 중 하나로 끝나서는 안 됩니다.

<a name="rule-email"></a>
<!-- #### email -->
#### email

<!-- The field under validation must be formatted as an email address. This validation rule utilizes the [egulias/email-validator](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well: -->
유효성 검증 대상 필드는 이메일 주소 형식이어야 합니다. 이 유효성 검증 규칙은 이메일 주소를 검증하기 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` validator가 적용되지만, 다른 검증 방식도 적용할 수 있습니다.

```php
'email' => 'email:rfc,dns'
```

<!-- The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply: -->
위 예제는 `RFCValidation`과 `DNSCheckValidation` 검증을 적용합니다. 적용할 수 있는 검증 방식의 전체 목록은 다음과 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `rfc`: `RFCValidation` - Validate the email address according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs).
- `strict`: `NoRFCWarningsValidation` - Validate the email according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs), failing when warnings are found (e.g. trailing periods and multiple consecutive periods).
- `dns`: `DNSCheckValidation` - Ensure the email address's domain has a valid MX record.
- `spoof`: `SpoofCheckValidation` - Ensure the email address does not contain homograph or deceptive Unicode characters.
- `filter`: `FilterEmailValidation` - Ensure the email address is valid according to PHP's `filter_var` function.
- `filter_unicode`: `FilterEmailValidation::unicode()` - Ensure the email address is valid according to PHP's `filter_var` function, allowing some Unicode characters.
-->
- `rfc`: `RFCValidation` - [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 주소를 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일을 검증하며, 경고가 발견되면 실패합니다(예: 끝에 붙은 마침표, 여러 개의 연속된 마침표).
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인에 유효한 MX 레코드가 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 이메일 주소에 동형 문자나 속일 수 있는 Unicode 문자가 포함되어 있지 않은지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수 기준으로 이메일 주소가 유효한지 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - 일부 Unicode 문자를 허용하면서 PHP의 `filter_var` 함수 기준으로 이메일 주소가 유효한지 확인합니다.

<!-- </div> -->
</div>

<!-- For convenience, email validation rules may be built using the fluent rule builder: -->
편의를 위해 이메일 유효성 검증 규칙은 유연한 규칙 빌더를 사용하여 구성할 수 있습니다.

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
<!-- #### encoding:*encoding_type* -->
#### encoding:*encoding_type*

<!-- The field under validation must match the specified character encoding. This rule uses PHP's `mb_check_encoding` function to verify the encoding of the given file or string value. For convenience, the `encoding` rule may be constructed using Laravel's fluent file rule builder: -->
유효성 검증 대상 필드는 지정된 문자 인코딩과 일치해야 합니다. 이 규칙은 PHP의 `mb_check_encoding` 함수를 사용하여 주어진 파일 또는 문자열 값의 인코딩을 확인합니다. 편의를 위해 `encoding` 규칙은 Laravel의 fluent 파일 규칙 빌더를 사용하여 구성할 수 있습니다.

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
<!-- #### ends_with:_foo_,_bar_,... -->
#### ends_with:_foo_,_bar_,...

<!-- The field under validation must end with one of the given values. -->
유효성 검증 대상 필드는 주어진 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
<!-- #### enum -->
#### enum

<!-- The `Enum` rule is a class-based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument. When validating primitive values, a backed Enum should be provided to the `Enum` rule: -->
`Enum` 규칙은 유효성 검증 대상 필드에 유효한 enum 값이 들어 있는지 검증하는 클래스 기반 규칙입니다. `Enum` 규칙은 생성자 인수로 enum 이름 하나만 받습니다. 원시 값을 검증할 때는 backed Enum을 `Enum` 규칙에 제공해야 합니다.

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

<!-- The `Enum` rule's `only` and `except` methods may be used to limit which enum cases should be considered valid: -->
`Enum` 규칙의 `only` 및 `except` 메서드를 사용하여 어떤 enum case를 유효한 값으로 볼지 제한할 수 있습니다.

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

<!-- The `when` method may be used to conditionally modify the `Enum` rule: -->
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
<!-- #### exclude -->
#### exclude

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods. -->
유효성 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
<!-- #### exclude_if:_anotherfield_,_value_ -->
#### exclude_if:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_. -->
_anotherfield_ 필드가 _value_와 같으면, 유효성 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<!-- If complex conditional exclusion logic is required, you may utilize the `Rule::excludeIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be excluded: -->
복잡한 조건부 제외 로직이 필요하다면 `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 boolean 또는 클로저를 받습니다. 클로저를 전달하는 경우, 해당 클로저는 유효성 검증 대상 필드를 제외할지 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

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
<!-- #### exclude_unless:_anotherfield_,_value_ -->
#### exclude_unless:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless _anotherfield_'s field is equal to _value_. If _value_ is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data. -->
_anotherfield_ 필드가 _value_와 같지 않으면, 유효성 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`)인 경우, 비교 대상 필드가 `null`이거나 요청 데이터에 비교 대상 필드가 없을 때를 제외하고 유효성 검증 대상 필드는 제외됩니다.

<a name="rule-exclude-with"></a>
<!-- #### exclude_with:_anotherfield_ -->
#### exclude_with:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is present. -->
_anotherfield_ 필드가 존재하면, 유효성 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
<!-- #### exclude_without:_anotherfield_ -->
#### exclude_without:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present. -->
_anotherfield_ 필드가 존재하지 않으면, 유효성 검증 대상 필드는 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
<!-- #### exists:_table_,_column_ -->
#### exists:_table_,_column_

<!-- The field under validation must exist in a given database table. -->
유효성 검증 대상 필드는 주어진 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
<!-- #### Basic Usage of Exists Rule -->
#### Basic Usage of Exists Rule

```php
'state' => 'exists:states'
```

<!-- If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value. -->
`column` 옵션을 지정하지 않으면 필드 이름이 사용됩니다. 따라서 이 경우 해당 규칙은 `states` 데이터베이스 테이블에 요청의 `state` 속성값과 일치하는 `state` 컬럼 값을 가진 레코드가 있는지 검증합니다.

<a name="specifying-a-custom-column-name"></a>
<!-- #### Specifying a Custom Column Name -->
#### Specifying a Custom Column Name

<!-- You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name: -->
데이터베이스 테이블 이름 뒤에 컬럼 이름을 배치하여 유효성 검증 규칙에서 사용할 데이터베이스 컬럼 이름을 명시적으로 지정할 수 있습니다.

```php
'state' => 'exists:states,abbreviation'
```

<!-- Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name: -->
때로는 `exists` 쿼리에 사용할 특정 데이터베이스 연결을 지정해야 할 수 있습니다. 테이블 이름 앞에 연결 이름을 붙이면 됩니다.

```php
'email' => 'exists:connection.staff,email'
```

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블 이름을 직접 지정하는 대신, 테이블 이름을 결정하는 데 사용할 Eloquent 모델을 지정할 수도 있습니다.

```php
'user_id' => 'exists:App\Models\User,id'
```

<!-- If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them: -->
유효성 검증 규칙이 실행하는 쿼리를 사용자 지정하려면 `Rule` 클래스를 사용하여 fluent 방식으로 규칙을 정의할 수 있습니다. 이 예제에서는 `|` 문자로 규칙을 구분하는 대신 배열로 유효성 검증 규칙을 지정합니다.

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

<!-- You may explicitly specify the database column name that should be used by the `exists` rule generated by the `Rule::exists` method by providing the column name as the second argument to the `exists` method: -->
`exists` 메서드의 두 번째 인수로 컬럼 이름을 제공하면, `Rule::exists` 메서드가 생성하는 `exists` 규칙에서 사용할 데이터베이스 컬럼 이름을 명시적으로 지정할 수 있습니다.

```php
'state' => Rule::exists('states', 'abbreviation'),
```

<!-- Sometimes, you may wish to validate whether an array of values exists in the database. You can do so by adding both the `exists` and [array](#rule-array) rules to the field being validated: -->
때로는 값 배열이 데이터베이스에 존재하는지 검증하고 싶을 수 있습니다. 검증할 필드에 `exists` 규칙과 [array](#rule-array) 규칙을 모두 추가하면 됩니다.

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

<!-- When both of these rules are assigned to a field, Laravel will automatically build a single query to determine if all of the given values exist in the specified table. -->
이 두 규칙이 모두 필드에 지정되면, Laravel은 주어진 모든 값이 지정된 테이블에 존재하는지 확인하기 위해 단일 쿼리를 자동으로 생성합니다.

<a name="rule-extensions"></a>
<!-- #### extensions:_foo_,_bar_,... -->
#### extensions:_foo_,_bar_,...

<!-- The file under validation must have a user-assigned extension corresponding to one of the listed extensions: -->
유효성 검증 대상 파일은 나열된 확장자 중 하나에 해당하는 사용자 지정 확장자를 가져야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> 사용자가 지정한 파일 확장자만으로 파일을 검증하는 방식에 절대 의존해서는 안 됩니다. 일반적으로 이 규칙은 항상 [mimes](#rule-mimes) 또는 [mimetypes](#rule-mimetypes) 규칙과 함께 사용해야 합니다.

<a name="rule-file"></a>
<!-- #### file -->
#### file

<!-- The field under validation must be a successfully uploaded file. -->
유효성 검증 대상 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
<!-- #### filled -->
#### filled

<!-- The field under validation must not be empty when it is present. -->
유효성 검증 대상 필드는 존재하는 경우 비어 있으면 안 됩니다.

<a name="rule-gt"></a>
<!-- #### gt:_field_ -->
#### gt:_field_

<!-- The field under validation must be greater than the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 주어진 _field_ 또는 _value_보다 커야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-gte"></a>
<!-- #### gte:_field_ -->
#### gte:_field_

<!-- The field under validation must be greater than or equal to the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 주어진 _field_ 또는 _value_보다 크거나 같아야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-hex-color"></a>
<!-- #### hex_color -->
#### hex_color

<!-- The field under validation must contain a valid color value in [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) format. -->
유효성 검증 대상 필드는 [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 형식의 유효한 색상 값을 포함해야 합니다.

<a name="rule-image"></a>
<!-- #### image -->
#### image

<!-- The file under validation must be an image (jpg, jpeg, png, bmp, gif, or webp). -->
유효성 검증 대상 파일은 이미지(jpg, jpeg, png, bmp, gif 또는 webp)여야 합니다.

> [!WARNING]
> 기본적으로 image 규칙은 XSS 취약점 가능성 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 한다면 `image` 규칙에 `allow_svg` 지시어(`image:allow_svg`)를 제공할 수 있습니다.

<a name="rule-in"></a>
<!-- #### in:_foo_,_bar_,... -->
#### in:_foo_,_bar_,...

<!-- The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule: -->
유효성 검증 대상 필드는 주어진 값 목록에 포함되어야 합니다. 이 규칙은 배열을 `implode`해야 하는 경우가 많으므로, `Rule::in` 메서드를 사용하여 fluent 방식으로 규칙을 구성할 수 있습니다.

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

<!-- When the `in` rule is combined with the `array` rule, each value in the input array must be present within the list of values provided to the `in` rule. In the following example, the `LAS` airport code in the input array is invalid since it is not contained in the list of airports provided to the `in` rule: -->
`in` 규칙을 `array` 규칙과 함께 사용하면, 입력 배열의 각 값이 `in` 규칙에 제공된 값 목록 안에 있어야 합니다. 다음 예제에서 입력 배열의 `LAS` 공항 코드는 `in` 규칙에 제공된 공항 목록에 포함되어 있지 않으므로 유효하지 않습니다.

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
<!-- #### in_array:_anotherfield_.* -->
#### in_array:_anotherfield_.*

<!-- The field under validation must exist in _anotherfield_'s values. -->
유효성 검증 대상 필드는 _anotherfield_의 값 안에 존재해야 합니다.

<a name="rule-in-array-keys"></a>
<!-- #### in_array_keys:_value_.* -->
#### in_array_keys:_value_.*

<!-- The field under validation must be an array having at least one of the given _values_ as a key within the array: -->
유효성 검증 대상 필드는 주어진 _values_ 중 적어도 하나를 키로 포함하는 배열이어야 합니다.

```php
'config' => 'array|in_array_keys:timezone'
```

<a name="rule-integer"></a>
<!-- #### integer -->
#### integer

<!-- The field under validation must be an integer. -->
유효성 검증 대상 필드는 정수여야 합니다.

<!-- You may use the `strict` parameter to only consider the field valid if its type is `integer`. Strings with integer values will be considered invalid: -->
필드의 타입이 `integer`인 경우에만 유효한 것으로 보려면 `strict` 매개변수를 사용할 수 있습니다. 정수 값을 가진 문자열은 유효하지 않은 것으로 간주됩니다.

```php
'age' => 'integer:strict'
```

> [!WARNING]
> 이 유효성 검증 규칙은 입력이 "integer" 변수 타입인지 확인하지 않고, PHP의 `FILTER_VALIDATE_INT` 규칙이 허용하는 타입인지 여부만 확인합니다. 입력이 숫자인지 검증해야 한다면 [the `numeric` validation rule](#rule-numeric)과 함께 이 규칙을 사용하십시오.

<a name="rule-ip"></a>
<!-- #### ip -->
#### ip

<!-- The field under validation must be an IP address. -->
유효성 검증 대상 필드는 IP 주소여야 합니다.

<a name="ipv4"></a>
<!-- #### ipv4 -->
#### ipv4

<!-- The field under validation must be an IPv4 address. -->
유효성 검증 대상 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
<!-- #### ipv6 -->
#### ipv6

<!-- The field under validation must be an IPv6 address. -->
유효성 검증 대상 필드는 IPv6 주소여야 합니다.

<a name="rule-json"></a>
<!-- #### json -->
#### json

<!-- The field under validation must be a valid JSON string. -->
유효성 검증 대상 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
<!-- #### lt:_field_ -->
#### lt:_field_

<!-- The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 주어진 _field_보다 작아야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lte"></a>
<!-- #### lte:_field_ -->
#### lte:_field_

<!-- The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 주어진 _field_보다 작거나 같아야 합니다. 두 필드는 같은 타입이어야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-lowercase"></a>
<!-- #### lowercase -->
#### lowercase

<!-- The field under validation must be lowercase. -->
유효성 검증 대상 필드는 소문자여야 합니다.

<a name="rule-list"></a>
<!-- #### list -->
#### list

<!-- The field under validation must be an array that is a list. An array is considered a list if its keys consist of consecutive numbers from 0 to `count($array) - 1`. -->
유효성 검증 대상 필드는 list인 배열이어야 합니다. 배열의 키가 0부터 `count($array) - 1`까지의 연속된 숫자로 이루어져 있으면 list로 간주됩니다.

<a name="rule-mac"></a>
<!-- #### mac_address -->
#### mac_address

<!-- The field under validation must be a MAC address. -->
유효성 검증 대상 필드는 MAC 주소여야 합니다.

<a name="rule-max"></a>
<!-- #### max:_value_ -->
#### max:_value_

<!-- The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 최대 _value_보다 작거나 같아야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-max-digits"></a>
<!-- #### max_digits:_value_ -->
#### max_digits:_value_

<!-- The integer under validation must have a maximum length of _value_. -->
유효성 검증 대상 정수는 최대 길이가 _value_여야 합니다.

<a name="rule-mimetypes"></a>
<!-- #### mimetypes:_text/plain_,... -->
#### mimetypes:_text/plain_,...

<!-- The file under validation must match one of the given MIME types: -->
유효성 검증 대상 파일은 주어진 MIME 타입 중 하나와 일치해야 합니다.

```php
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime',

'media' => 'mimetypes:image/*,video/*',
```

<!-- To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type. -->
업로드된 파일의 MIME 타입을 결정하기 위해 파일의 내용을 읽고, 프레임워크가 MIME 타입을 추측합니다. 이 값은 클라이언트가 제공한 MIME 타입과 다를 수 있습니다.

<a name="rule-mimes"></a>
<!-- #### mimes:_foo_,_bar_,... -->
#### mimes:_foo_,_bar_,...

<!-- The file under validation must have a MIME type corresponding to one of the listed extensions: -->
유효성 검증 대상 파일은 나열된 확장자 중 하나에 해당하는 MIME 타입을 가져야 합니다.

```php
'photo' => 'mimes:jpg,bmp,png'
```

<!-- Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
확장자만 지정하면 되지만, 이 규칙은 실제로 파일의 내용을 읽고 MIME 타입을 추측하여 파일의 MIME 타입을 검증합니다. MIME 타입과 해당 확장자의 전체 목록은 다음 위치에서 확인할 수 있습니다.

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
<!-- #### MIME Types and Extensions -->
#### MIME Types and Extensions

<!-- This validation rule does not verify agreement between the MIME type and the extension the user assigned to the file. For example, the `mimes:png` validation rule would consider a file containing valid PNG content to be a valid PNG image, even if the file is named `photo.txt`. If you would like to validate the user-assigned extension of the file, you may use the [extensions](#rule-extensions) rule. -->
이 유효성 검증 규칙은 MIME 타입과 사용자가 파일에 지정한 확장자가 서로 일치하는지 확인하지 않습니다. 예를 들어 `mimes:png` 유효성 검증 규칙은 파일 이름이 `photo.txt`이더라도, 파일 내용이 유효한 PNG라면 해당 파일을 유효한 PNG 이미지로 간주합니다. 파일의 사용자 지정 확장자를 검증하고 싶다면 [extensions](#rule-extensions) 규칙을 사용할 수 있습니다.

<a name="rule-min"></a>
<!-- #### min:_value_ -->
#### min:_value_

<!-- The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule. -->
유효성 검증 대상 필드는 최소 _value_를 가져야 합니다. 문자열, 숫자, 배열, 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-min-digits"></a>
<!-- #### min_digits:_value_ -->
#### min_digits:_value_

<!-- The integer under validation must have a minimum length of _value_. -->
유효성 검증 대상 정수는 최소 길이가 _value_여야 합니다.

<a name="rule-multiple-of"></a>
<!-- #### multiple_of:_value_ -->
#### multiple_of:_value_

<!-- The field under validation must be a multiple of _value_. -->
유효성 검증 대상 필드는 _value_의 배수여야 합니다.

<a name="rule-missing"></a>
<!-- #### missing -->
#### missing

<!-- The field under validation must not be present in the input data. -->
유효성 검증 대상 필드는 입력 데이터에 존재하지 않아야 합니다.

<a name="rule-missing-if"></a>
<!-- #### missing_if:_anotherfield_,_value_,... -->
#### missing_if:_anotherfield_,_value_,...

<!-- The field under validation must not be present if the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ 필드가 어떤 _value_와 같으면, 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-unless"></a>
<!-- #### missing_unless:_anotherfield_,_value_ -->
#### missing_unless:_anotherfield_,_value_

<!-- The field under validation must not be present unless the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ 필드가 어떤 _value_와 같지 않으면, 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with"></a>
<!-- #### missing_with:_foo_,_bar_,... -->
#### missing_with:_foo_,_bar_,...

<!-- The field under validation must not be present _only if_ any of the other specified fields are present. -->
지정된 다른 필드 중 하나라도 존재하는 경우에만, 유효성 검증 대상 필드는 존재하지 않아야 합니다.

<a name="rule-missing-with-all"></a>
<!-- #### missing_with_all:_foo_,_bar_,... -->
#### missing_with_all:_foo_,_bar_,...

<!-- The field under validation must not be present _only if_ all of the other specified fields are present. -->
유효성 검증 중인 필드는 지정된 다른 모든 필드가 존재하는 경우에만 존재해서는 안 됩니다.

<a name="rule-not-in"></a>
<!-- #### not_in:_foo_,_bar_,... -->
#### not_in:_foo_,_bar_,...

<!-- The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule: -->
유효성 검증 중인 필드는 주어진 값 목록에 포함되어서는 안 됩니다. `Rule::notIn` 메서드를 사용하여 규칙을 유창하게 구성할 수 있습니다.

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
<!-- #### not_regex:_pattern_ -->
#### not_regex:_pattern_

<!-- The field under validation must not match the given regular expression. -->
유효성 검증 중인 필드는 주어진 정규 표현식과 일치해서는 안 됩니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`. -->
내부적으로 이 규칙은 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 형식을 따라야 하므로, 유효한 구분자도 포함해야 합니다. 예: `'email' => 'not_regex:/^.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 특히 정규 표현식에 `|` 문자가 포함되어 있다면 `|` 구분자를 사용하는 대신 배열로 유효성 검증 규칙을 지정해야 할 수 있습니다.

<a name="rule-nullable"></a>
<!-- #### nullable -->
#### nullable

<!-- The field under validation may be `null`. -->
유효성 검증 중인 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
<!-- #### numeric -->
#### numeric

<!-- The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php). -->
유효성 검증 중인 필드는 [numeric](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<!-- You may use the `strict` parameter to only consider the field valid if its value is an integer or float type. Numeric strings will be considered invalid: -->
필드의 값이 정수 또는 부동소수점 타입인 경우에만 유효한 것으로 간주하려면 `strict` 매개변수를 사용할 수 있습니다. 숫자 문자열은 유효하지 않은 것으로 간주됩니다.

```php
'amount' => 'numeric:strict'
```

<a name="rule-present"></a>
<!-- #### present -->
#### present

<!-- The field under validation must exist in the input data. -->
유효성 검증 중인 필드는 입력 데이터에 존재해야 합니다.

<a name="rule-present-if"></a>
<!-- #### present_if:_anotherfield_,_value_,... -->
#### present_if:_anotherfield_,_value_,...

<!-- The field under validation must be present if the _anotherfield_ field is equal to any _value_. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 어떤 _value_ 와 같으면 존재해야 합니다.

<a name="rule-present-unless"></a>
<!-- #### present_unless:_anotherfield_,_value_ -->
#### present_unless:_anotherfield_,_value_

<!-- The field under validation must be present unless the _anotherfield_ field is equal to any _value_. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 어떤 _value_ 와 같지 않은 한 존재해야 합니다.

<a name="rule-present-with"></a>
<!-- #### present_with:_foo_,_bar_,... -->
#### present_with:_foo_,_bar_,...

<!-- The field under validation must be present _only if_ any of the other specified fields are present. -->
유효성 검증 중인 필드는 지정된 다른 필드 중 하나라도 존재하는 경우에만 존재해야 합니다.

<a name="rule-present-with-all"></a>
<!-- #### present_with_all:_foo_,_bar_,... -->
#### present_with_all:_foo_,_bar_,...

<!-- The field under validation must be present _only if_ all of the other specified fields are present. -->
유효성 검증 중인 필드는 지정된 다른 모든 필드가 존재하는 경우에만 존재해야 합니다.

<a name="rule-prohibited"></a>
<!-- #### prohibited -->
#### prohibited

<!-- The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
유효성 검증 중인 필드는 누락되었거나 비어 있어야 합니다. 필드는 다음 기준 중 하나를 충족하면 "비어 있음"으로 간주됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

<!-- </div> -->
</div>

<a name="rule-prohibited-if"></a>
<!-- #### prohibited_if:_anotherfield_,_value_,... -->
#### prohibited_if:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 어떤 _value_ 와 같으면 누락되었거나 비어 있어야 합니다. 필드는 다음 기준 중 하나를 충족하면 "비어 있음"으로 간주됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

<!-- </div> -->
</div>

<!-- If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited: -->
복잡한 조건부 금지 로직이 필요하다면 `Rule::prohibitedIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받습니다. 클로저가 전달되면, 해당 클로저는 유효성 검증 중인 필드를 금지할지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

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
<!-- #### prohibited_if_accepted:_anotherfield_,... -->
#### prohibited_if_accepted:_anotherfield_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`와 같으면 누락되었거나 비어 있어야 합니다.

<a name="rule-prohibited-if-declined"></a>
<!-- #### prohibited_if_declined:_anotherfield_,... -->
#### prohibited_if_declined:_anotherfield_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`와 같으면 누락되었거나 비어 있어야 합니다.

<a name="rule-prohibited-unless"></a>
<!-- #### prohibited_unless:_anotherfield_,_value_,... -->
#### prohibited_unless:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty unless the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 어떤 _value_ 와 같지 않은 한 누락되었거나 비어 있어야 합니다. 필드는 다음 기준 중 하나를 충족하면 "비어 있음"으로 간주됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

<!-- </div> -->
</div>

<a name="rule-prohibits"></a>
<!-- #### prohibits:_anotherfield_,... -->
#### prohibits:_anotherfield_,...

<!-- If the field under validation is not missing or empty, all fields in _anotherfield_ must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
유효성 검증 중인 필드가 누락되었거나 비어 있지 않다면, _anotherfield_ 에 있는 모든 필드는 누락되었거나 비어 있어야 합니다. 필드는 다음 기준 중 하나를 충족하면 "비어 있음"으로 간주됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.
-->
- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 빈 경로를 가진 업로드된 파일입니다.

<!-- </div> -->
</div>

<a name="rule-regex"></a>
<!-- #### regex:_pattern_ -->
#### regex:_pattern_

<!-- The field under validation must match the given regular expression. -->
유효성 검증 중인 필드는 주어진 정규 표현식과 일치해야 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`. -->
내부적으로 이 규칙은 PHP의 `preg_match` 함수를 사용합니다. 지정하는 패턴은 `preg_match`에서 요구하는 형식을 따라야 하므로, 유효한 구분자도 포함해야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`.

> [!WARNING]
> `regex` / `not_regex` 패턴을 사용할 때, 특히 정규 표현식에 `|` 문자가 포함되어 있다면 `|` 구분자를 사용하는 대신 배열로 규칙을 지정해야 할 수 있습니다.

<a name="rule-required"></a>
<!-- #### required -->
#### required

<!-- The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria: -->
유효성 검증 중인 필드는 입력 데이터에 존재해야 하며 비어 있으면 안 됩니다. 필드는 다음 기준 중 하나를 충족하면 "비어 있음"으로 간주됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.
-->
- 값이 `null`입니다.
- 값이 빈 문자열입니다.
- 값이 빈 배열이거나 빈 `Countable` 객체입니다.
- 값이 경로가 없는 업로드된 파일입니다.

<!-- </div> -->
</div>

<a name="rule-required-if"></a>
<!-- #### required_if:_anotherfield_,_value_,... -->
#### required_if:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 어떤 _value_ 와 같으면 존재해야 하며 비어 있으면 안 됩니다.

<!-- If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required: -->
`required_if` 규칙에 더 복잡한 조건을 구성하고 싶다면 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 또는 클로저를 받습니다. 클로저가 전달되면, 해당 클로저는 유효성 검증 중인 필드가 필수인지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

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
<!-- #### required_if_accepted:_anotherfield_,... -->
#### required_if_accepted:_anotherfield_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 `"yes"`, `"on"`, `1`, `"1"`, `true`, 또는 `"true"`와 같으면 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-if-declined"></a>
<!-- #### required_if_declined:_anotherfield_,... -->
#### required_if_declined:_anotherfield_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`와 같으면 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-unless"></a>
<!-- #### required_unless:_anotherfield_,_value_,... -->
#### required_unless:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data. -->
유효성 검증 중인 필드는 _anotherfield_ 필드가 어떤 _value_ 와 같지 않은 한 존재해야 하며 비어 있으면 안 됩니다. 이는 _value_ 가 `null`이 아닌 한 _anotherfield_ 도 요청 데이터에 존재해야 한다는 의미이기도 합니다. _value_ 가 `null`인 경우(`required_unless:name,null`), 비교 대상 필드가 `null`이거나 요청 데이터에 존재하지 않는 경우를 제외하고 유효성 검증 중인 필드는 필수입니다.

<a name="rule-required-with"></a>
<!-- #### required_with:_foo_,_bar_,... -->
#### required_with:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty. -->
유효성 검증 중인 필드는 지정된 다른 필드 중 하나라도 존재하고 비어 있지 않은 경우에만 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-with-all"></a>
<!-- #### required_with_all:_foo_,_bar_,... -->
#### required_with_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty. -->
유효성 검증 중인 필드는 지정된 다른 모든 필드가 존재하고 비어 있지 않은 경우에만 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-without"></a>
<!-- #### required_without:_foo_,_bar_,... -->
#### required_without:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present. -->
유효성 검증 중인 필드는 지정된 다른 필드 중 하나라도 비어 있거나 존재하지 않을 때에만 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-without-all"></a>
<!-- #### required_without_all:_foo_,_bar_,... -->
#### required_without_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present. -->
유효성 검증 중인 필드는 지정된 다른 모든 필드가 비어 있거나 존재하지 않을 때에만 존재해야 하며 비어 있으면 안 됩니다.

<a name="rule-required-array-keys"></a>
<!-- #### required_array_keys:_foo_,_bar_,... -->
#### required_array_keys:_foo_,_bar_,...

<!-- The field under validation must be an array and must contain at least the specified keys. -->
유효성 검증 중인 필드는 배열이어야 하며, 적어도 지정된 키들을 포함해야 합니다.

<a name="rule-same"></a>
<!-- #### same:_field_ -->
#### same:_field_

<!-- The given _field_ must match the field under validation. -->
주어진 _field_ 는 유효성 검증 중인 필드와 일치해야 합니다.

<a name="rule-size"></a>
<!-- #### size:_value_ -->
#### size:_value_

<!-- The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples: -->
유효성 검증 중인 필드는 주어진 _value_ 와 일치하는 크기를 가져야 합니다. 문자열 데이터의 경우 _value_ 는 문자 수에 해당합니다. 숫자 데이터의 경우 _value_ 는 주어진 정수 값에 해당합니다. 이때 해당 속성에는 `numeric` 또는 `integer` 규칙도 있어야 합니다. 배열의 경우 _size_ 는 배열의 `count`에 해당합니다. 파일의 경우 _size_ 는 킬로바이트 단위의 파일 크기에 해당합니다. 몇 가지 예를 살펴보겠습니다.

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
<!-- #### starts_with:_foo_,_bar_,... -->
#### starts_with:_foo_,_bar_,...

<!-- The field under validation must start with one of the given values. -->
유효성 검증 중인 필드는 주어진 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
<!-- #### string -->
#### string

<!-- The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field. -->
유효성 검증 중인 필드는 문자열이어야 합니다. 필드가 `null`도 허용되게 하려면 해당 필드에 `nullable` 규칙을 지정해야 합니다.

<a name="rule-timezone"></a>
<!-- #### timezone -->
#### timezone

<!-- The field under validation must be a valid timezone identifier according to the `DateTimeZone::listIdentifiers` method. -->
유효성 검증 중인 필드는 `DateTimeZone::listIdentifiers` 메서드 기준으로 유효한 시간대 식별자여야 합니다.

<!-- The arguments [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php) may also be provided to this validation rule: -->
[accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php)도 이 유효성 검증 규칙에 제공할 수 있습니다.

```php
'timezone' => 'required|timezone:all';

'timezone' => 'required|timezone:Africa';

'timezone' => 'required|timezone:per_country,US';
```

<a name="rule-unique"></a>
<!-- #### unique:_table_,_column_ -->
#### unique:_table_,_column_

<!-- The field under validation must not exist within the given database table. -->
유효성 검증 중인 필드는 주어진 데이터베이스 테이블 안에 존재해서는 안 됩니다.

<!-- **Specifying a Custom Table / Column Name:** -->
**커스텀 테이블 / 컬럼 이름 지정:**

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블 이름을 직접 지정하는 대신, 테이블 이름을 결정하는 데 사용할 Eloquent 모델을 지정할 수 있습니다.

```php
'email' => 'unique:App\Models\User,email_address'
```

<!-- The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used. -->
`column` 옵션을 사용하여 필드에 대응하는 데이터베이스 컬럼을 지정할 수 있습니다. `column` 옵션을 지정하지 않으면 유효성 검증 중인 필드의 이름이 사용됩니다.

```php
'email' => 'unique:users,email_address'
```

<!-- **Specifying a Custom Database Connection** -->
**커스텀 데이터베이스 연결 지정**

<!-- Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name: -->
때로는 Validator가 수행하는 데이터베이스 쿼리에 커스텀 연결을 설정해야 할 수 있습니다. 이를 위해 테이블 이름 앞에 연결 이름을 붙일 수 있습니다.

```php
'email' => 'unique:connection.users,email_address'
```

<!-- **Forcing a Unique Rule to Ignore a Given ID:** -->
**Unique 규칙이 주어진 ID를 무시하도록 강제하기:**

<!-- Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question. -->
때로는 unique 유효성 검증 중에 주어진 ID를 무시하고 싶을 수 있습니다. 예를 들어 사용자의 이름, 이메일 주소, 위치를 포함하는 "프로필 업데이트" 화면을 생각해 보겠습니다. 이메일 주소가 고유한지 확인하고 싶을 것입니다. 하지만 사용자가 이메일 필드는 변경하지 않고 이름 필드만 변경했다면, 해당 사용자가 이미 문제의 이메일 주소 소유자이므로 유효성 검증 오류가 발생하지 않아야 합니다.

<!-- To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules: -->
Validator가 사용자의 ID를 무시하도록 지시하려면 `Rule` 클래스를 사용하여 규칙을 유창하게 정의합니다. 이 예제에서는 규칙을 구분하기 위해 `|` 문자를 사용하는 대신, 유효성 검증 규칙도 배열로 지정합니다.

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
> 사용자가 제어할 수 있는 요청 입력값을 `ignore` 메서드에 절대 전달해서는 안 됩니다. 대신 Eloquent 모델 인스턴스의 자동 증가 ID나 UUID처럼 시스템이 생성한 고유 ID만 전달해야 합니다. 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해집니다.

<!-- Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model: -->
모델 키 값을 `ignore` 메서드에 전달하는 대신, 전체 모델 인스턴스를 전달할 수도 있습니다. Laravel은 모델에서 키를 자동으로 추출합니다.

```php
Rule::unique('users')->ignore($user)
```

<!-- If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method: -->
테이블이 `id`가 아닌 다른 기본 키 컬럼 이름을 사용한다면, `ignore` 메서드를 호출할 때 컬럼 이름을 지정할 수 있습니다.

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

<!-- By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method: -->
기본적으로 `unique` 규칙은 유효성 검증 중인 속성의 이름과 일치하는 컬럼의 고유성을 확인합니다. 그러나 `unique` 메서드의 두 번째 인수로 다른 컬럼 이름을 전달할 수 있습니다.

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

<!-- **Adding Additional Where Clauses:** -->
**추가 Where 절 추가:**

<!-- You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`: -->
`where` 메서드를 사용해 쿼리를 커스터마이즈하여 추가 쿼리 조건을 지정할 수 있습니다. 예를 들어 `account_id` 컬럼 값이 `1`인 레코드만 검색하도록 쿼리 범위를 제한하는 조건을 추가해 보겠습니다.

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

<!-- **Ignoring Soft Deleted Records in Unique Checks:** -->
**Unique 확인에서 소프트 삭제된 레코드 무시하기:**

<!-- By default, the unique rule includes soft deleted records when determining uniqueness. To exclude soft deleted records from the uniqueness check, you may invoke the `withoutTrashed` method: -->
기본적으로 unique 규칙은 고유성을 판단할 때 소프트 삭제된 레코드도 포함합니다. 고유성 확인에서 소프트 삭제된 레코드를 제외하려면 `withoutTrashed` 메서드를 호출할 수 있습니다.

```php
Rule::unique('users')->withoutTrashed();
```

<!-- If your model uses a column name other than `deleted_at` for soft deleted records, you may provide the column name when invoking the `withoutTrashed` method: -->
모델이 소프트 삭제된 레코드에 대해 `deleted_at`이 아닌 다른 컬럼 이름을 사용한다면, `withoutTrashed` 메서드를 호출할 때 컬럼 이름을 제공할 수 있습니다.

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
<!-- #### uppercase -->
#### uppercase

<!-- The field under validation must be uppercase. -->
유효성 검증 중인 필드는 대문자여야 합니다.

<a name="rule-url"></a>
<!-- #### url -->
#### url

<!-- The field under validation must be a valid URL. -->
유효성 검증 중인 필드는 유효한 URL이어야 합니다.

<!-- If you would like to specify the URL protocols that should be considered valid, you may pass the protocols as validation rule parameters: -->
유효한 것으로 간주할 URL 프로토콜을 지정하고 싶다면, 해당 프로토콜들을 유효성 검증 규칙 매개변수로 전달할 수 있습니다.

```php
'url' => 'url:http,https',

'game' => 'url:minecraft,steam',
```

<a name="rule-ulid"></a>
<!-- #### ulid -->
#### ulid

<!-- The field under validation must be a valid [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID). -->
유효성 검증 중인 필드는 유효한 [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec)(ULID)여야 합니다.

<a name="rule-uuid"></a>
<!-- #### uuid -->
#### uuid

<!-- The field under validation must be a valid RFC 9562 (version 1, 3, 4, 5, 6, 7, or 8) universally unique identifier (UUID). -->
유효성 검증 중인 필드는 유효한 RFC 9562(버전 1, 3, 4, 5, 6, 7 또는 8) 범용 고유 식별자(UUID)여야 합니다.

<!-- You may also validate that the given UUID matches a UUID specification by version: -->
또한 주어진 UUID가 버전별 UUID 사양과 일치하는지 검증할 수도 있습니다:

```php
'uuid' => 'uuid:4'
```

<a name="conditionally-adding-rules"></a>
<!-- ## Conditionally Adding Rules -->
## Conditionally Adding Rules

<a name="skipping-validation-when-fields-have-certain-values"></a>
<!-- #### Skipping Validation When Fields Have Certain Values -->
#### Skipping Validation When Fields Have Certain Values

<!-- You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`: -->
다른 필드가 특정 값을 가질 때 특정 필드를 검증하지 않고 싶을 때가 있습니다. 이 작업은 `exclude_if` 유효성 검증 규칙으로 수행할 수 있습니다. 이 예제에서는 `has_appointment` 필드의 값이 `false`이면 `appointment_date`와 `doctor_name` 필드는 유효성 검증을 받지 않습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

<!-- Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value: -->
또는 다른 필드가 특정 값을 가지지 않는 한 특정 필드를 검증하지 않으려면 `exclude_unless` 규칙을 사용할 수 있습니다:

```php
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
어떤 상황에서는 검증 대상 데이터에 해당 필드가 존재하는 경우에만 해당 필드에 대해 유효성 검증을 실행하고 싶을 수 있습니다. 이를 빠르게 처리하려면 규칙 목록에 `sometimes` 규칙을 추가합니다:

```php
$validator = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

<!-- In the example above, the `email` field will only be validated if it is present in the `$data` array. -->
위 예제에서 `email` 필드는 `$data` 배열에 존재하는 경우에만 유효성 검증됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드를 검증하려는 경우, [this note on optional fields](#a-note-on-optional-fields)을 확인하십시오.

<a name="complex-conditional-validation"></a>
<!-- #### Complex Conditional Validation -->
#### Complex Conditional Validation

<!-- Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change: -->
때로는 더 복잡한 조건 로직을 기준으로 유효성 검증 규칙을 추가하고 싶을 수 있습니다. 예를 들어, 다른 필드의 값이 100보다 클 때만 특정 필드를 필수로 만들고 싶을 수 있습니다. 또는 다른 필드가 존재할 때만 두 필드가 특정 값을 가져야 할 수도 있습니다. 이러한 유효성 검증 규칙을 추가하는 일은 어렵지 않습니다. 먼저 절대 변경되지 않는 _static rules(정적 규칙)_ 로 `Validator` 인스턴스를 생성합니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|integer|min:0',
]);
```

<!-- Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance. -->
우리 웹 애플리케이션이 게임 수집가를 위한 것이라고 가정해 보겠습니다. 게임 수집가가 애플리케이션에 가입하고 100개가 넘는 게임을 보유하고 있다면, 왜 그렇게 많은 게임을 보유하고 있는지 설명하도록 하고 싶습니다. 예를 들어, 게임 재판매 매장을 운영하고 있을 수도 있고, 단순히 게임 수집을 즐기는 사람일 수도 있습니다. 이 요구 사항을 조건부로 추가하려면 `Validator` 인스턴스의 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', 'required|max:500', function (Fluent $input) {
    return $input->games >= 100;
});
```

<!-- The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once: -->
`sometimes` 메서드에 전달되는 첫 번째 인수는 조건부로 검증할 필드의 이름입니다. 두 번째 인수는 추가하려는 규칙 목록입니다. 세 번째 인수로 전달된 클로저가 `true`를 반환하면 규칙이 추가됩니다. 이 메서드를 사용하면 복잡한 조건부 유효성 검증을 쉽게 구성할 수 있습니다. 여러 필드에 조건부 유효성 검증을 한 번에 추가할 수도 있습니다:

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> 클로저에 전달되는 `$input` 매개변수는 `Illuminate\Support\Fluent`의 인스턴스이며, 검증 중인 입력값과 파일에 접근하는 데 사용할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
<!-- #### Complex Conditional Array Validation -->
#### Complex Conditional Array Validation

<!-- Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated: -->
때로는 인덱스를 알 수 없는 동일한 중첩 배열 안의 다른 필드를 기준으로 특정 필드를 검증하고 싶을 수 있습니다. 이런 상황에서는 클로저가 두 번째 인수를 받을 수 있도록 할 수 있으며, 이 인수는 검증 중인 배열의 현재 개별 항목입니다:

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

<!-- Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string. -->
클로저에 전달되는 `$input` 매개변수와 마찬가지로, 속성 데이터가 배열이면 `$item` 매개변수는 `Illuminate\Support\Fluent`의 인스턴스입니다. 그렇지 않으면 문자열입니다.

<a name="validating-arrays"></a>
<!-- ## Validating Arrays -->
## Validating Arrays

<!-- As discussed in the [array validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail: -->
[array validation rule documentation](#rule-array)에서 설명한 것처럼, `array` 규칙은 허용되는 배열 키 목록을 받습니다. 배열 안에 추가 키가 존재하면 유효성 검증은 실패합니다:

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

<!-- In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules. -->
일반적으로 배열 안에 존재할 수 있는 배열 키를 항상 명시해야 합니다. 그렇지 않으면 다른 중첩 배열 유효성 검증 규칙으로 검증되지 않은 키가 있더라도, 유효성 검증기의 `validate`와 `validated` 메서드는 배열과 그 모든 키를 포함한 검증된 데이터 전체를 반환합니다.

<a name="validating-nested-array-input"></a>
<!-- ### Validating Nested Array Input -->
### Validating Nested Array Input

<!-- Validating nested array-based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so: -->
중첩된 배열 기반 폼 입력 필드를 검증하는 일은 어렵지 않습니다. 배열 안의 속성을 검증하려면 "점 표기법"을 사용할 수 있습니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]` 필드가 포함되어 있다면 다음과 같이 검증할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

<!-- You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following: -->
배열의 각 요소도 검증할 수 있습니다. 예를 들어, 특정 배열 입력 필드의 각 이메일이 고유한지 검증하려면 다음과 같이 할 수 있습니다:

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => 'email|unique:users',
    'users.*.first_name' => 'required_with:users.*.last_name',
]);
```

<!-- Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array-based fields: -->
마찬가지로 [custom validation messages in your language files](#custom-messages-for-specific-attributes)를 지정할 때 `*` 문자를 사용할 수 있으므로, 배열 기반 필드에 하나의 유효성 검증 메시지를 쉽게 사용할 수 있습니다:

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
<!-- #### Accessing Nested Array Data -->
#### Accessing Nested Array Data

<!-- Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element: -->
속성에 유효성 검증 규칙을 할당할 때 특정 중첩 배열 요소의 값에 접근해야 할 때가 있습니다. 이 작업은 `Rule::forEach` 메서드를 사용하여 수행할 수 있습니다. `forEach` 메서드는 검증 중인 배열 속성을 반복할 때마다 호출되는 클로저를 받으며, 이 클로저는 속성의 값과 명시적으로 완전히 확장된 속성 이름을 받습니다. 클로저는 배열 요소에 할당할 규칙 배열을 반환해야 합니다:

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
<!-- ### Error Message Indexes and Positions -->
### Error Message Indexes and Positions

<!-- When validating arrays, you may want to reference the index or position of a particular item that failed validation within the error message displayed by your application. To accomplish this, you may include the `:index` (starts from `0`), `:position` (starts from `1`), or `:ordinal-position` (starts from `1st`) placeholders within your [custom validation message](#manual-customizing-the-error-messages): -->
배열을 검증할 때 애플리케이션에 표시되는 오류 메시지 안에서 유효성 검증에 실패한 특정 항목의 인덱스나 위치를 참조하고 싶을 수 있습니다. 이를 위해 [custom validation message](#manual-customizing-the-error-messages)에 `:index`(`0`부터 시작), `:position`(`1`부터 시작), 또는 `:ordinal-position`(`1st`부터 시작) 플레이스홀더를 포함할 수 있습니다:

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

<!-- Given the example above, validation will fail and the user will be presented with the following error of _"Please describe photo #2."_ -->
위 예제에서는 유효성 검증이 실패하고, 사용자에게 _"Please describe photo #2."_ 라는 오류가 표시됩니다.

<!-- If necessary, you may reference more deeply nested indexes and positions via `second-index`, `second-position`, `third-index`, `third-position`, etc. -->
필요하다면 `second-index`, `second-position`, `third-index`, `third-position` 등을 통해 더 깊게 중첩된 인덱스와 위치를 참조할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
<!-- ## Validating Files -->
## Validating Files

<!-- Laravel provides a variety of validation rules that may be used to validate uploaded files, such as `mimes`, `image`, `min`, and `max`. While you are free to specify these rules individually when validating files, Laravel also offers a fluent file validation rule builder that you may find convenient: -->
Laravel은 업로드된 파일을 검증하는 데 사용할 수 있는 `mimes`, `image`, `min`, `max` 같은 다양한 유효성 검증 규칙을 제공합니다. 파일을 검증할 때 이러한 규칙을 각각 지정해도 되지만, Laravel은 편리하게 사용할 수 있는 유창한 파일 유효성 검증 규칙 빌더도 제공합니다:

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
<!-- #### Validating File Types -->
#### Validating File Types

<!-- Even though you only need to specify the extensions when invoking the `types` method, this method actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
`types` 메서드를 호출할 때는 확장자만 지정하면 되지만, 이 메서드는 실제로 파일의 내용을 읽고 MIME 타입을 추정하여 파일의 MIME 타입을 검증합니다. MIME 타입과 그에 대응하는 확장자의 전체 목록은 다음 위치에서 확인할 수 있습니다:

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
<!-- #### Validating File Sizes -->
#### Validating File Sizes

<!-- For convenience, minimum and maximum file sizes may be specified as a string with a suffix indicating the file size units. The `kb`, `mb`, `gb`, and `tb` suffixes are supported: -->
편의를 위해 최소 및 최대 파일 크기는 파일 크기 단위를 나타내는 접미사가 붙은 문자열로 지정할 수 있습니다. `kb`, `mb`, `gb`, `tb` 접미사가 지원됩니다:

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
<!-- #### Validating Image Files -->
#### Validating Image Files

<!-- If your application accepts images uploaded by your users, you may use the `File` rule's `image` constructor method to ensure that the file under validation is an image (jpg, jpeg, png, bmp, gif, or webp). -->
애플리케이션이 사용자가 업로드한 이미지를 받는다면, 검증 중인 파일이 이미지(jpg, jpeg, png, bmp, gif, 또는 webp)인지 확인하기 위해 `File` 규칙의 `image` 생성자 메서드를 사용할 수 있습니다.

<!-- In addition, the `dimensions` rule may be used to limit the dimensions of the image: -->
또한 `dimensions` 규칙을 사용하여 이미지의 크기를 제한할 수 있습니다:

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
> 이미지 크기 유효성 검증에 대한 자세한 정보는 [dimension rule documentation](#rule-dimensions)에서 확인할 수 있습니다.

> [!WARNING]
> 기본적으로 `image` 규칙은 XSS 취약점 가능성 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 한다면 `image` 규칙에 `allowSvg: true`를 전달할 수 있습니다: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
<!-- #### Validating Image Dimensions -->
#### Validating Image Dimensions

<!-- You may also validate the dimensions of an image. For example, to validate that an uploaded image is at least 1000 pixels wide and 500 pixels tall, you may use the `dimensions` rule: -->
이미지의 크기도 검증할 수 있습니다. 예를 들어, 업로드된 이미지의 너비가 최소 1000픽셀이고 높이가 최소 500픽셀인지 검증하려면 `dimensions` 규칙을 사용할 수 있습니다:

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
> 이미지 크기 유효성 검증에 대한 자세한 정보는 [dimension rule documentation](#rule-dimensions)에서 확인할 수 있습니다.

<a name="validating-passwords"></a>
<!-- ## Validating Passwords -->
## Validating Passwords

<!-- To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object: -->
비밀번호가 충분한 수준의 복잡성을 갖도록 하려면 Laravel의 `Password` 규칙 객체를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

<!-- The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing: -->
`Password` 규칙 객체를 사용하면 비밀번호에 최소 하나의 문자, 숫자, 기호 또는 대소문자가 섞인 문자가 필요하다는 식으로 애플리케이션의 비밀번호 복잡도 요구 사항을 쉽게 사용자 정의할 수 있습니다:

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

<!-- In addition, you may ensure that a password has not been compromised in a public password data breach leak using the `uncompromised` method: -->
또한 `uncompromised` 메서드를 사용하여 공개 비밀번호 데이터 유출에서 비밀번호가 노출되지 않았는지 확인할 수 있습니다:

```php
Password::min(8)->uncompromised()
```

<!-- Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security. -->
내부적으로 `Password` 규칙 객체는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 모델을 사용하여, 사용자의 개인정보나 보안을 희생하지 않고 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호가 유출되었는지 판단합니다.

<!-- By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method: -->
기본적으로 비밀번호가 데이터 유출에 최소 한 번이라도 나타나면 손상된 것으로 간주됩니다. `uncompromised` 메서드의 첫 번째 인수를 사용하여 이 임계값을 사용자 정의할 수 있습니다:

```php
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

<!-- Of course, you may chain all the methods in the examples above: -->
물론 위 예제의 모든 메서드를 체이닝할 수 있습니다:

```php
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
애플리케이션의 한 위치에서 비밀번호에 대한 기본 유효성 검증 규칙을 지정하면 편리할 수 있습니다. 클로저를 받는 `Password::defaults` 메서드를 사용하면 이를 쉽게 수행할 수 있습니다. `defaults` 메서드에 전달되는 클로저는 Password 규칙의 기본 구성을 반환해야 합니다. 일반적으로 `defaults` 규칙은 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 안에서 호출해야 합니다:

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
그런 다음 유효성 검증 중인 특정 비밀번호에 기본 규칙을 적용하고 싶을 때는 인수 없이 `defaults` 메서드를 호출하면 됩니다:

```php
'password' => ['required', Password::defaults()],
```

<!-- Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this: -->
때때로 기본 비밀번호 유효성 검증 규칙에 추가 유효성 검증 규칙을 붙이고 싶을 수 있습니다. 이 작업은 `rules` 메서드를 사용하여 수행할 수 있습니다:
```php
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
Laravel은 다양한 유용한 유효성 검증 규칙을 제공합니다. 하지만 직접 규칙을 정의하고 싶을 수도 있습니다. 사용자 정의 유효성 검증 규칙을 등록하는 한 가지 방법은 규칙 객체를 사용하는 것입니다. 새 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용할 수 있습니다. 이 명령어를 사용해 문자열이 대문자인지 확인하는 규칙을 만들어 보겠습니다. Laravel은 새 규칙을 `app/Rules` 디렉터리에 배치합니다. 이 디렉터리가 없으면, 규칙을 생성하는 Artisan 명령어를 실행할 때 Laravel이 디렉터리를 생성합니다.

```shell
php artisan make:rule Uppercase
```

<!-- Once the rule has been created, we are ready to define its behavior. A rule object contains a single method: `validate`. This method receives the attribute name, its value, and a callback that should be invoked on failure with the validation error message: -->
규칙이 생성되면 이제 동작을 정의할 수 있습니다. 규칙 객체에는 `validate`라는 단일 메서드가 포함됩니다. 이 메서드는 속성 이름, 값, 그리고 유효성 검증 실패 시 유효성 검증 오류 메시지와 함께 호출해야 하는 콜백을 받습니다.

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

<!-- Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules: -->
규칙이 정의되면, 다른 유효성 검증 규칙과 함께 규칙 객체의 인스턴스를 전달하여 validator에 연결할 수 있습니다.

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

<!-- #### Translating Validation Messages -->
#### Translating Validation Messages

<!-- Instead of providing a literal error message to the `$fail` closure, you may also provide a [translation string key](/docs/master/localization) and instruct Laravel to translate the error message: -->
`$fail` 클로저에 문자 그대로의 오류 메시지를 제공하는 대신, [translation string key](/docs/master/localization)를 제공하고 Laravel이 오류 메시지를 번역하도록 지시할 수도 있습니다.

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

<!-- If necessary, you may provide placeholder replacements and the preferred language as the first and second arguments to the `translate` method: -->
필요한 경우, `translate` 메서드의 첫 번째 및 두 번째 인수로 플레이스홀더 대체값과 선호 언어를 제공할 수 있습니다.

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

<!-- #### Accessing Additional Data -->
#### Accessing Additional Data

<!-- If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation: -->
사용자 정의 유효성 검증 규칙 클래스가 유효성 검증 중인 다른 모든 데이터에 접근해야 한다면, 규칙 클래스는 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스는 클래스가 `setData` 메서드를 정의하도록 요구합니다. 이 메서드는 Laravel에 의해 유효성 검증이 진행되기 전에 자동으로 호출되며, 유효성 검증 대상인 모든 데이터를 전달받습니다.

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

<!-- Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface: -->
또는, 유효성 검증 규칙이 유효성 검증을 수행하는 validator 인스턴스에 접근해야 한다면 `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

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
<!-- ### Using Closures -->
### Using Closures

<!-- If you only need the functionality of a custom rule once throughout your application, you may use a closure instead of a rule object. The closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails: -->
애플리케이션 전체에서 사용자 정의 규칙의 기능이 한 번만 필요하다면, 규칙 객체 대신 클로저를 사용할 수 있습니다. 클로저는 속성 이름, 속성 값, 그리고 유효성 검증이 실패할 경우 호출해야 하는 `$fail` 콜백을 받습니다.

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
<!-- ### Implicit Rules -->
### Implicit Rules

<!-- By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the [unique](#rule-unique) rule will not be run against an empty string: -->
기본적으로 유효성 검증 중인 속성이 존재하지 않거나 빈 문자열을 포함하는 경우, 사용자 정의 규칙을 포함한 일반 유효성 검증 규칙은 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에 대해서는 실행되지 않습니다.

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

<!-- For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To quickly generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option: -->
속성이 비어 있어도 사용자 정의 규칙이 실행되도록 하려면, 해당 규칙은 속성이 필수임을 암묵적으로 나타내야 합니다. 새 암묵적 규칙 객체를 빠르게 생성하려면 `--implicit` 옵션과 함께 `make:rule` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> "암묵적" 규칙은 속성이 필수임을 _암시할_ 뿐입니다. 누락되었거나 비어 있는 속성을 실제로 유효하지 않다고 판단할지는 여러분이 정해야 합니다.
