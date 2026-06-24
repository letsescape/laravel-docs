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
    - [Excluding Unvalidated Array Keys](#excluding-unvalidated-array-keys)
    - [Validating Nested Array Input](#validating-nested-array-input)
- [Validating Passwords](#validating-passwords)
- [Custom Validation Rules](#custom-validation-rules)
    - [Using Rule Objects](#using-rule-objects)
    - [Using Closures](#using-closures)
    - [Implicit Rules](#implicit-rules)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well. -->
Laravel은 애플리케이션의 입력 데이터를 유효성 검증하는 여러 가지 다양한 방법을 제공합니다. 가장 일반적으로는 모든 들어오는 HTTP 요청에서 사용할 수 있는 `validate` 메서드를 활용합니다. 하지만 이외에도 여러 가지 다른 유효성 검증 방식에 대해서도 이 문서에서 다룹니다.

<!-- Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features. -->
Laravel에는 다양한 간편한 유효성 검증 규칙이 내장되어 있으며, 데이터가 데이터베이스의 특정 테이블 내에서 유일한지까지 손쉽게 검증할 수 있습니다. 본 문서에서는 각 유효성 검증 규칙에 대해 꼼꼼하게 설명하여, Laravel의 유효성 검증 기능을 완벽하게 익힐 수 있도록 안내합니다.

<a name="validation-quickstart"></a>
<!-- ## Validation Quickstart -->
## Validation Quickstart

<!-- To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel: -->
Laravel의 강력한 유효성 검증 기능을 이해하기 위해, 폼을 검증하고 오류 메시지를 사용자에게 보여주는 전체 흐름을 단계별로 살펴보겠습니다. 이 내용을 먼저 읽어보면 Laravel에서 들어오는 요청 데이터를 어떻게 유효성 검증하는지 전반적인 큰 흐름을 쉽게 파악할 수 있습니다.

<a name="quick-defining-the-routes"></a>
<!-- ### Defining The Routes -->
### Defining The Routes

<!-- First, let's assume we have the following routes defined in our `routes/web.php` file: -->
먼저, `routes/web.php` 파일에 다음과 같이 라우트가 정의되어 있다고 가정해 봅시다.

```
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

<!-- The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database. -->
위 예시에서 `GET` 라우트는 사용자가 새로운 블로그 게시글을 작성할 수 있는 폼을 보여주고, `POST` 라우트는 사용자가 작성한 새 블로그 게시글을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
<!-- ### Creating The Controller -->
### Creating The Controller

<!-- Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now: -->
다음으로, 위 라우트에서 들어온 요청을 처리하는 간단한 컨트롤러를 만들어 봅시다. 여기서 `store` 메서드는 아직 비워둡니다.

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
이제 `store` 메서드에 새 블로그 게시글을 검증하는 로직을 작성해봅시다. 이를 위해서는 `Illuminate\Http\Request` 객체에서 제공하는 `validate` 메서드를 사용하면 됩니다. 만약 유효성 검증 규칙을 모두 통과하면, 코드가 정상적으로 계속 실행됩니다. 하지만 검증 실패 시에는 `Illuminate\Validation\ValidationException` 예외가 발생하며, 자동으로 올바른 오류 응답이 사용자에게 반환됩니다.

<!-- If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a JSON response containing the validation error messages will be returned. -->
만약 전통적인 HTTP 요청 방식이라면, 검증 실패 시 이전 URL로 리다이렉트 응답이 생성됩니다. 요청이 XHR 방식이라면, 유효성 검증 오류 메시지를 담은 JSON 응답이 반환됩니다.

<!-- To get a better understanding of the `validate` method, let's jump back into the `store` method: -->
`validate` 메서드가 실제로 어떻게 동작하는지 `store` 메서드로 돌아가 직접 살펴봅시다.

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
위에서 볼 수 있듯, 유효성 검증 규칙은 `validate` 메서드에 배열로 전달됩니다. 걱정하지 마세요 - 모든 사용 가능한 유효성 검증 규칙은 [documented](#available-validation-rules). 다시 한번, 검증에 실패하면 적절한 응답이 자동으로 생성됩니다. 만약 검증에 성공한다면, 컨트롤러는 정상적으로 실행을 계속합니다.

<!-- Alternatively, validation rules may be specified as arrays of rules instead of a single `|` delimited string: -->
또한, 규칙을 단일 `|` 구분 문자열 대신 배열 형태로 지정할 수도 있습니다.

```
$validatedData = $request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<!-- In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a [named error bag](#named-error-bags): -->
또한, [named error bag](#named-error-bags)을 사용하고 싶다면 `validateWithBag` 메서드를 이용해 각 요청에 대한 검증 오류 메시지를 저장할 수 있습니다.

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
특정 속성(attribute)에서 한 번이라도 검증에 실패하면, 이후 해당 속성에 대해 더 이상 검증하지 않고 멈추길 원할 수 있습니다. 이럴 때는 해당 속성에 `bail` 규칙을 추가해 주세요.

```
$request->validate([
    'title' => 'bail|required|unique:posts|max:255',
    'body' => 'required',
]);
```

<!-- In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned. -->
이 예시에서 `title` 속성에 대해 `unique` 규칙이 실패하면, `max` 규칙은 더 이상 확인하지 않습니다. 규칙들은 작성한 순서대로 차례로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
<!-- #### A Note On Nested Attributes -->
#### A Note On Nested Attributes

<!-- If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax: -->
만약 들어오는 HTTP 요청에 '중첩된' 필드 데이터가 있다면, 검증 규칙에서 '닷(dot) 표기법'을 사용해 이런 필드를 지정할 수 있습니다.

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'author.name' => 'required',
    'author.description' => 'required',
]);
```

<!-- On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash: -->
반면에, 필드 이름 자체에 온점(닷)이 포함된 경우에는, 역슬래시(\)로 닷을 이스케이프하면 "닷 표기법"이 아닌 문자 그대로의 온점으로 인식됩니다.

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'v1\.0' => 'required',
]);
```

<a name="quick-displaying-the-validation-errors"></a>
<!-- ### Displaying The Validation Errors -->
### Displaying The Validation Errors

<!-- So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/8.x/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/8.x/session#flash-data). -->
그렇다면, 들어온 요청 필드가 지정한 검증 규칙을 통과하지 못하면 어떻게 될까요? 앞에서 언급한 것처럼, Laravel은 자동으로 사용자를 이전 위치로 리다이렉트합니다. 그리고 모든 유효성 검증 오류와 [request input](/docs/8.x/requests#retrieving-old-input)이 자동으로 [flashed to the session](/docs/8.x/session#flash-data)됩니다.

<!-- An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages). -->
`Illuminate\View\Middleware\ShareErrorsFromSession` 미들웨어가 `$errors` 변수를 모든 뷰에 자동으로 공유해줍니다. 이 미들웨어는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으므로, 별다른 설정 없이도 모든 뷰에서 `$errors` 변수를 언제든지 사용할 수 있고 `$errors` 변수가 항상 정의되어 있다고 가정할 수 있습니다. `$errors` 변수는 `Illuminate\Support\MessageBag`의 인스턴스입니다. 이 객체를 다루는 방법은 [check out its documentation](#working-with-error-messages)에서 자세히 설명합니다.

<!-- So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view: -->
따라서, 이 예시에서는 검증 실패 시 컨트롤러의 `create` 메서드로 다시 리다이렉트되며, 뷰에서 오류 메시지를 아래와 같이 표시할 수 있습니다:

```html
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

<!-- Laravel's built-in validation rules each has an error message that is located in your application's `resources/lang/en/validation.php` file. Within this file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
Laravel 내장 유효성 검증 규칙마다 오류 메시지가 함께 제공되며, 이 메시지는 애플리케이션의 `resources/lang/en/validation.php` 파일에 위치합니다. 해당 파일에서 각 유효성 검증 규칙에 대한 번역 항목을 확인할 수 있습니다. 애플리케이션의 필요에 따라, 메시지를 자유롭게 수정하거나 변경할 수 있습니다.

<!-- In addition, you may copy this file to another translation language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/8.x/localization). -->
또한, 이 파일을 다른 언어 디렉터리로 복사해 메시지를 번역할 수도 있습니다. Laravel의 로컬라이제이션에 대해 더 자세히 알고 싶다면 [localization documentation](/docs/8.x/localization)를 참고해 주세요.

<a name="quick-xhr-requests-and-validation"></a>
<!-- #### XHR Requests & Validation -->
#### XHR Requests & Validation

<!-- In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a JSON response containing all of the validation errors. This JSON response will be sent with a 422 HTTP status code. -->
이 예시에서는 전통적인 폼을 통해 데이터를 애플리케이션으로 전송했습니다. 하지만, 많은 현대 애플리케이션에서는 자바스크립트 기반 프론트엔드에서 XHR 요청을 보냅니다. 이런 경우, `validate` 메서드를 사용할 때 Laravel은 리다이렉트 대신 모든 유효성 검증 오류를 포함한 JSON 응답을 반환합니다. 이 응답은 HTTP 상태 코드 422와 함께 전송됩니다.

<a name="the-at-error-directive"></a>
<!-- #### The `@error` Directive -->
#### The `@error` Directive

<!-- You may use the `@error` [Blade](/docs/8.x/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
주어진 속성에 대해 유효성 검증 오류 메시지가 존재하는지 빠르게 확인하려면 [Blade](/docs/8.x/blade)에서 `@error` 디렉티브를 사용할 수 있습니다. `@error` 블록 내부에서는 `$message` 변수를 출력해 오류 메시지를 표시할 수 있습니다.

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title" type="text" name="title" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- If you are using [named error bags](#named-error-bags), you may pass the name of the error bag as the second argument to the `@error` directive: -->
[named error bags](#named-error-bags)을 사용하는 경우, 두 번째 인자로 에러 백의 이름을 `@error` 디렉티브에 전달할 수 있습니다:

```html
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
<!-- ### Repopulating Forms -->
### Repopulating Forms

<!-- When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/8.x/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit. -->
Laravel이 유효성 검증 오류로 인해 리다이렉트를 생성할 때, 프레임워크는 자동으로 [flash all of the request's input to the session](/docs/8.x/session#flash-data)합니다. 덕분에, 사용자는 바로 다음 요청에서 이전에 입력한 데이터에 접근할 수 있어, 제출 직전의 폼을 그대로 다시 보여주거나 일부 값을 자동으로 채우는 데 매우 편리합니다.

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/8.x/session): -->
이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출하면 됩니다. `old` 메서드는 [session](/docs/8.x/session)에 보관된 플래시 입력값을 꺼내줍니다:

```
$title = $request->old('title');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/8.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel은 전역 헬퍼 함수인 `old`도 제공합니다. 뷰(특히 [Blade template](/docs/8.x/blade))에서 이전 입력값을 표시할 때, 이 `old` 헬퍼를 사용하면 훨씬 편리하게 폼 값을 다시 채울 수 있습니다. 해당 필드에 이전 입력값이 없다면, `null`이 반환됩니다.

```
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
<!-- ### A Note On Optional Fields -->
### A Note On Optional Fields

<!-- By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware are listed in the stack by the `App\Http\Kernel` class. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example: -->
기본적으로, Laravel은 전역 미들웨어 스택에 `TrimStrings`와 `ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이들은 `App\Http\Kernel` 클래스에서 정의되어 있습니다. 그래서, 선택(필수 아님) 필드에 대해 값이 `null`일 때도 검증에서 오류가 나길 원하지 않는다면 해당 필드를 반드시 `nullable`로 지정해야 합니다. 예를 들면 다음과 같습니다.

```
$request->validate([
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
    'publish_at' => 'nullable|date',
]);
```

<!-- In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date. -->
위 예시에서, `publish_at` 필드는 `null`이거나 올바른 날짜 형식이어야 합니다. 만약 `nullable`을 추가하지 않으면, 검증기는 `null`을 잘못된 날짜로 간주해 검증에 실패할 수 있습니다.

<a name="form-request-validation"></a>
<!-- ## Form Request Validation -->
## Form Request Validation

<a name="creating-form-requests"></a>
<!-- ### Creating Form Requests -->
### Creating Form Requests

<!-- For more complex validation scenarios, you may wish to create a "form request". Form requests are custom request classes that encapsulate their own validation and authorization logic. To create a form request class, you may use the `make:request` Artisan CLI command: -->
더 복잡한 유효성 검증이 필요한 경우, "폼 리퀘스트(form request)"라는 방식을 사용할 수 있습니다. 폼 리퀘스트는 자체적으로 유효성 검증 및 인가(authorization) 로직을 캡슐화한 커스텀 요청 클래스입니다. 폼 리퀘스트 클래스를 만들려면 `make:request` 아티즌 CLI 명령어를 사용하세요.

```
php artisan make:request StorePostRequest
```

<!-- The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`. -->
생성된 폼 리퀘스트 클래스는 `app/Http/Requests` 디렉터리에 위치합니다. 이 디렉터리가 없으면, `make:request` 명령어 실행 시 자동으로 생성됩니다. Laravel에서 만들어진 각 폼 리퀘스트는 `authorize`와 `rules`라는 두 가지 메서드를 포함합니다.

<!-- As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data: -->
예상하신 대로, `authorize` 메서드는 현재 인증된 사용자가 해당 요청에서 나타내는 동작을 할 수 있는지 판단하는 역할을 하며, `rules` 메서드는 요청 데이터에 적용해야 할 유효성 검증 규칙을 반환합니다:

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

> [!TIP]
> `rules` 메서드의 시그니처에 필요한 의존성을 타입힌트 할 수 있습니다. 이를 통해 의존성이 Laravel [service container](/docs/8.x/container)에서 자동으로 주입됩니다.

<!-- So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic: -->
그럼 이러한 규칙들은 어떻게 평가될까요? 컨트롤러 메서드에서 해당 요청 클래스를 타입힌트(명시적 매개변수로 선언)해주면 됩니다. 폼 리퀘스트가 들어오면, 컨트롤러 메서드가 호출되기 전에 자동으로 유효성 검증이 이뤄지기 때문에 컨트롤러가 지저분해질 걱정 없이 검증을 적용할 수 있습니다.

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

<!-- If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a JSON representation of the validation errors. -->
만약 유효성 검증에 실패하면, 자동으로 이전 페이지로 리다이렉트되는 응답이 생성됩니다. 오류 메시지는 세션에 flash 처리되어 뷰에서 쉽게 표시할 수 있습니다. 만약 요청이 XHR 방식이라면, 422 상태 코드를 포함한 JSON 형태로 오류 정보가 반환됩니다.

<a name="adding-after-hooks-to-form-requests"></a>
<!-- #### Adding After Hooks To Form Requests -->
#### Adding After Hooks To Form Requests

<!-- If you would like to add an "after" validation hook to a form request, you may use the `withValidator` method. This method receives the fully constructed validator, allowing you to call any of its methods before the validation rules are actually evaluated: -->
폼 리퀘스트에서 "after" 유효성 검증 훅을 추가하고 싶다면 `withValidator` 메서드를 사용할 수 있습니다. 이 메서드는 완전히 구성된 validator 객체를 전달받으므로, 실제 규칙이 평가되기 전에 validator의 다양한 메서드를 호출해 추가 로직을 넣을 수 있습니다.

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
폼 리퀘스트 클래스에 `stopOnFirstFailure` 프로퍼티를 추가함으로써, 하나의 유효성 검증 실패가 발생하면 모든 속성(attribute)에 대한 추가 검증을 멈추도록 validator에 알릴 수 있습니다.

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
앞서 설명한 대로, 폼 리퀘스트 검증에 실패하면 사용자를 이전 위치로 리다이렉트하게 됩니다. 하지만 이 동작은 필요에 따라 자유롭게 커스터마이즈할 수 있습니다. 이를 위해서 폼 리퀘스트에 `$redirect` 프로퍼티를 정의하면 됩니다.

```
/**
 * The URI that users should be redirected to if validation fails.
 *
 * @var string
 */
protected $redirect = '/dashboard';
```

<!-- Or, if you would like to redirect users to a named route, you may define a `$redirectRoute` property instead: -->
또는, 네임드 라우트로 리다이렉트하고 싶다면 `$redirectRoute` 프로퍼티를 대신 정의할 수 있습니다.

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

<!-- The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/8.x/authorization) within this method: -->
폼 리퀘스트 클래스에는 `authorize` 메서드도 함께 존재합니다. 이 메서드에서는 현재 인증된 사용자가 해당 리소스를 실제로 수정 등 업데이트할 권한이 있는지 판단할 수 있습니다. 예를 들면 사용자가 자신이 소유한 블로그 댓글만 수정할 수 있도록 인가 체크 코드를 추가할 수 있습니다. 보통은 이 안에서 [authorization gates and policies](/docs/8.x/authorization)을 활용합니다.

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
모든 폼 리퀘스트는 기본 Laravel 요청 클래스를 확장하므로, `user` 메서드를 사용해 현재 인증된 사용자에 접근할 수 있습니다. 위 예시에서 `route` 메서드를 사용한 부분에 주목해 주세요. 이 메서드는 현재 호출 중인 라우트에서 정의된 URI 파라미터(`{comment}` 등)에 접근하는 데 유용합니다.

```
Route::post('/comment/{comment}');
```

<!-- Therefore, if your application is taking advantage of [route model binding](/docs/8.x/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request: -->
따라서, [route model binding](/docs/8.x/routing#route-model-binding)을 사용하고 있다면, 요청의 속성으로 바로 바인딩된 모델을 더 간결하게 사용할 수 있습니다.

```
return $this->user()->can('update', $this->comment);
```

<!-- If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute. -->
`authorize` 메서드가 `false`를 반환하면, 자동으로 403 상태 코드의 HTTP 응답이 반환되며, 컨트롤러 메서드는 아예 실행되지 않습니다.

<!-- If you plan to handle authorization logic for the request in another part of your application, you may simply return `true` from the `authorize` method: -->
요청에 대한 인가 로직을 애플리케이션의 다른 곳에서 처리할 예정이라면, `authorize` 메서드에서 간단히 `true`만 반환해도 괜찮습니다.

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

> [!TIP]
> `authorize` 메서드 시그니처에 필요한 의존성을 타입힌트로 선언할 수 있습니다. 이 경우 의존성은 Laravel [service container](/docs/8.x/container)에서 자동으로 주입됩니다.

<a name="customizing-the-error-messages"></a>
<!-- ### Customizing The Error Messages -->
### Customizing The Error Messages

<!-- You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages: -->
폼 리퀘스트에서 사용하는 오류 메시지는 `messages` 메서드를 오버라이드하여 자유롭게 변경할 수 있습니다. 이 메서드는 attribute / rule 쌍과 각각의 오류 메시지가 담긴 배열을 반환하면 됩니다.

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
Laravel 내장 유효성 검증 오류 메시지 중에는 `:attribute` 플레이스홀더를 포함하는 경우가 많습니다. 이 `:attribute` 플레이스홀더를 원하는 속성명으로 바꾸고 싶다면, `attributes` 메서드를 오버라이드해 직접 지정할 수 있습니다. 이 메서드는 attribute / name 쌍의 배열을 반환해야 합니다.

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
검증 규칙을 적용하기 전에 요청 데이터 일부를 사전 처리(가공/정제)해야 한다면, `prepareForValidation` 메서드를 활용할 수 있습니다.

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

<a name="manually-creating-validators"></a>
<!-- ## Manually Creating Validators -->
## Manually Creating Validators

<!-- If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/8.x/facades). The `make` method on the facade generates a new validator instance: -->
요청 객체의 `validate` 메서드를 사용하고 싶지 않다면, `Validator` [facade](/docs/8.x/facades)를 사용해 validator 인스턴스를 직접 생성할 수도 있습니다. 파사드의 `make` 메서드는 새로운 validator 인스턴스를 만듭니다.

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
`make` 메서드의 첫 번째 인자는 검증할 데이터이고, 두 번째 인자는 데이터에 적용할 유효성 검증 규칙 배열입니다.

<!-- After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`. -->
요청 데이터 검증 결과 실패했는지 확인한 뒤, `withErrors` 메서드를 사용해 오류 메시지를 세션에 flash할 수 있습니다. 이 메서드를 사용하면, 뷰에서 `$errors` 변수가 자동으로 공유되므로, 사용자에게 오류 메시지를 간편하게 다시 보여줄 수 있습니다. `withErrors` 메서드는 validator, `MessageBag`, 또는 PHP `array`를 인자로 받을 수 있습니다.

<!-- #### Stopping On First Validation Failure -->
#### Stopping On First Validation Failure

<!-- The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`stopOnFirstFailure` 메서드는 하나의 속성에서 유효성 검증이 실패하면, 모든 속성에 대한 추가 검증을 중단하도록 검증기(validator)에게 알립니다.

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
<!-- ### Automatic Redirection -->
### Automatic Redirection

<!-- If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a JSON response will be returned: -->
직접 검증기 인스턴스를 생성하면서도, HTTP 요청의 `validate` 메서드가 제공하는 자동 리디렉션 기능을 활용하고 싶다면, 이미 생성한 검증기 인스턴스에서 `validate` 메서드를 호출하면 됩니다. 유효성 검증이 실패할 경우 사용자는 자동으로 리디렉션되거나, XHR 요청의 경우 JSON 응답이 반환됩니다.

```
Validator::make($request->all(), [
    'title' => 'required|unique:posts|max:255',
    'body' => 'required',
])->validate();
```

<!-- You may use the `validateWithBag` method to store the error messages in a [named error bag](#named-error-bags) if validation fails: -->
유효성 검증 실패 시 [named error bag](#named-error-bags)에 에러 메시지를 저장하고 싶다면 `validateWithBag` 메서드를 사용할 수 있습니다.

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
한 페이지에 여러 개의 폼이 있다면, 해당 폼의 유효성 검증 에러를 담는 `MessageBag`에 이름을 붙이고 싶을 때가 있습니다. 이렇게 하면 특정 폼에 해당하는 에러 메시지를 쉽게 가져올 수 있습니다. 이를 위해 `withErrors`의 두 번째 인자로 이름을 전달하면 됩니다.

```
return redirect('register')->withErrors($validator, 'login');
```

<!-- You may then access the named `MessageBag` instance from the `$errors` variable: -->
그런 다음, `$errors` 변수에서 이름이 지정된 `MessageBag` 인스턴스에 접근할 수 있습니다.

```
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
<!-- ### Customizing The Error Messages -->
### Customizing The Error Messages

<!-- If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method: -->
필요하다면, 검증기 인스턴스가 Laravel이 제공하는 기본 에러 메시지 대신 사용할 커스텀 에러 메시지를 지정할 수 있습니다. 커스텀 메시지는 여러 가지 방식으로 지정할 수 있습니다. 첫 번째로, `Validator::make` 메서드의 세 번째 인자로 커스텀 메시지 배열을 전달할 수 있습니다.

```
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

<!-- In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example: -->
이 예시에서 `:attribute` 플레이스홀더는 실제 검증 중인 필드명으로 치환됩니다. 유효성 검증 메시지에서는 다른 플레이스홀더도 사용할 수 있습니다. 예를 들면 다음과 같습니다.

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
특정 속성에만 커스텀 에러 메시지를 지정하고 싶을 때가 있습니다. 이럴 때는 "점(.) 표기법(dot notation)"을 사용합니다. 속성명 다음에 규칙명을 이어서 지정합니다.

```
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
<!-- #### Specifying Custom Attribute Values -->
#### Specifying Custom Attribute Values

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method: -->
Laravel의 기본 에러 메시지 중 다수는 `:attribute` 플레이스홀더를 포함하며, 이는 검증 대상 필드 또는 속성명으로 치환됩니다. 특정 필드에 대해 이 플레이스홀더를 치환할 값을 커스터마이징하고 싶다면, `Validator::make`의 네 번째 인자로 커스텀 속성 배열을 전달하면 됩니다.

```
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="after-validation-hook"></a>
<!-- ### After Validation Hook -->
### After Validation Hook

<!-- You may also attach callbacks to be run after validation is completed. This allows you to easily perform further validation and even add more error messages to the message collection. To get started, call the `after` method on a validator instance: -->
유효성 검증이 끝난 후 실행할 콜백을 추가할 수도 있습니다. 이를 통해 추가적인 검증이나 에러 메시지 추가 등 후처리를 쉽게 수행할 수 있습니다. 먼저, 검증기 인스턴스에서 `after` 메서드를 호출하세요.

```
$validator = Validator::make(...);

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
폼 요청을 사용하거나 직접 검증기 인스턴스를 생성해 유효성 검증을 거친 후, 실제로 검증된 요청 데이터만 가져오고 싶을 수 있습니다. 이는 여러 가지 방법으로 할 수 있습니다. 가장 먼저, 폼 요청 혹은 검증기 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 검증을 통과한 데이터만 담긴 배열을 반환합니다.

```
$validated = $request->validated();

$validated = $validator->validated();
```

<!-- Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data: -->
또는, 폼 요청이나 검증기 인스턴스에서 `safe` 메서드를 호출할 수도 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체에서는 `only`, `except`, `all` 메서드를 통해 검증된 데이터 중 원하는 부분만, 또는 전체를 쉽게 가져올 수 있습니다.

```
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

<!-- In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array: -->
그 외에도, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 순회하거나 접근할 수 있습니다.

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
검증된 데이터에 추가 필드를 더하고 싶다면 `merge` 메서드를 사용할 수 있습니다.

```
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

<!-- If you would like to retrieve the validated data as a [collection](/docs/8.x/collections) instance, you may call the `collect` method: -->
검증된 데이터를 [collection](/docs/8.x/collections) 인스턴스로 받고 싶다면 `collect` 메서드를 호출하세요.

```
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
<!-- ## Working With Error Messages -->
## Working With Error Messages

<!-- After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class. -->
`Validator` 인스턴스에서 `errors` 메서드를 호출하면, 다양한 편리한 메서드로 에러 메시지를 다룰 수 있는 `Illuminate\Support\MessageBag` 인스턴스를 얻게 됩니다. 모든 뷰에서 자동으로 사용할 수 있는 `$errors` 변수 역시 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
<!-- #### Retrieving The First Error Message For A Field -->
#### Retrieving The First Error Message For A Field

<!-- To retrieve the first error message for a given field, use the `first` method: -->
특정 필드에 대해 첫 번째 에러 메시지만 가져오려면 `first` 메서드를 사용하세요.

```
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
<!-- #### Retrieving All Error Messages For A Field -->
#### Retrieving All Error Messages For A Field

<!-- If you need to retrieve an array of all the messages for a given field, use the `get` method: -->
특정 필드에 대한 모든 에러 메시지 배열을 가져오려면 `get` 메서드를 사용하세요.

```
foreach ($errors->get('email') as $message) {
    //
}
```

<!-- If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character: -->
배열 형태의 폼 필드를 검증하였다면, `*` 문자를 사용해 각 배열 요소의 모든 메시지를 한 번에 가져올 수 있습니다.

```
foreach ($errors->get('attachments.*') as $message) {
    //
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
<!-- #### Retrieving All Error Messages For All Fields -->
#### Retrieving All Error Messages For All Fields

<!-- To retrieve an array of all messages for all fields, use the `all` method: -->
모든 필드에 대한 모든 메시지 배열을 가져오려면 `all` 메서드를 사용하세요.

```
foreach ($errors->all() as $message) {
    //
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
<!-- #### Determining If Messages Exist For A Field -->
#### Determining If Messages Exist For A Field

<!-- The `has` method may be used to determine if any error messages exist for a given field: -->
특정 필드에 아무 에러 메시지가 존재하는지 확인하려면 `has` 메서드를 사용합니다.

```
if ($errors->has('email')) {
    //
}
```

<a name="specifying-custom-messages-in-language-files"></a>
<!-- ### Specifying Custom Messages In Language Files -->
### Specifying Custom Messages In Language Files

<!-- Laravel's built-in validation rules each has an error message that is located in your application's `resources/lang/en/validation.php` file. Within this file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
Laravel의 기본 내장 유효성 검증 규칙 각각은 애플리케이션의 `resources/lang/en/validation.php` 파일에 에러 메시지가 정의되어 있습니다. 이 파일 안에는 각 유효성 검증 규칙에 대한 번역 항목이 있습니다. 필요에 따라 이 메시지들을 자유롭게 변경하거나 수정할 수 있습니다.

<!-- In addition, you may copy this file to another translation language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/8.x/localization). -->
또한, 이 파일을 다른 언어 디렉터리로 복사해 애플리케이션 언어에 맞게 메세지를 번역할 수도 있습니다. Laravel의 지역화(Localization)에 대해 더 자세히 알아보고 싶다면 [localization documentation](/docs/8.x/localization)를 참고하세요.

<a name="custom-messages-for-specific-attributes"></a>
<!-- #### Custom Messages For Specific Attributes -->
#### Custom Messages For Specific Attributes

<!-- You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `resources/lang/xx/validation.php` language file: -->
애플리케이션의 유효성 검증 언어 파일에서, 특정 속성과 규칙의 조합에 대해 사용하는 에러 메시지를 커스터마이즈할 수 있습니다. 이를 위해 `resources/lang/xx/validation.php` 언어 파일의 `custom` 배열에 메시지를 추가합니다.

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

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. If you would like the `:attribute` portion of your validation message to be replaced with a custom value, you may specify the custom attribute name in the `attributes` array of your `resources/lang/xx/validation.php` language file: -->
Laravel의 기본 에러 메시지 중 다수는 `:attribute` 플레이스홀더를 포함하며, 검증 중인 필드나 속성명으로 치환됩니다. 유효성 검증 메시지의 `:attribute` 부분을 커스텀 값으로 바꾸고 싶으면, `resources/lang/xx/validation.php` 언어 파일의 `attributes` 배열에 커스텀 속성명을 지정하세요.

```
'attributes' => [
    'email' => 'email address',
],
```

<a name="specifying-values-in-language-files"></a>
<!-- ### Specifying Values In Language Files -->
### Specifying Values In Language Files

<!-- Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`: -->
Laravel의 내장 유효성 검증 규칙에 대한 에러 메시지 중 일부는 `:value` 플레이스홀더를 포함하는데, 이는 현재 요청 속성의 실제 값으로 치환됩니다. 하지만, 가끔씩 유효성 메시지에서 이 `:value` 값 대신 더 사용자 친화적인 표현으로 바꾸고 싶을 때가 있습니다. 예를 들어, 아래와 같이 `payment_type` 값이 `cc`인 경우에 신용카드 번호가 필수임을 나타내는 규칙이 있다고 해봅시다.

```
Validator::make($request->all(), [
    'credit_card_number' => 'required_if:payment_type,cc'
]);
```

<!-- If this validation rule fails, it will produce the following error message: -->
이 규칙에 실패하면 다음과 같은 에러 메시지가 출력됩니다.

<!--     The credit card number field is required when payment type is cc. -->
    The credit card number field is required when payment type is cc.

<!-- Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `resources/lang/xx/validation.php` language file by defining a `values` array: -->
`cc` 대신 사용자에게 더 친근한 값을 보여주고 싶다면, `resources/lang/xx/validation.php` 언어 파일의 `values` 배열에 다음과 같이 정의할 수 있습니다.

```
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

<!-- After defining this value, the validation rule will produce the following error message: -->
이렇게 하면, 유효성 검증 규칙이 다음과 같은 에러 메시지를 출력하게 됩니다.

<!--     The credit card number field is required when payment type is credit card. -->
    The credit card number field is required when payment type is credit card.

<a name="available-validation-rules"></a>
<!-- ## Available Validation Rules -->
## Available Validation Rules

<!-- Below is a list of all available validation rules and their function: -->
아래는 모든 사용 가능한 유효성 검증 규칙과 그 기능에 대한 목록입니다.



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
[Declined](#rule-declined)
[Declined If](#rule-declined-if)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Dimensions (Image Files)](#rule-dimensions)
[Distinct](#rule-distinct)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
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
[MAC Address](#rule-mac)
[JSON](#rule-json)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Min](#rule-min)
[Multiple Of](#multiple-of)
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
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#validating-when-present)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[Unique (Database)](#rule-unique)
[URL](#rule-url)
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
[Declined](#rule-declined)
[Declined If](#rule-declined-if)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Dimensions (Image Files)](#rule-dimensions)
[Distinct](#rule-distinct)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
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
[MAC Address](#rule-mac)
[JSON](#rule-json)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Min](#rule-min)
[Multiple Of](#multiple-of)
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
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#validating-when-present)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[Unique (Database)](#rule-unique)
[URL](#rule-url)
[UUID](#rule-uuid)

<!-- </div> -->
</div>

<a name="rule-accepted"></a>
<!-- #### accepted -->
#### accepted

<!-- The field under validation must be `"yes"`, `"on"`, `1`, or `true`. This is useful for validating "Terms of Service" acceptance or similar fields. -->
검증 중인 필드의 값이 반드시 `"yes"`, `"on"`, `1`, 또는 `true`여야 합니다. "서비스 약관 동의"와 같은 필드를 검증할 때 유용합니다.

<a name="rule-accepted-if"></a>
<!-- #### accepted_if:anotherfield,value,... -->
#### accepted_if:anotherfield,value,...

<!-- The field under validation must be `"yes"`, `"on"`, `1`, or `true` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields. -->
검증 중인 필드의 값이, 대상이 되는 다른 필드의 값이 지정한 값과 같을 때만 `"yes"`, `"on"`, `1`, 또는 `true`여야 합니다. "서비스 약관 동의"와 유사한 필드 검증에 활용할 수 있습니다.

<a name="rule-active-url"></a>
<!-- #### active_url -->
#### active_url

<!-- The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`. -->
검증 중인 필드는 PHP의 `dns_get_record` 함수에 따라 유효한 A 레코드 또는 AAAA 레코드를 반드시 가지고 있어야 합니다. 입력 값에서 URL의 호스트명은 PHP의 `parse_url` 함수를 사용해 추출된 뒤 `dns_get_record`로 전달됩니다.

<a name="rule-after"></a>
<!-- #### after:_date_ -->
#### after:_date_

<!-- The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance: -->
검증 중인 필드는, 주어진 날짜 이후의 값이어야 합니다. 주어진 날짜는 내부적으로 PHP의 `strtotime` 함수로 `DateTime` 인스턴스에 변환됩니다.

```
'start_date' => 'required|date|after:tomorrow'
```

<!-- Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date: -->
`strtotime`으로 평가할 날짜 문자열 대신, 비교할 기준으로 다른 필드명을 지정할 수도 있습니다.

```
'finish_date' => 'required|date|after:start_date'
```

<a name="rule-after-or-equal"></a>
<!-- #### after\_or\_equal:_date_ -->
#### after\_or\_equal:_date_

<!-- The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule. -->
검증 중인 필드는 주어진 날짜 이후 또는 그 날짜와 같아야 합니다. 더 자세한 사항은 [after](#rule-after) 규칙을 참고하세요.

<a name="rule-alpha"></a>
<!-- #### alpha -->
#### alpha

<!-- The field under validation must be entirely alphabetic characters. -->
검증 중인 필드는 영문 알파벳 문자만을 포함해야 합니다.

<a name="rule-alpha-dash"></a>
<!-- #### alpha_dash -->
#### alpha_dash

<!-- The field under validation may have alpha-numeric characters, as well as dashes and underscores. -->
검증 중인 필드는 영문자, 숫자, 대시(-), 언더스코어(_)만 포함할 수 있습니다.

<a name="rule-alpha-num"></a>
<!-- #### alpha_num -->
#### alpha_num

<!-- The field under validation must be entirely alpha-numeric characters. -->
검증 중인 필드는 영문자와 숫자만 포함해야 합니다.

<a name="rule-array"></a>
<!-- #### array -->
#### array

<!-- The field under validation must be a PHP `array`. -->
검증 중인 필드는 PHP의 `array` 타입이어야 합니다.

<!-- When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule: -->
`array` 규칙에 추가 값이 전달되면, 입력 배열에서 각 키가 반드시 이 `array` 규칙에 정의한 값의 목록 안에 있어야만 합니다. 아래 예시에서 입력 배열의 `admin` 키는, 규칙에서 지정한 값 목록에 없으므로 유효하지 않습니다.

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
일반적으로 배열의 허용 키 목록을 명시적으로 지정하는 것이 좋습니다. 지정하지 않으면, 검증기의 `validate` 및 `validated` 메서드는 배열과 모든 키를 포함한 검증 데이터를 반환하며, 별도의 중첩 배열 검증 규칙이 없다면 허용되지 않은 키도 함께 반환될 수 있습니다.

<!-- If you would like, you may instruct Laravel's validator to never include unvalidated array keys in the "validated" data it returns, even if you use the `array` rule without specifying a list of allowed keys. To accomplish this, you may call the validator's `excludeUnvalidatedArrayKeys` method in the `boot` method of your application's `AppServiceProvider`. After doing so, the validator will include array keys in the "validated" data it returns only when those keys were specifically validated by [nested array rules](#validating-arrays): -->
만약 `array` 규칙에서 별도의 허용 키 목록을 지정하지 않았을 때도, 검증 데이터에 유효하지 않은 배열 키를 포함하고 싶지 않다면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 검증기의 `excludeUnvalidatedArrayKeys` 메서드를 호출하여 언제나 유효성 검증되지 않은 배열 키를 반환 데이터에서 제외하도록 할 수 있습니다. 이렇게 하면, 검증 결과 데이터에는 반드시 [nested array rules](#validating-arrays)으로 검증한 키만 포함됩니다.

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::excludeUnvalidatedArrayKeys();
}
```

<a name="rule-bail"></a>
<!-- #### bail -->
#### bail

<!-- Stop running validation rules for the field after the first validation failure. -->
유효성 검증 도중, 해당 필드에서 가장 첫 번째 실패가 발생하면 그 뒤의 규칙은 검증하지 않습니다.

<!-- While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`bail` 규칙은 특정 필드에서만 유효성 검증 실패 시 검증을 중단하지만, `stopOnFirstFailure` 메서드는 하나의 검증 실패가 발생한 즉시 모든 속성의 추가 유효성 검증을 중단합니다.

```
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
<!-- #### before:_date_ -->
#### before:_date_

<!-- The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
검증 중인 필드는, 주어진 날짜 이전의 값이어야 합니다. 주어진 날짜는 내부적으로 PHP의 `strtotime` 함수로 `DateTime` 인스턴스에 변환됩니다. 또한 [`after`](#rule-after) 규칙과 마찬가지로, `date` 값으로 다른 필드명을 사용할 수도 있습니다.

<a name="rule-before-or-equal"></a>
<!-- #### before\_or\_equal:_date_ -->
#### before\_or\_equal:_date_

<!-- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [`after`](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
검증 중인 필드는 주어진 날짜 이전이거나 동일한 값이어야 합니다. 사용 방법과 동작은 [`after`](#rule-after) 규칙과 동일하며, 내부적으로 PHP `strtotime`으로 날짜를 유효한 `DateTime` 인스턴스로 평가합니다. `date` 값으로 다른 필드명을 사용할 수도 있습니다.

<a name="rule-between"></a>
<!-- #### between:_min_,_max_ -->
#### between:_min_,_max_

<!-- The field under validation must have a size between the given _min_ and _max_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
검증 중인 필드는 지정한 _min_과 _max_ 사이의 크기여야 합니다. 문자열, 숫자, 배열, 파일 등은 [`size`](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-boolean"></a>
<!-- #### boolean -->
#### boolean

<!-- The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`. -->
검증 중인 필드는 boolean 타입으로 변환될 수 있어야 합니다. 허용되는 값은 `true`, `false`, `1`, `0`, `"1"`, `"0"` 입니다.

<a name="rule-confirmed"></a>
<!-- #### confirmed -->
#### confirmed

<!-- The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input. -->
검증 중인 필드는 `{field}_confirmation`으로 끝나는 동일한 이름의 필드를 입력 값에서 반드시 가져야 하며, 두 필드의 값이 일치해야 합니다. 예를 들어, `password` 필드를 검증할 때 `password_confirmation` 필드도 함께 받아야 합니다.

<a name="rule-current-password"></a>
<!-- #### current_password -->
#### current_password

<!-- The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/8.x/authentication) using the rule's first parameter: -->
검증 중인 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 이 규칙의 첫 번째 파라미터로 [authentication guard](/docs/8.x/authentication)를 지정할 수도 있습니다.

```
'password' => 'current_password:api'
```

<a name="rule-date"></a>
<!-- #### date -->
#### date

<!-- The field under validation must be a valid, non-relative date according to the `strtotime` PHP function. -->
검증 중인 필드는 PHP `strtotime` 함수로 유효(존재하는 날짜, 상대적이지 않은 날짜)한 날짜 형식이어야 합니다.

<a name="rule-date-equals"></a>
<!-- #### date_equals:_date_ -->
#### date_equals:_date_

<!-- The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. -->
검증 중인 필드는 주어진 날짜와 정확히 같은 값이어야 합니다. 주어진 날짜는 PHP의 `strtotime` 함수로 변환해 `DateTime` 인스턴스로 체크됩니다.

<a name="rule-date-format"></a>
<!-- #### date_format:_format_ -->
#### date_format:_format_

<!-- The field under validation must match the given _format_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class. -->
검증 중인 필드는 지정한 _format_과 일치해야 합니다. 한 필드에 `date`와 `date_format` 규칙을 함께 사용하면 안 됩니다. 이 검증 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 형식을 지원합니다.

<a name="rule-declined"></a>
<!-- #### declined -->
#### declined

<!-- The field under validation must be `"no"`, `"off"`, `0`, or `false`. -->
검증 중인 필드는 반드시 `"no"`, `"off"`, `0`, 또는 `false` 값이어야 합니다.

<a name="rule-declined-if"></a>
<!-- #### declined_if:anotherfield,value,... -->
#### declined_if:anotherfield,value,...

<!-- The field under validation must be `"no"`, `"off"`, `0`, or `false` if another field under validation is equal to a specified value. -->
다른 필드의 값이 특정 값과 같을 때, 검증 중인 필드는 반드시 `"no"`, `"off"`, `0`, 또는 `false`여야 합니다.

<a name="rule-different"></a>
<!-- #### different:_field_ -->
#### different:_field_

<!-- The field under validation must have a different value than _field_. -->
검증 중인 필드는 지정한 _field_와 값이 달라야 합니다.

<a name="rule-digits"></a>
<!-- #### digits:_value_ -->
#### digits:_value_

<!-- The field under validation must be _numeric_ and must have an exact length of _value_. -->
검증 중인 필드는 _numeric_이어야 하며, 자리수가 정확히 _value_여야 합니다.

<a name="rule-digits-between"></a>
<!-- #### digits_between:_min_,_max_ -->
#### digits_between:_min_,_max_

<!-- The field under validation must be _numeric_ and must have a length between the given _min_ and _max_. -->
검증 중인 필드는 _numeric_이어야 하며, 자리수가 _min_과 _max_ 사이여야 합니다.

<a name="rule-dimensions"></a>
<!-- #### dimensions -->
#### dimensions

<!-- The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters: -->
검증 중인 파일은 다음과 같이 지정한 파라미터 제약조건을 만족하는 이미지여야 합니다.

```
'avatar' => 'dimensions:min_width=100,min_height=200'
```

<!-- Available constraints are: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_. -->
사용 가능한 제약조건: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_.

<!-- A _ratio_ constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`: -->
_비율(ratio)_ 제약조건은 가로를 세로로 나눈 값으로 표시합니다. 분수(`3/2`) 또는 실수(`1.5`) 형태로 지정할 수 있습니다.

```
'avatar' => 'dimensions:ratio=3/2'
```

<!-- Since this rule requires several arguments, you may use the `Rule::dimensions` method to fluently construct the rule: -->
이 규칙은 여러 인자를 필요로 하므로, `Rule::dimensions` 메서드를 사용해 더 유연하게 규칙을 구성할 수 있습니다.

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
distinct 규칙은 기본적으로 느슨한(비엄격한) 변수 비교를 사용합니다. 엄격한 비교를 사용하려면 `strict` 매개변수를 규칙 정의에 추가하면 됩니다.

```
'foo.*.id' => 'distinct:strict'
```

<!-- You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences: -->
대소문자 구분 없이 중복 여부를 검사하고 싶다면 `ignore_case`를 규칙에 추가하세요.

```
'foo.*.id' => 'distinct:ignore_case'
```

<a name="rule-email"></a>
<!-- #### email -->
#### email

<!-- The field under validation must be formatted as an email address. This validation rule utilizes the [`egulias/email-validator`](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well: -->
해당 필드는 이메일 주소 형식이어야 합니다. 이 유효성 검증 규칙은 이메일 주소를 검증하기 위해 [`egulias/email-validator`](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 검증기가 적용되지만, 다른 검증 스타일도 사용할 수 있습니다.

```
'email' => 'email:rfc,dns'
```

<!-- The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply: -->
위 예시에서는 `RFCValidation`과 `DNSCheckValidation` 두 가지 검증이 동시에 적용됩니다. 적용 가능한 검증 스타일 전체 목록은 아래와 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`
-->
- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`

<!-- </div> -->
</div>

<!-- The `filter` validator, which uses PHP's `filter_var` function, ships with Laravel and was Laravel's default email validation behavior prior to Laravel version 5.8. -->
PHP의 `filter_var` 함수를 사용하는 `filter` 검증기는 Laravel에 기본 탑재되어 있으며, Laravel 버전 5.8 이전의 기본 이메일 검증 방식이기도 했습니다.

> [!NOTE]
> `dns` 및 `spoof` 검증기는 PHP `intl` 확장 모듈이 필요합니다.

<a name="rule-ends-with"></a>
<!-- #### ends_with:_foo_,_bar_,... -->
#### ends_with:_foo_,_bar_,...

<!-- The field under validation must end with one of the given values. -->
해당 필드는 주어진 값들 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
<!-- #### enum -->
#### enum

<!-- The `Enum` rule is a class based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument: -->
`Enum` 규칙은 필드 값이 유효한 열거형(enum) 값인지 클래스 기반으로 검증합니다. `Enum` 규칙은 생성자 인수로 열거형 클래스명을 받습니다.

```
use App\Enums\ServerStatus;
use Illuminate\Validation\Rules\Enum;

$request->validate([
    'status' => [new Enum(ServerStatus::class)],
]);
```

> [!NOTE]
> 열거형(enum)은 PHP 8.1 이상에서만 사용할 수 있습니다.

<a name="rule-exclude"></a>
<!-- #### exclude -->
#### exclude

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods. -->
해당 필드는 `validate`, `validated` 메서드로 반환되는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
<!-- #### exclude_if:_anotherfield_,_value_ -->
#### exclude_if:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_. -->
_anotherfield_에 해당하는 필드가 _value_와 같으면, 해당 필드는 `validate`, `validated` 메서드로 반환되는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-unless"></a>
<!-- #### exclude_unless:_anotherfield_,_value_ -->
#### exclude_unless:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless _anotherfield_'s field is equal to _value_. If _value_ is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data. -->
_anotherfield_ 필드가 _value_와 같지 않다면, 해당 필드는 `validate`, `validated` 메서드로 반환되는 데이터에서 제외됩니다. _value_가 `null`(`exclude_unless:name,null`)이면, 비교 대상 필드가 `null`이거나 요청 데이터에 없을 때 해당 필드는 제외됩니다.

<a name="rule-exclude-without"></a>
<!-- #### exclude_without:_anotherfield_ -->
#### exclude_without:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present. -->
_anotherfield_ 필드가 존재하지 않을 경우, 해당 필드는 `validate`, `validated` 결과에서 제외됩니다.

<a name="rule-exists"></a>
<!-- #### exists:_table_,_column_ -->
#### exists:_table_,_column_

<!-- The field under validation must exist in a given database table. -->
해당 필드의 값은 지정된 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
<!-- #### Basic Usage Of Exists Rule -->
#### Basic Usage Of Exists Rule

```
'state' => 'exists:states'
```

<!-- If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value. -->
`column` 옵션을 지정하지 않으면, 필드명이 그대로 사용됩니다. 즉, 위 규칙은 요청의 `state` 값이 `states` 테이블의 `state` 컬럼에 존재하는지 검사합니다.

<a name="specifying-a-custom-column-name"></a>
<!-- #### Specifying A Custom Column Name -->
#### Specifying A Custom Column Name

<!-- You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name: -->
유효성 규칙에서 사용할 데이터베이스 컬럼명을 테이블명 뒤에 명시적으로 지정할 수 있습니다.

```
'state' => 'exists:states,abbreviation'
```

<!-- Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name: -->
경우에 따라 `exists` 쿼리를 수행할 때 특정 데이터베이스 커넥션을 지정해야 할 수도 있습니다. 이때는 테이블 이름 앞에 커넥션명을 추가하면 됩니다.

```
'email' => 'exists:connection.staff,email'
```

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블명을 직접 지정하는 대신, 사용할 Eloquent 모델을 지정하여 테이블명을 자동으로 결정하게 할 수도 있습니다.

```
'user_id' => 'exists:App\Models\User,id'
```

<!-- If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit them: -->
유효성 검증 규칙이 실행하는 쿼리를 커스터마이징하고 싶다면, `Rule` 클래스를 이용해 규칙을 체이닝 방식으로 정의할 수 있습니다. 아래 예시에서는 구분자로 `|` 대신 배열로 규칙을 명시하고 있습니다.

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

<a name="rule-file"></a>
<!-- #### file -->
#### file

<!-- The field under validation must be a successfully uploaded file. -->
해당 필드는 성공적으로 업로드된 파일이어야 합니다.

<a name="rule-filled"></a>
<!-- #### filled -->
#### filled

<!-- The field under validation must not be empty when it is present. -->
해당 필드가 존재할 경우, 빈 값이 아니어야 합니다.

<a name="rule-gt"></a>
<!-- #### gt:_field_ -->
#### gt:_field_

<!-- The field under validation must be greater than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
해당 필드는 지정한 _field_보다 커야 합니다. 두 필드의 데이터 타입이 동일해야 합니다. 문자열, 숫자, 배열, 파일의 경우 [`size`](#rule-size) 규칙과 동일한 기준으로 비교합니다.

<a name="rule-gte"></a>
<!-- #### gte:_field_ -->
#### gte:_field_

<!-- The field under validation must be greater than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
해당 필드는 지정한 _field_보다 크거나 같아야 합니다. 두 값의 데이터 타입이 동일해야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일하게 평가합니다.

<a name="rule-image"></a>
<!-- #### image -->
#### image

<!-- The file under validation must be an image (jpg, jpeg, png, bmp, gif, svg, or webp). -->
검증 대상 파일은 이미지(jpg, jpeg, png, bmp, gif, svg, webp)여야 합니다.

<a name="rule-in"></a>
<!-- #### in:_foo_,_bar_,... -->
#### in:_foo_,_bar_,...

<!-- The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule: -->
해당 필드는 주어진 값들의 목록에 포함되어야 합니다. 이 규칙은 배열을 `implode`로 연결할 필요가 많은데, `Rule::in` 메서드를 사용하면 규칙을 더 간결하게 작성할 수 있습니다.

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
`in` 규칙을 `array` 규칙과 함께 사용하면, 입력 배열의 각 값이 `in` 규칙의 값 목록에 모두 존재해야 합니다. 다음 예시에서 입력 배열의 `LAS` 코드 값은 `in` 목록에 포함돼 있지 않으므로 유효하지 않습니다.

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
        Rule::in(['NYC', 'LIT']),
    ],
]);
```

<a name="rule-in-array"></a>
<!-- #### in_array:_anotherfield_.* -->
#### in_array:_anotherfield_.*

<!-- The field under validation must exist in _anotherfield_'s values. -->
해당 필드는 _anotherfield_에 포함된 값들 중 하나여야 합니다.

<a name="rule-integer"></a>
<!-- #### integer -->
#### integer

<!-- The field under validation must be an integer. -->
해당 필드는 정수 값이어야 합니다.

> [!NOTE]
> 이 유효성 규칙은 입력값이 "integer" 자료형인지까지는 검사하지 않고, PHP의 `FILTER_VALIDATE_INT`로 허용되는 값인지 확인합니다. 입력값을 명확하게 숫자로 검증하고 싶다면 [the `numeric` validation rule](#rule-numeric)과 같이 사용하세요.

<a name="rule-ip"></a>
<!-- #### ip -->
#### ip

<!-- The field under validation must be an IP address. -->
해당 필드는 IP 주소 형식이어야 합니다.

<a name="ipv4"></a>
<!-- #### ipv4 -->
#### ipv4

<!-- The field under validation must be an IPv4 address. -->
해당 필드는 IPv4 주소여야 합니다.

<a name="ipv6"></a>
<!-- #### ipv6 -->
#### ipv6

<!-- The field under validation must be an IPv6 address. -->
해당 필드는 IPv6 주소여야 합니다.

<a name="rule-mac"></a>
<!-- #### mac_address -->
#### mac_address

<!-- The field under validation must be a MAC address. -->
해당 필드는 MAC 주소 형식이어야 합니다.

<a name="rule-json"></a>
<!-- #### json -->
#### json

<!-- The field under validation must be a valid JSON string. -->
해당 필드는 유효한 JSON 문자열이어야 합니다.

<a name="rule-lt"></a>
<!-- #### lt:_field_ -->
#### lt:_field_

<!-- The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
해당 필드는 지정한 _field_보다 작아야 합니다. 두 값의 타입이 동일해야 하며, 문자열, 숫자, 배열, 파일은 [`size`](#rule-size) 규칙과 동일한 기준으로 비교합니다.

<a name="rule-lte"></a>
<!-- #### lte:_field_ -->
#### lte:_field_

<!-- The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [`size`](#rule-size) rule. -->
해당 필드는 지정한 _field_보다 작거나 같아야 합니다. 두 값은 동일한 타입이어야 하며, 문자열, 숫자, 배열, 파일의 경우 [`size`](#rule-size) 규칙과 동일하게 평가합니다.

<a name="rule-max"></a>
<!-- #### max:_value_ -->
#### max:_value_

<!-- The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
해당 필드는 _value_보다 작거나 같은 값이어야 합니다. 문자열, 숫자, 배열, 파일은 [`size`](#rule-size) 규칙과 동일하게 평가합니다.

<a name="rule-mimetypes"></a>
<!-- #### mimetypes:_text/plain_,... -->
#### mimetypes:_text/plain_,...

<!-- The file under validation must match one of the given MIME types: -->
해당 파일의 MIME 타입이 주어진 타입 중 하나와 일치해야 합니다.

```
'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'
```

<!-- To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type. -->
업로드된 파일의 MIME 타입을 확인하기 위해, 프레임워크는 파일의 내용을 읽어 MIME 타입을 추론합니다(이 과정에서 클라이언트가 제공한 값과 다를 수 있습니다).

<a name="rule-mimes"></a>
<!-- #### mimes:_foo_,_bar_,... -->
#### mimes:_foo_,_bar_,...

<!-- The file under validation must have a MIME type corresponding to one of the listed extensions. -->
해당 파일의 확장자가 나열된 목록과 대응하는 MIME 타입이어야 합니다.

<a name="basic-usage-of-mime-rule"></a>
<!-- #### Basic Usage Of MIME Rule -->
#### Basic Usage Of MIME Rule

```
'photo' => 'mimes:jpg,bmp,png'
```

<!-- Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
확장자만 지정하면 되지만, 실제로는 파일의 내용이 읽혀서 MIME 타입을 판별합니다. 전체 MIME 타입과 확장자 목록은 아래에서 확인할 수 있습니다.

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
<!-- #### min:_value_ -->
#### min:_value_

<!-- The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [`size`](#rule-size) rule. -->
해당 필드는 최소 _value_ 값 이상이어야 합니다. 문자열, 숫자, 배열, 파일 모두 [`size`](#rule-size) 규칙과 동일하게 평가됩니다.

<a name="multiple-of"></a>
<!-- #### multiple_of:_value_ -->
#### multiple_of:_value_

<!-- The field under validation must be a multiple of _value_. -->
해당 필드는 _value_의 배수여야 합니다.

> [!NOTE]
> `multiple_of` 규칙을 사용하려면 [`bcmath` PHP extension](https://www.php.net/manual/en/book.bc.php)이 필요합니다.

<a name="rule-not-in"></a>
<!-- #### not_in:_foo_,_bar_,... -->
#### not_in:_foo_,_bar_,...

<!-- The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule: -->
해당 필드는 주어진 값 목록에 포함되지 않아야 합니다. `Rule::notIn` 메서드를 쓰면 규칙을 더 깔끔하게 선언할 수 있습니다.

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
해당 필드는 주어진 정규 표현식과 일치하지 않아야 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'not_regex:/^.+$/i'`. -->
이 규칙은 내부적으로 PHP의 `preg_match` 함수로 동작합니다. 지정한 패턴은 `preg_match`의 형식(구분자 포함)을 따라야 합니다. 예시: `'email' => 'not_regex:/^.+$/i'`

> [!NOTE]
> `regex` 또는 `not_regex` 규칙에 `|` 문자가 포함되어 있을 땐, `|` 구분자 대신 규칙을 배열로 입력하는 것이 필요할 수 있습니다.

<a name="rule-nullable"></a>
<!-- #### nullable -->
#### nullable

<!-- The field under validation may be `null`. -->
해당 필드는 `null` 값을 허용합니다.

<a name="rule-numeric"></a>
<!-- #### numeric -->
#### numeric

<!-- The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php). -->
해당 필드는 [numeric](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

<a name="rule-password"></a>
<!-- #### password -->
#### password

<!-- The field under validation must match the authenticated user's password. -->
해당 필드는 인증된 사용자의 비밀번호와 일치해야 합니다.

> [!NOTE]
> 이 규칙은 Laravel 9에서 삭제 예정이며, 이름이 `current_password`로 변경되었습니다. 반드시 [Current Password](#rule-current-password) 규칙을 사용하시기 바랍니다.

<a name="rule-present"></a>
<!-- #### present -->
#### present

<!-- The field under validation must be present in the input data but can be empty. -->
해당 필드는 입력 데이터에 반드시 존재해야 하며, 비어 있어도 상관없습니다.

<a name="rule-prohibited"></a>
<!-- #### prohibited -->
#### prohibited

<!-- The field under validation must be empty or not present. -->
해당 필드는 비어 있거나 요청 데이터에 존재하지 않아야 합니다.

<a name="rule-prohibited-if"></a>
<!-- #### prohibited_if:_anotherfield_,_value_,... -->
#### prohibited_if:_anotherfield_,_value_,...

<!-- The field under validation must be empty or not present if the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ 필드가 _value_와 같을 경우, 이 필드는 비어 있거나 존재하지 않아야 합니다.

<a name="rule-prohibited-unless"></a>
<!-- #### prohibited_unless:_anotherfield_,_value_,... -->
#### prohibited_unless:_anotherfield_,_value_,...

<!-- The field under validation must be empty or not present unless the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ 필드가 _value_와 같지 않을 경우, 이 필드는 비어 있거나 존재하지 않아야 합니다.

<a name="rule-prohibits"></a>
<!-- #### prohibits:_anotherfield_,... -->
#### prohibits:_anotherfield_,...

<!-- If the field under validation is present, no fields in _anotherfield_ can be present, even if empty. -->
해당 필드가 존재하는 경우, _anotherfield_ 목록에 있는 어느 필드도(비어 있더라도) 존재해서는 안 됩니다.

<a name="rule-regex"></a>
<!-- #### regex:_pattern_ -->
#### regex:_pattern_

<!-- The field under validation must match the given regular expression. -->
해당 필드는 주어진 정규 표현식과 일치해야 합니다.

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => 'regex:/^.+@.+$/i'`. -->
이 규칙은 내부적으로 PHP의 `preg_match`를 사용합니다. 지정한 패턴은 구분자를 포함해 `preg_match` 규칙 형식을 따라야 합니다. 예: `'email' => 'regex:/^.+@.+$/i'`

> [!NOTE]
> `regex` 또는 `not_regex` 규칙을 쓸 때 정규표현식에 `|` 문자가 포함되어 있으면, `|` 구분자 대신 규칙을 배열 형태로 선언하는 것이 필요할 수 있습니다.

<a name="rule-required"></a>
<!-- #### required -->
#### required

<!-- The field under validation must be present in the input data and not empty. A field is considered "empty" if one of the following conditions are true: -->
해당 필드는 입력 데이터에 반드시 존재해야 하며, 비어 있으면 안 됩니다. 필드가 "비어 있음"으로 간주되는 조건은 다음과 같습니다.

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
- 값이 빈 배열이거나, 비어 있는 `Countable` 객체인 경우
- 업로드된 파일이 경로를 갖고 있지 않은 경우

<!-- </div> -->
</div>

<a name="rule-required-if"></a>
<!-- #### required_if:_anotherfield_,_value_,... -->
#### required_if:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ 필드가 _value_ 값일 때, 해당 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<!-- If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required: -->
`required_if` 규칙에 더 복잡한 조건을 사용하고 싶을 땐 `Rule::requiredIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 받고, 클로저는 해당 필드가 필수인지 판단해 `true` 또는 `false`를 반환해야 합니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf($request->user()->is_admin),
]);

Validator::make($request->all(), [
    'role_id' => Rule::requiredIf(function () use ($request) {
        return $request->user()->is_admin;
    }),
]);
```

<a name="rule-required-unless"></a>
<!-- #### required_unless:_anotherfield_,_value_,... -->
#### required_unless:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data. -->
_anotherfield_ 필드가 _value_가 아닌 경우에 해당 필드는 반드시 존재하며 비어 있으면 안 됩니다. 즉, _anotherfield_도 _value_가 `null`이 아닌 한 요청 데이터에 반드시 포함되어야 합니다. _value_가 `null`(`required_unless:name,null`)이면, 비교 대상 필드가 `null`이거나 데이터에 없는 경우에만 해당 필드를 요구하지 않습니다.

<a name="rule-required-with"></a>
<!-- #### required_with:_foo_,_bar_,... -->
#### required_with:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty. -->
지정한 다른 필드들 중 어느 하나라도 값이 존재하며 비어 있지 않다면, 해당 필드도 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-with-all"></a>
<!-- #### required_with_all:_foo_,_bar_,... -->
#### required_with_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty. -->
지정한 필드들이 모두 값이 존재하며 비어 있지 않을 때만, 해당 필드도 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-without"></a>
<!-- #### required_without:_foo_,_bar_,... -->
#### required_without:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present. -->
지정한 필드들 중 어느 하나라도 비어 있거나 존재하지 않을 때에만, 해당 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-required-without-all"></a>
<!-- #### required_without_all:_foo_,_bar_,... -->
#### required_without_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present. -->
지정한 필드들이 모두 비어 있거나 존재하지 않을 때에만, 해당 필드는 반드시 존재하며 비어 있으면 안 됩니다.

<a name="rule-same"></a>
<!-- #### same:_field_ -->
#### same:_field_

<!-- The given _field_ must match the field under validation. -->
지정한 _field_의 값과 해당 필드가 일치해야 합니다.

<a name="rule-size"></a>
<!-- #### size:_value_ -->
#### size:_value_

<!-- The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples: -->
해당 필드는 _value_와 정확히 일치하는 크기를 가져야 합니다. 문자열 데이터라면 _value_는 글자 수, 숫자라면 정수값(그리고 반드시 `numeric` 또는 `integer` 규칙이 함께 적용되어야 함), 배열이라면 `count`, 파일이라면 킬로바이트(KB) 단위의 파일 크기에 해당합니다. 예시를 보겠습니다.

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
해당 필드는 주어진 값들 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
<!-- #### string -->
#### string

<!-- The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field. -->
해당 필드는 문자열이어야 합니다. 만약 이 필드에 `null`도 허용하고 싶다면, `nullable` 규칙도 함께 지정해야 합니다.

<a name="rule-timezone"></a>
<!-- #### timezone -->
#### timezone

<!-- The field under validation must be a valid timezone identifier according to the `timezone_identifiers_list` PHP function. -->
해당 필드는 PHP의 `timezone_identifiers_list` 함수에 기반하여 유효한 타임존 식별자여야 합니다.

<a name="rule-unique"></a>
<!-- #### unique:_table_,_column_ -->
#### unique:_table_,_column_

<!-- The field under validation must not exist within the given database table. -->
해당 필드 값이 주어진 데이터베이스 테이블에 기존에 존재하지 않아야 합니다.

<!-- **Specifying A Custom Table / Column Name:** -->
**커스텀 테이블/컬럼명 지정하기**

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
테이블명을 직접 지정하는 대신, 사용할 Eloquent 모델을 지정해 테이블명을 자동으로 사용할 수 있습니다.

```
'email' => 'unique:App\Models\User,email_address'
```

<!-- The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used. -->
`column` 옵션에서 데이터베이스 컬럼명을 지정할 수 있습니다. `column` 옵션을 지정하지 않으면 필드명이 사용됩니다.

```
'email' => 'unique:users,email_address'
```

<!-- **Specifying A Custom Database Connection** -->
**커스텀 데이터베이스 커넥션 지정하기**

<!-- Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name: -->
경우에 따라 유효성 검사 시 사용하는 커넥션을 지정해야 할 수 있습니다. 이때는 테이블명 앞에 커넥션명을 붙여 사용합니다.

```
'email' => 'unique:connection.users,email_address'
```

<!-- **Forcing A Unique Rule To Ignore A Given ID:** -->
**특정 ID를 무시하도록 Unique 규칙에 지정하기**

<!-- Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question. -->
예를 들어 '프로필 수정 화면'에서 사용자의 이름, 이메일, 위치를 검사한다고 할 때, 이메일 주소의 유일성을 검증하길 원할 수 있습니다. 하지만 사용자가 이름만 바꾸고 이메일은 바꾸지 않은 경우, 기존 본인의 이메일이기 때문에 유효성 검증에서 문제없이 통과해야 합니다.

<!-- To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. In this example, we'll also specify the validation rules as an array instead of using the `|` character to delimit the rules: -->
사용자의 ID를 무시하도록 지정하려면 `Rule` 클래스를 이용해 규칙을 체이닝 방식으로 정의해야 합니다. 예시에서는 `|` 문자 구분자 대신 배열로 규칙을 입력하고 있습니다.

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

> [!NOTE]
> `ignore` 메서드에 사용자 입력값을 직접 사용해서는 절대 안 됩니다. 반드시 Eloquent 모델에서 얻거나 시스템이 생성한 고유 키 값(예: 증가하는 ID, UUID)만 사용해야 합니다. 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해질 수 있습니다.

<!-- Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model: -->
모델의 키 값 자체를 전달하지 않고, 모델 인스턴스 전체를 `ignore` 메서드에 넘길 수도 있습니다. 이 경우 Laravel이 자동으로 키 값을 추출합니다.

```
Rule::unique('users')->ignore($user)
```

<!-- If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method: -->
테이블의 기본 키 컬럼명이 `id`가 아니라면, `ignore` 메서드에서 해당 컬럼명을 지정할 수 있습니다.

```
Rule::unique('users')->ignore($user->id, 'user_id')
```

<!-- By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method: -->
기본적으로 `unique` 규칙은 검증 중인 필드명과 동일한 컬럼의 유일성을 검사합니다. 하지만, `unique` 메서드의 두 번째 인수로 다른 컬럼명을 지정할 수도 있습니다.

```
Rule::unique('users', 'email_address')->ignore($user->id),
```

<!-- **Adding Additional Where Clauses:** -->
**추가 Where 조건 지정하기**

<!-- You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`: -->
`where` 메서드를 활용해 쿼리 조건을 더 상세하게 지정할 수 있습니다. 예시에서는 `account_id` 컬럼 값이 `1`인 레코드 안에서만 검색하도록 쿼리를 제한하고 있습니다.

```
'email' => Rule::unique('users')->where(function ($query) {
    return $query->where('account_id', 1);
})
```

<a name="rule-url"></a>
<!-- #### url -->
#### url

<!-- The field under validation must be a valid URL. -->
해당 필드는 유효한 URL이어야 합니다.

<a name="rule-uuid"></a>
<!-- #### uuid -->
#### uuid

<!-- The field under validation must be a valid RFC 4122 (version 1, 3, 4, or 5) universally unique identifier (UUID). -->
해당 필드는 RFC 4122(버전 1, 3, 4, 5) 표준의 UUID(범용 고유 식별자)여야 합니다.

<a name="conditionally-adding-rules"></a>
<!-- ## Conditionally Adding Rules -->
## Conditionally Adding Rules

<a name="skipping-validation-when-fields-have-certain-values"></a>

<!-- #### Skipping Validation When Fields Have Certain Values -->
#### Skipping Validation When Fields Have Certain Values

<!-- You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`: -->
다른 필드가 특정 값을 가질 때, 해당 필드의 유효성 검증을 건너뛰고 싶을 수 있습니다. 이런 경우에는 `exclude_if` 유효성 검증 규칙을 사용할 수 있습니다. 아래 예시에서는 `has_appointment` 필드의 값이 `false`일 경우, `appointment_date`와 `doctor_name` 필드의 유효성 검증이 수행되지 않습니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => 'required|boolean',
    'appointment_date' => 'exclude_if:has_appointment,false|required|date',
    'doctor_name' => 'exclude_if:has_appointment,false|required|string',
]);
```

<!-- Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value: -->
반대로, 특정 필드가 주어진 값이 아닐 때만 검증을 건너뛰고, 특정 값일 때만 검증을 수행하고 싶다면 `exclude_unless` 규칙을 사용할 수 있습니다.

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
특정 필드가 입력 데이터에 포함되어 있을 때만 유효성 검증을 진행하고 싶은 경우가 있습니다. 이런 경우에는 규칙 목록에 `sometimes` 규칙을 추가하면 간단하게 처리할 수 있습니다.

```
$v = Validator::make($data, [
    'email' => 'sometimes|required|email',
]);
```

<!-- In the example above, the `email` field will only be validated if it is present in the `$data` array. -->
위 예시에서, `email` 필드는 `$data` 배열에 존재할 때만 유효성 검증 대상이 됩니다.

> [!TIP]
> 무조건 존재해야 하지만 비어 있을 수 있는 필드를 검증하려면 [this note on optional fields](#a-note-on-optional-fields)을 참고하세요.

<a name="complex-conditional-validation"></a>
<!-- #### Complex Conditional Validation -->
#### Complex Conditional Validation

<!-- Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change: -->
조건이 조금 더 복잡할 때 유효성 규칙을 동적으로 추가하고 싶을 수 있습니다. 예를 들어, 어떤 필드가 100보다 클 경우에만 다른 필드를 필수로 만들거나, 특정 필드의 값이 있을 때만 다른 두 필드가 특정 값을 갖게 하는 등의 요구사항이 있을 수 있습니다. 이런 경우에도 유효성 검증 규칙을 유연하게 추가할 수 있습니다. 우선, _항상 동일하게 적용되는 규칙_ 으로 `Validator` 인스턴스를 생성합니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => 'required|email',
    'games' => 'required|numeric',
]);
```

<!-- Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance. -->
예를 들어, 게임 수집가를 위한 웹 애플리케이션이라고 가정해봅시다. 만약 가입 시 수집한 게임이 100개를 넘는다면, 왜 그렇게 많은 게임을 소유하게 되었는지 설명을 받으려 할 수 있습니다(예: 게임 되팔이점을 운영함, 또는 단순히 수집을 즐김 등). 이런 조건부 요구사항은 `Validator` 인스턴스의 `sometimes` 메서드로 추가할 수 있습니다.

```
$validator->sometimes('reason', 'required|max:500', function ($input) {
    return $input->games >= 100;
});
```

<!-- The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once: -->
`sometimes` 메서드의 첫 번째 인자는 조건부로 검증할 필드명입니다. 두 번째 인자는 추가할 규칙 목록이고, 세 번째 인자로 전달되는 클로저가 `true`를 반환하면 해당 규칙이 추가됩니다. 이 방식으로 복잡한 조건부 유효성 검증도 매우 쉽게 작성할 수 있습니다. 여러 필드에 대해 한 번에 조건부 검증 규칙을 추가하는 것도 가능합니다.

```
$validator->sometimes(['reason', 'cost'], 'required', function ($input) {
    return $input->games >= 100;
});
```

> [!TIP]
> 클로저에 전달되는 `$input` 파라미터는 `Illuminate\Support\Fluent` 인스턴스입니다. 따라서 유효성 검증 중인 입력 값이나 파일에 접근할 수 있습니다.

<a name="complex-conditional-array-validation"></a>
<!-- #### Complex Conditional Array Validation -->
#### Complex Conditional Array Validation

<!-- Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated: -->
중첩 배열 내에서, 정확한 인덱스를 모르는 경우 다른 필드의 값을 조건으로 검증할 때도 있을 수 있습니다. 이럴 때는, 클로저에 두 번째 인자를 받아서, 현재 검증 중인 배열 내 개별 항목 정보를 활용할 수 있습니다.

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
`$input`과 마찬가지로, `$item` 파라미터는 배열 데이터라면 `Illuminate\Support\Fluent` 인스턴스가 되고, 배열이 아니라면 일반 문자열이 됩니다.

<a name="validating-arrays"></a>
<!-- ## Validating Arrays -->
## Validating Arrays

<!-- As discussed in the [`array` validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail: -->
[`array` validation rule documentation](#rule-array)에서 설명한 것처럼, `array` 규칙에는 허용할 배열 키의 목록을 지정할 수 있습니다. 배열에 추가적인 키가 있으면, 유효성 검증은 실패하게 됩니다.

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
일반적으로, 배열 내에 어떤 키가 들어올 수 있는지 명시하는 것이 좋습니다. 그렇지 않으면, validator의 `validate`와 `validated` 메서드는 배열 전체와 모든 키(심지어 중첩 배열 규칙으로 검증되지 않은 키 포함)를 그대로 반환합니다.

<a name="excluding-unvalidated-array-keys"></a>
<!-- ### Excluding Unvalidated Array Keys -->
### Excluding Unvalidated Array Keys

<!-- If you would like, you may instruct Laravel's validator to never include unvalidated array keys in the "validated" data it returns, even if you use the `array` rule without specifying a list of allowed keys. To accomplish this, you may call the validator's `excludeUnvalidatedArrayKeys` method in the `boot` method of your application's `AppServiceProvider`. After doing so, the validator will include array keys in the "validated" data it returns only when those keys were specifically validated by [nested array rules](#validating-arrays): -->
만약 `array` 규칙에서 허용 키 목록을 지정하지 않아도, 검증되지 않은 배열 키를 "검증된 데이터"에 절대 포함시키고 싶지 않다면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 validator의 `excludeUnvalidatedArrayKeys` 메서드를 호출하면 됩니다. 이렇게 하면 [nested array rules](#validating-arrays)으로 구체적으로 검증한 키만 "검증된 데이터"에 포함됩니다.

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::excludeUnvalidatedArrayKeys();
}
```

<a name="validating-nested-array-input"></a>
<!-- ### Validating Nested Array Input -->
### Validating Nested Array Input

<!-- Validating nested array based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so: -->
중첩 배열 형식의 폼 입력 필드도 손쉽게 검증할 수 있습니다. 배열 내 특정 속성을 지정할 때는 "점 표기법(dot notation)"을 사용할 수 있습니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]` 필드가 있다면 다음과 같이 검증할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => 'required|image',
]);
```

<!-- You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following: -->
배열의 각 요소에 대해서도 검증이 가능합니다. 예를 들어, 주어진 배열 입력의 각 이메일이 고유해야 하는 경우 아래와 같이 처리할 수 있습니다.

```
$validator = Validator::make($request->all(), [
    'person.*.email' => 'email|unique:users',
    'person.*.first_name' => 'required_with:person.*.last_name',
]);
```

<!-- Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array based fields: -->
마찬가지로, [custom validation messages in your language files](#custom-messages-for-specific-attributes)를 지정할 때에도 `*` 문자를 사용할 수 있습니다. 이렇게 하면 배열 기반 필드에 단일 검증 메시지를 쉽게 적용할 수 있습니다.

```
'custom' => [
    'person.*.email' => [
        'unique' => 'Each person must have a unique email address',
    ]
],
```

<a name="validating-passwords"></a>
<!-- ## Validating Passwords -->
## Validating Passwords

<!-- To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object: -->
비밀번호가 충분한 복잡성을 갖추었는지 확인하려면, Laravel의 `Password` 규칙 객체를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

<!-- The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing: -->
`Password` 규칙 객체를 사용하면, 비밀번호가 최소 한 글자, 숫자, 특수 기호, 대소문자 혼합 등 다양한 복잡성 요구사항을 손쉽게 지정할 수 있습니다.

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
또한, `uncompromised` 메서드를 사용하면 공개적으로 유출된 비밀번호 데이터에 포함된 적이 있는지 확인하여, 유출된 비밀번호 사용을 방지할 수 있습니다.

```
Password::min(8)->uncompromised()
```

<!-- Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security. -->
내부적으로 `Password` 규칙 객체는 [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) 모델을 활용하여, 사용자의 개인정보나 보안을 침해하지 않는 선에서 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 비밀번호 유출 여부를 검사합니다.

<!-- By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method: -->
기본적으로, 데이터 유출 내역에 한 번이라도 등장한 비밀번호는 유출된 것으로 간주되며, `uncompromised` 메서드의 첫 번째 인자를 통해 이 기준을 바꿀 수 있습니다.

```
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

<!-- Of course, you may chain all the methods in the examples above: -->
물론 위의 메서드들을 모두 체인으로 연결하여 사용할 수 있습니다.

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
애플리케이션에서 비밀번호 검증 규칙을 한 번에 정의해두고 재사용하고 싶을 때가 있을 수 있습니다. 이때는 `Password::defaults` 메서드에 클로저를 전달하여 기본 규칙 구성을 지정하면 됩니다. 이 `defaults` 메서드에 전달하는 클로저는 기본 구성을 반환해야 하며, 일반적으로 `defaults` 규칙 등록은 서비스 제공자의 `boot` 메서드에서 설정합니다.

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
이후, 해당 기본 규칙을 검증에 적용하려면 아래와 같이 인자 없이 `defaults` 메서드를 호출하면 됩니다.

```
'password' => ['required', Password::defaults()],
```

<!-- Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this: -->
가끔 기본 비밀번호 규칙 외에 추가적인 검증 규칙을 붙이고 싶을 때는, `rules` 메서드를 사용할 수 있습니다.

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
Laravel은 다양한 유효성 검증 규칙을 제공합니다. 그러나 나만의 특별한 규칙이 필요할 수도 있습니다. 이럴 때 "규칙 객체(rule object)"를 이용하여 사용자 정의 검증 규칙을 정의할 수 있습니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용할 수 있습니다. 예를 들어, 문자열이 모두 대문자인지 검사하는 규칙을 만들어보겠습니다. 새롭게 생성된 규칙 객체는 `app/Rules` 디렉토리에 저장되며, 디렉토리가 없다면 Artisan 명령 실행 시 자동으로 생성됩니다.

```
php artisan make:rule Uppercase
```

<!-- Once the rule has been created, we are ready to define its behavior. A rule object contains two methods: `passes` and `message`. The `passes` method receives the attribute value and name, and should return `true` or `false` depending on whether the attribute value is valid or not. The `message` method should return the validation error message that should be used when validation fails: -->
생성이 완료되면, 해당 규칙의 동작을 정의할 준비가 된 것입니다. 규칙 객체엔 두 가지 메서드가 있습니다: `passes`와 `message`. `passes`는 필드명과 값이 인자로 전달되어, 유효할 경우 `true`, 아니면 `false`를 반환해야 합니다. `message`는 유효성 검증에 실패할 때 사용할 에러 메시지를 반환합니다.

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class Uppercase implements Rule
{
    /**
     * Determine if the validation rule passes.
     *
     * @param  string  $attribute
     * @param  mixed  $value
     * @return bool
     */
    public function passes($attribute, $value)
    {
        return strtoupper($value) === $value;
    }

    /**
     * Get the validation error message.
     *
     * @return string
     */
    public function message()
    {
        return 'The :attribute must be uppercase.';
    }
}
```

<!-- You may call the `trans` helper from your `message` method if you would like to return an error message from your translation files: -->
만약 에러 메시지를 다국어 파일에서 불러오고 싶다면, `message` 메서드에서 `trans` 헬퍼를 사용할 수 있습니다.

```
/**
 * Get the validation error message.
 *
 * @return string
 */
public function message()
{
    return trans('validation.uppercase');
}
```

<!-- Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules: -->
이제 이 규칙 객체를 유효성 검증에 사용할 수 있으며, 다른 유효성 규칙과 함께 인스턴스를 전달하면 됩니다.

```
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

<!-- #### Accessing Additional Data -->
#### Accessing Additional Data

<!-- If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation: -->
사용자 정의 유효성 검증 규칙 클래스에서 검증 중인 모든 데이터를 접근해야 한다면, 해당 클래스에서 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현하면 됩니다. 이때 `setData` 메서드를 정의해야 하며, Laravel이 유효성 검증 전에 내부적으로 해당 메서드를 호출해 검증 데이터 전체를 전달합니다.

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;
use Illuminate\Contracts\Validation\DataAwareRule;

class Uppercase implements Rule, DataAwareRule
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
만약 유효성 검증을 수행하는 validator 인스턴스 자체에 접근해야 한다면, `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다.

```
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;

class Uppercase implements Rule, ValidatorAwareRule
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
애플리케이션 전반에서 재사용할 필요 없이, 특정 곳에서 한 번만 규칙이 필요한 경우라면, 별도의 클래스 대신 클로저를 사용할 수 있습니다. 이 클로저는 필드명, 값, 그리고 검증 실패 시 호출할 `$fail` 콜백을 인수로 받습니다.

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
기본적으로, 검증 대상 필드가 없거나 빈 문자열일 경우에는 일반 규칙과 사용자 정의 규칙을 포함한 대부분의 유효성 검증은 실행되지 않습니다. 예를 들어, [`unique`](#rule-unique) 규칙은 빈 문자열에 대해 실행되지 않습니다.

```
use Illuminate\Support\Facades\Validator;

$rules = ['name' => 'unique:users,name'];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

<!-- For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To create an "implicit" rule, implement the `Illuminate\Contracts\Validation\ImplicitRule` interface. This interface serves as a "marker interface" for the validator; therefore, it does not contain any additional methods you need to implement beyond the methods required by the typical `Rule` interface. -->
사용자 정의 규칙이 비어 있거나 없는 값에도 항상 실행되게 하려면, 해당 규칙이 "필수"임을 암묵적으로 나타내야 합니다. 즉, `Illuminate\Contracts\Validation\ImplicitRule` 인터페이스를 구현하세요. 이 인터페이스는 자체적인 추가 메서드가 있는 것은 아니며, 일반적인 `Rule` 인터페이스에 필요한 메서드 외에는 추가 구현 없이 validator에서 "암묵적으로 필수"로 판단하게 해주는 마커 인터페이스 역할만 합니다.

<!-- To generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option : -->
새로운 암묵적 규칙 객체를 생성하려면 `make:rule` Artisan 명령어에 `--implicit` 옵션을 추가하면 됩니다.

```
 php artisan make:rule Uppercase --implicit
```

> [!NOTE]
> "암묵적(implicit)" 규칙은 해당 필드가 "필수"임을 _암시_ 할 뿐입니다. 실제로 필드가 없거나 비어 있는 경우를 에러로 처리할지는 규칙 메서드를 어떻게 구현했는지에 달려 있습니다.
