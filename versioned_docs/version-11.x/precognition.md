<!-- # Precognition -->
# Precognition

- [Introduction](#introduction)
- [Live Validation](#live-validation)
    - [Using Vue](#using-vue)
    - [Using Vue and Inertia](#using-vue-and-inertia)
    - [Using React](#using-react)
    - [Using React and Inertia](#using-react-and-inertia)
    - [Using Alpine and Blade](#using-alpine)
    - [Configuring Axios](#configuring-axios)
- [Customizing Validation Rules](#customizing-validation-rules)
- [Handling File Uploads](#handling-file-uploads)
- [Managing Side-Effects](#managing-side-effects)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel Precognition allows you to anticipate the outcome of a future HTTP request. One of the primary use cases of Precognition is the ability to provide "live" validation for your frontend JavaScript application without having to duplicate your application's backend validation rules. Precognition pairs especially well with Laravel's Inertia-based [starter kits](/docs/11.x/starter-kits). -->
Laravel 프리코그니션(Precognition)을 사용하면, 앞으로 발생할 HTTP 요청의 결과를 미리 예측할 수 있습니다. 프리코그니션의 대표적인 활용 사례는, 프런트엔드 자바스크립트 애플리케이션에서 이미 정의한 백엔드 검증 규칙을 중복해서 구현하지 않고도 "실시간" 유효성 검증 기능을 제공하는 것입니다. 프리코그니션은 특히 Laravel의 Inertia 기반 [starter kits](/docs/11.x/starter-kits)와 함께 사용할 때 매우 유용합니다.

<!-- When Laravel receives a "precognitive request", it will execute all of the route's middleware and resolve the route's controller dependencies, including validating [form requests](/docs/11.x/validation#form-request-validation) - but it will not actually execute the route's controller method. -->
Laravel이 "프리코그니티브(precognitive) 요청"을 받으면, 해당 라우트의 모든 미들웨어를 실행하고 라우트 컨트롤러의 의존성도 모두 해결합니다(여기에는 [form requests](/docs/11.x/validation#form-request-validation)를 통한 유효성 검증도 포함됩니다). 단, 실제로 라우트의 컨트롤러 메서드 자체는 실행되지 않습니다.

<a name="live-validation"></a>
<!-- ## Live Validation -->
## Live Validation

<a name="using-vue"></a>
<!-- ### Using Vue -->
### Using Vue

<!-- Using Laravel Precognition, you can offer live validation experiences to your users without having to duplicate your validation rules in your frontend Vue application. To illustrate how it works, let's build a form for creating new users within our application. -->
Laravel 프리코그니션을 활용하면, 프런트엔드 Vue 애플리케이션에서 유효성 검증 규칙을 중복 정의할 필요 없이 사용자에게 실시간 유효성 검증을 제공할 수 있습니다. 예시로 새로운 사용자를 생성하는 폼을 만드는 과정을 살펴보겠습니다.

<!-- First, to enable Precognition for a route, the `HandlePrecognitiveRequests` middleware should be added to the route definition. You should also create a [form request](/docs/11.x/validation#form-request-validation) to house the route's validation rules: -->
먼저, 라우트에서 프리코그니션을 활성화하려면, 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가해야 합니다. 또한, 해당 라우트의 유효성 검증 규칙을 담을 [form request](/docs/11.x/validation#form-request-validation) 클래스를 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

<!-- Next, you should install the Laravel Precognition frontend helpers for Vue via NPM: -->
다음으로, 프런트엔드에서 Vue용 Laravel 프리코그니션 헬퍼를 NPM을 통해 설치합니다.

```shell
npm install laravel-precognition-vue
```

<!-- With the Laravel Precognition package installed, you can now create a form object using Precognition's `useForm` function, providing the HTTP method (`post`), the target URL (`/users`), and the initial form data. -->
패키지 설치가 완료되면, 프리코그니션의 `useForm` 함수를 사용하여 폼 오브젝트를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 요청 URL(`/users`), 초기 폼 데이터 등을 전달합니다.

<!-- Then, to enable live validation, invoke the form's `validate` method on each input's `change` event, providing the input's name: -->
실시간 유효성 검증을 사용하려면 각 입력값의 `change` 이벤트 발생 시 폼의 `validate` 메서드를 호출하고, 해당 입력의 이름을 인수로 넘겨줍니다.

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

<!-- Now, as the form is filled by the user, Precognition will provide live validation output powered by the validation rules in the route's form request. When the form's inputs are changed, a debounced "precognitive" validation request will be sent to your Laravel application. You may configure the debounce timeout by calling the form's `setValidationTimeout` function: -->
이제 사용자가 폼을 입력하는 동안, 라우트의 폼 리퀘스트에 정의된 유효성 검증 규칙을 기반으로 프리코그니션이 실시간 검증 결과를 제공합니다. 폼 입력값이 변경되면 디바운스된(지연 처리되는) "프리코그니티브" 유효성 검증 요청이 Laravel 애플리케이션에 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

<!-- When a validation request is in-flight, the form's `validating` property will be `true`: -->
유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```html
<div v-if="form.validating">
    Validating...
</div>
```

<!-- Any validation errors returned during a validation request or a form submission will automatically populate the form's `errors` object: -->
유효성 검증 또는 폼 제출 시 발생한 모든 검증 오류는 자동으로 폼의 `errors` 객체에 저장됩니다.

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

<!-- You can determine if the form has any errors using the form's `hasErrors` property: -->
폼에 검증 오류가 있는지 여부는 폼의 `hasErrors` 속성을 통해 확인할 수 있습니다.

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

<!-- You may also determine if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions, respectively: -->
특정 입력값의 검증 통과 또는 실패 여부는 각 입력의 이름을 `valid` 또는 `invalid` 함수에 전달해서 확인할 수도 있습니다.

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> 입력 필드는 사용자가 값을 변경하고, 그에 대한 검증 응답이 도착한 경우에만 유효(Valid) 혹은 무효(Invalid)로 표시됩니다.

<!-- If you are validating a subset of a form's inputs with Precognition, it can be useful to manually clear errors. You may use the form's `forgetError` function to achieve this: -->
폼의 일부 입력값만 프리코그니션으로 검증하는 경우, 오류를 직접 지워야 할 수도 있습니다. 폼의 `forgetError` 함수를 사용하면 특정 입력값의 오류를 수동으로 제거할 수 있습니다.

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

<!-- As we have seen, you can hook into an input's `change` event and validate individual inputs as the user interacts with them; however, you may need to validate inputs that the user has not yet interacted with. This is common when building a "wizard", where you want to validate all visible inputs, whether the user has interacted with them or not, before moving to the next step. -->
이처럼 입력값의 `change` 이벤트에 검증 로직을 연결해 개별 입력값을 검증할 수 있지만, 사용자가 아직 한 번도 만지지 않은 다른 입력값도 검증이 필요한 경우가 있습니다. 예를 들어, "다음 단계"로 넘어가기 전 모든 표시된 입력값의 유효성을 확인하고 싶을 때 많이 사용됩니다.

<!-- To do this with Precognition, you should call the `validate` method passing the field names you wish to validate to the `only` configuration key. You may handle the validation result with `onSuccess` or `onValidationError` callbacks: -->
이 경우에는 `validate` 메서드에 `only` 옵션을 사용하여 검증할 필드명을 배열로 넘겨줍니다. 검증 결과에 따라 `onSuccess` 또는 `onValidationError` 콜백도 등록할 수 있습니다.

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

<!-- Of course, you may also execute code in reaction to the response to the form submission. The form's `submit` function returns an Axios request promise. This provides a convenient way to access the response payload, reset the form inputs on successful submission, or handle a failed request: -->
또한 폼 서버 제출 응답에 따른 후속 처리를 할 수도 있습니다. `submit` 함수는 Axios 요청 Promise를 반환하므로, 응답을 받아 폼 입력값 초기화, 성공/실패 처리 등을 할 수 있습니다.

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

<!-- You may determine if a form submission request is in-flight by inspecting the form's `processing` property: -->
폼 전송 요청이 진행 중인지 여부는 폼의 `processing` 속성을 확인하면 됩니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-vue-and-inertia"></a>
<!-- ### Using Vue and Inertia -->
### Using Vue and Inertia

> [!NOTE]
> Vue와 Inertia로 Laravel 애플리케이션을 개발할 때 시작을 쉽게 하려면, [starter kits](/docs/11.x/starter-kits)를 사용하는 것이 좋습니다. 스타터 키트에는 백엔드와 프런트엔드의 인증 관련 기본 구조가 포함되어 있습니다.

<!-- Before using Precognition with Vue and Inertia, be sure to review our general documentation on [using Precognition with Vue](#using-vue). When using Vue with Inertia, you will need to install the Inertia compatible Precognition library via NPM: -->
Vue와 Inertia에서 프리코그니션을 사용하기 전, [using Precognition with Vue](#using-vue) 문서도 함께 읽어보시기 바랍니다. Inertia와 함께 Vue를 사용할 때는, Inertia 호환 프리코그니션 라이브러리를 NPM으로 설치해야 합니다.

```shell
npm install laravel-precognition-vue-inertia
```

<!-- Once installed, Precognition's `useForm` function will return an Inertia [form helper](https://inertiajs.com/forms#form-helper) augmented with the validation features discussed above. -->
설치가 완료되면, 프리코그니션의 `useForm` 함수가 Inertia의 [form helper](https://inertiajs.com/forms#form-helper)에 위에서 설명한 유효성 검증 기능을 결합하여 반환합니다.

<!-- The form helper's `submit` method has been streamlined, removing the need to specify the HTTP method or URL. Instead, you may pass Inertia's [visit options](https://inertiajs.com/manual-visits) as the first and only argument. In addition, the `submit` method does not return a Promise as seen in the Vue example above. Instead, you may provide any of Inertia's supported [event callbacks](https://inertiajs.com/manual-visits#event-callbacks) in the visit options given to the `submit` method: -->
폼 헬퍼의 `submit` 메서드는, HTTP 메서드나 URL을 별도로 지정할 필요 없이 Inertia의 [visit options](https://inertiajs.com/manual-visits)를 첫 번째(그리고 유일한) 인자로 받습니다. 또한 `submit` 메서드는 위 Vue 예시와 달리 Promise를 반환하지 않습니다. 대신, `submit` 메서드에 전달하는 visit 옵션에 Inertia에서 지원하는 [event callbacks](https://inertiajs.com/manual-visits#event-callbacks)을 지정하면 됩니다.

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit({
    preserveScroll: true,
    onSuccess: () => form.reset(),
});
</script>
```

<a name="using-react"></a>
<!-- ### Using React -->
### Using React

<!-- Using Laravel Precognition, you can offer live validation experiences to your users without having to duplicate your validation rules in your frontend React application. To illustrate how it works, let's build a form for creating new users within our application. -->
Laravel 프리코그니션을 활용하면, 프런트엔드 React 애플리케이션에서도 유효성 검증 규칙을 중복 정의하지 않고 실시간 검증을 제공할 수 있습니다. 새로운 사용자를 생성하는 폼 예시를 통해 동작 방식을 설명하겠습니다.

<!-- First, to enable Precognition for a route, the `HandlePrecognitiveRequests` middleware should be added to the route definition. You should also create a [form request](/docs/11.x/validation#form-request-validation) to house the route's validation rules: -->
먼저, 라우트에서 프리코그니션을 사용하려면 `HandlePrecognitiveRequests` 미들웨어를 등록해야 하며, 해당 라우트의 유효성 검증 규칙을 담을 [form request](/docs/11.x/validation#form-request-validation) 클래스를 생성해야 합니다.

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

<!-- Next, you should install the Laravel Precognition frontend helpers for React via NPM: -->
이후, React용 Laravel 프리코그니션 프런트엔드 헬퍼를 NPM으로 설치합니다.

```shell
npm install laravel-precognition-react
```

<!-- With the Laravel Precognition package installed, you can now create a form object using Precognition's `useForm` function, providing the HTTP method (`post`), the target URL (`/users`), and the initial form data. -->
패키지 설치가 완료되면, `useForm` 함수를 사용해 폼 오브젝트를 만들 수 있습니다. HTTP 메서드(`post`), 라우트 경로(`/users`), 초기 폼 데이터를 인수로 넘깁니다.

<!-- To enable live validation, you should listen to each input's `change` and `blur` event. In the `change` event handler, you should set the form's data with the `setData` function, passing the input's name and new value. Then, in the `blur` event handler invoke the form's `validate` method, providing the input's name: -->
실시간 유효성 검증을 위해 각 입력의 `change`와 `blur` 이벤트를 모두 감지해야 합니다. `change` 이벤트에서는 `setData` 함수로 폼 데이터를 갱신하고, `blur` 이벤트에서는 `validate` 메서드를 호출하면서 해당 입력의 이름을 전달합니다.

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

<!-- Now, as the form is filled by the user, Precognition will provide live validation output powered by the validation rules in the route's form request. When the form's inputs are changed, a debounced "precognitive" validation request will be sent to your Laravel application. You may configure the debounce timeout by calling the form's `setValidationTimeout` function: -->
이제 사용자가 폼을 입력하는 동안, 라우트 폼 리퀘스트에 정의된 유효성 검증 규칙에 기반해 프리코그니션이 실시간 검증 결과를 제공합니다. 입력값이 변경되면 프리코그니티브 검증 요청이 디바운스되어 전송됩니다. 디바운스 타임아웃은 `setValidationTimeout` 함수로 조정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

<!-- When a validation request is in-flight, the form's `validating` property will be `true`: -->
유효성 검증 요청이 진행 중일 때는 폼의 `validating` 속성이 `true`가 됩니다.

```jsx
{form.validating && <div>Validating...</div>}
```

<!-- Any validation errors returned during a validation request or a form submission will automatically populate the form's `errors` object: -->
유효성 검증이나 폼 제출 시 발생한 모든 검증 오류는 폼의 `errors` 객체에 자동으로 저장됩니다.

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

<!-- You can determine if the form has any errors using the form's `hasErrors` property: -->
폼 전체에 검증 오류가 있는지는 `hasErrors` 속성으로 확인할 수 있습니다.

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

<!-- You may also determine if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions, respectively: -->
특정 입력값의 검증 성공/실패 여부도 `valid`, `invalid` 함수에 입력값 이름을 넘겨 판단합니다.

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> 입력 필드는 값이 변경되고, 해당 값에 대한 검증 응답을 받은 뒤에만 유효(Valid)/무효(Invalid)로 보여집니다.

<!-- If you are validating a subset of a form's inputs with Precognition, it can be useful to manually clear errors. You may use the form's `forgetError` function to achieve this: -->
폼의 일부 입력값만 프리코그니션으로 검증할 경우, 오류를 수동으로 지워야 할 때가 있습니다. 이때는 `forgetError` 함수를 사용할 수 있습니다.

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.value);

        form.forgetError('avatar');
    }}
>
```

<!-- As we have seen, you can hook into an input's `blur` event and validate individual inputs as the user interacts with them; however, you may need to validate inputs that the user has not yet interacted with. This is common when building a "wizard", where you want to validate all visible inputs, whether the user has interacted with them or not, before moving to the next step. -->
위와 같이 각 입력의 `blur` 이벤트에서 개별 검증을 할 수 있지만, 사용자가 아직 만지지 않은 입력값이 남아 있는 상태에서, "다음 단계"로 넘어가기에 앞서 모든 표시 입력값을 검증해야 하는 경우가 있습니다.

<!-- To do this with Precognition, you should call the `validate` method passing the field names you wish to validate to the `only` configuration key. You may handle the validation result with `onSuccess` or `onValidationError` callbacks: -->
이럴 때는 `validate` 메서드에 `only` 옵션을 사용해서 검증할 입력값 배열을 지정하고, 결과에 따라 `onSuccess`, `onValidationError` 콜백을 등록하면 됩니다.

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

<!-- Of course, you may also execute code in reaction to the response to the form submission. The form's `submit` function returns an Axios request promise. This provides a convenient way to access the response payload, reset the form's inputs on a successful form submission, or handle a failed request: -->
폼 제출 과정의 응답에 따라 추가 작업을 하고 싶다면, `submit` 함수가 반환하는 Axios의 Promise에서 응답을 받아 활용할 수 있습니다.

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

<!-- You may determine if a form submission request is in-flight by inspecting the form's `processing` property: -->
폼 전송 요청이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다.

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-react-and-inertia"></a>
<!-- ### Using React and Inertia -->
### Using React and Inertia

> [!NOTE]
> React와 Inertia로 Laravel 애플리케이션을 개발할 때 시작을 쉽게 하려면, [starter kits](/docs/11.x/starter-kits) 사용을 고려해보세요. 스타터 키트는 백엔드와 프런트엔드 인증 기능의 기본 구조를 제공합니다.

<!-- Before using Precognition with React and Inertia, be sure to review our general documentation on [using Precognition with React](#using-react). When using React with Inertia, you will need to install the Inertia compatible Precognition library via NPM: -->
React와 Inertia에서 프리코그니션을 사용하기 전에는, [using Precognition with React](#using-react) 문서를 먼저 참고하세요. Inertia와 React를 함께 사용한다면, Inertia 호환 프리코그니션 라이브러리를 NPM으로 설치해야 합니다.

```shell
npm install laravel-precognition-react-inertia
```

<!-- Once installed, Precognition's `useForm` function will return an Inertia [form helper](https://inertiajs.com/forms#form-helper) augmented with the validation features discussed above. -->
설치가 완료되면, 프리코그니션의 `useForm` 함수가 Inertia의 [form helper](https://inertiajs.com/forms#form-helper)에 앞서 설명한 실시간 유효성 검증 기능을 더해 반환합니다.

<!-- The form helper's `submit` method has been streamlined, removing the need to specify the HTTP method or URL. Instead, you may pass Inertia's [visit options](https://inertiajs.com/manual-visits) as the first and only argument. In addition, the `submit` method does not return a Promise as seen in the React example above. Instead, you may provide any of Inertia's supported [event callbacks](https://inertiajs.com/manual-visits#event-callbacks) in the visit options given to the `submit` method: -->
폼 헬퍼의 `submit` 메서드는 HTTP 메서드나 URL을 지정할 필요 없이 Inertia의 [visit options](https://inertiajs.com/manual-visits)를 첫 번째(그리고 유일한) 인자로 전달합니다. 또한 `submit` 메서드는 위 React 예시와 달리 Promise를 반환하지 않습니다. 대신, `submit` 메서드에 전달하는 visit 옵션에 Inertia에서 제공하는 [event callbacks](https://inertiajs.com/manual-visits#event-callbacks)을 지정할 수 있습니다.

```js
import { useForm } from 'laravel-precognition-react-inertia';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = (e) => {
    e.preventDefault();

    form.submit({
        preserveScroll: true,
        onSuccess: () => form.reset(),
    });
};
```

<a name="using-alpine"></a>
<!-- ### Using Alpine and Blade -->
### Using Alpine and Blade

<!-- Using Laravel Precognition, you can offer live validation experiences to your users without having to duplicate your validation rules in your frontend Alpine application. To illustrate how it works, let's build a form for creating new users within our application. -->
Laravel 프리코그니션을 이용하면, 프런트엔드 Alpine 애플리케이션에서도 유효성 검증 규칙을 중복 정의하지 않고 실시간 검증 경험을 제공할 수 있습니다. 새로운 사용자를 만드는 폼 예제를 통해 설명하겠습니다.

<!-- First, to enable Precognition for a route, the `HandlePrecognitiveRequests` middleware should be added to the route definition. You should also create a [form request](/docs/11.x/validation#form-request-validation) to house the route's validation rules: -->
먼저, 해당 라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가하고, 유효성 검증 규칙을 정의한 [form request](/docs/11.x/validation#form-request-validation) 클래스를 생성합니다.

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

<!-- Next, you should install the Laravel Precognition frontend helpers for Alpine via NPM: -->
다음으로, Alpine용 Laravel 프리코그니션 프런트엔드 헬퍼를 NPM으로 설치합니다.

```shell
npm install laravel-precognition-alpine
```

<!-- Then, register the Precognition plugin with Alpine in your `resources/js/app.js` file: -->
설치 후, `resources/js/app.js` 파일에서 Alpine에 프리코그니션 플러그인을 등록합니다.

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

<!-- With the Laravel Precognition package installed and registered, you can now create a form object using Precognition's `$form` "magic", providing the HTTP method (`post`), the target URL (`/users`), and the initial form data. -->
등록이 완료되면, 프리코그니션의 `$form` "매직"을 사용해 폼 오브젝트를 만들 수 있습니다. HTTP 메서드(`post`), 요청 URL(`/users`), 초기 폼 데이터를 인수로 넘깁니다.

<!-- To enable live validation, you should bind the form's data to its relevant input and then listen to each input's `change` event. In the `change` event handler, you should invoke the form's `validate` method, providing the input's name: -->
실시간 유효성 검증을 위해 입력값과 폼 데이터를 바인딩하고, 각 입력값의 `change` 이벤트를 감지해야 합니다. `change` 이벤트 핸들러에서 폼의 `validate` 메서드를 호출하고 입력값의 이름을 전달합니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

<!-- Now, as the form is filled by the user, Precognition will provide live validation output powered by the validation rules in the route's form request. When the form's inputs are changed, a debounced "precognitive" validation request will be sent to your Laravel application. You may configure the debounce timeout by calling the form's `setValidationTimeout` function: -->
사용자가 폼을 채우는 동안, 라우트 폼 리퀘스트의 유효성 검증 규칙을 바탕으로 프리코그니션이 실시간 검증 결과를 보여줍니다. 입력값이 변경되면 프리코그니티브 검증 요청이 디바운스되어 전송되며, 타임아웃은 `setValidationTimeout`으로 설정할 수 있습니다.

```js
form.setValidationTimeout(3000);
```

<!-- When a validation request is in-flight, the form's `validating` property will be `true`: -->
유효성 검증 요청이 진행 중인지 여부는 폼의 `validating` 속성이 `true`로 표시됩니다.

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

<!-- Any validation errors returned during a validation request or a form submission will automatically populate the form's `errors` object: -->
검증 과정이나 폼 제출 시 발생한 오류는 폼의 `errors` 객체에 자동으로 저장됩니다.

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

<!-- You can determine if the form has any errors using the form's `hasErrors` property: -->
폼에 오류가 있는지 여부는 `hasErrors` 속성으로 확인할 수 있습니다.

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

<!-- You may also determine if an input has passed or failed validation by passing the input's name to the form's `valid` and `invalid` functions, respectively: -->
특정 입력의 검증 통과/실패 여부는 이름을 `valid`/`invalid` 함수에 넘겨 사용할 수 있습니다.

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> 입력 필드는 값이 변경되고, 검증 응답을 받은 뒤에만 유효 또는 무효로 표시됩니다.

<!-- As we have seen, you can hook into an input's `change` event and validate individual inputs as the user interacts with them; however, you may need to validate inputs that the user has not yet interacted with. This is common when building a "wizard", where you want to validate all visible inputs, whether the user has interacted with them or not, before moving to the next step. -->
개별 입력의 `change` 이벤트에 대해 검증 로직을 연결할 수 있지만, 예를 들어 "다음 단계"로 넘어가기 전 모든 표시된 입력값을 검증해야 할 수도 있습니다.

<!-- To do this with Precognition, you should call the `validate` method passing the field names you wish to validate to the `only` configuration key. You may handle the validation result with `onSuccess` or `onValidationError` callbacks: -->
이때는 `validate` 메서드에 `only` 옵션을 사용해 검증할 필드명 목록을 직접 지정할 수 있으며, 결과에 따라 `onSuccess`, `onValidationError` 콜백도 활용할 수 있습니다.

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

<!-- You may determine if a form submission request is in-flight by inspecting the form's `processing` property: -->
폼 제출 요청이 진행 중인지 여부는 `processing` 속성으로 확인할 수 있습니다.

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
<!-- #### Repopulating Old Form Data -->
#### Repopulating Old Form Data

<!-- In the user creation example discussed above, we are using Precognition to perform live validation; however, we are performing a traditional server-side form submission to submit the form. So, the form should be populated with any "old" input and validation errors returned from the server-side form submission: -->
위 예시처럼 프리코그니션을 실시간 검증에만 사용하고, 실제 폼 제출은 전통적인 서버 방식으로 처리하는 경우, 서버에서 반환하는 "이전(old)" 입력값과 유효성 검증 오류로 폼을 자동 채워줄 필요가 있습니다.

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

<!-- Alternatively, if you would like to submit the form via XHR you may use the form's `submit` function, which returns an Axios request promise: -->
또한, 폼을 XHR로 제출하고 싶다면, 폼의 `submit` 함수를 사용할 수 있습니다. 이 함수는 Axios Promise를 반환합니다.

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
<!-- ### Configuring Axios -->
### Configuring Axios

<!-- The Precognition validation libraries use the [Axios](https://github.com/axios/axios) HTTP client to send requests to your application's backend. For convenience, the Axios instance may be customized if required by your application. For example, when using the `laravel-precognition-vue` library, you may add additional request headers to each outgoing request in your application's `resources/js/app.js` file: -->
프리코그니션 유효성 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용해 백엔드에 요청을 보냅니다. 애플리케이션에서 필요하다면 Axios 인스턴스를 자유롭게 커스터마이징할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때, `resources/js/app.js` 파일에서 각 요청에 추가 헤더를 선언할 수 있습니다.

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

<!-- Or, if you already have a configured Axios instance for your application, you may tell Precognition to use that instance instead: -->
이미 별도의 설정이 적용된 Axios 인스턴스를 보유한 경우, 프리코그니션이 해당 인스턴스를 사용하도록 지정할 수도 있습니다.

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

> [!WARNING]
> Inertia 전용 프리코그니션 라이브러리는 유효성 검증 요청에만 커스텀 Axios 인스턴스를 사용합니다. 폼 제출 자체는 항상 Inertia가 직접 처리합니다.

<a name="customizing-validation-rules"></a>
<!-- ## Customizing Validation Rules -->
## Customizing Validation Rules

<!-- It is possible to customize the validation rules executed during a precognitive request by using the request's `isPrecognitive` method. -->
프리코그니티브 요청이 들어올 때 어떤 유효성 검증 규칙을 사용할지 `isPrecognitive` 메서드를 통해 직접 지정할 수 있습니다.

<!-- For example, on a user creation form, we may want to validate that a password is "uncompromised" only on the final form submission. For precognitive validation requests, we will simply validate that the password is required and has a minimum of 8 characters. Using the `isPrecognitive` method, we can customize the rules defined by our form request: -->
예를 들어, 사용자 등록 폼에서 최종 제출 시에만 비밀번호가 "유출되지 않은(uncompromised) 비밀번호"인지 검증하고 싶을 수 있습니다. 프리코그니션 요청에서는 단순히 비밀번호가 필수이고 최소 8자 이상인지 검증만 하면 됩니다. `isPrecognitive` 메서드를 사용하여 폼 리퀘스트 내에서 유효성 검증 규칙을 동적으로 조정할 수 있습니다.

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-file-uploads"></a>
<!-- ## Handling File Uploads -->
## Handling File Uploads

<!-- By default, Laravel Precognition does not upload or validate files during a precognitive validation request. This ensure that large files are not unnecessarily uploaded multiple times. -->
기본적으로, Laravel 프리코그니션은 프리코그니티브 유효성 검증 요청 시 파일 업로드나 파일 유효성 검증을 수행하지 않습니다. 이로 인해 대용량 파일이 불필요하게 여러 번 업로드되는 일을 방지할 수 있습니다.

<!-- Because of this behavior, you should ensure that your application [customizes the corresponding form request's validation rules](#customizing-validation-rules) to specify the field is only required for full form submissions: -->
이런 동작 특성 때문에, [customizes the corresponding form request's validation rules](#customizing-validation-rules) 해서, 실제 폼 전체 제출 시에만 해당 필드가 필수로 요구되도록 처리해야 합니다.

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

<!-- If you would like to include files in every validation request, you may invoke the `validateFiles` function on your client-side form instance: -->
모든 유효성 검증 요청에 파일도 포함하고 싶다면, 프런트엔드 폼 인스턴스에서 `validateFiles` 메서드를 호출하면 됩니다.

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
<!-- ## Managing Side-Effects -->
## Managing Side-Effects

<!-- When adding the `HandlePrecognitiveRequests` middleware to a route, you should consider if there are any side-effects in _other_ middleware that should be skipped during a precognitive request. -->
라우트에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때는, _다른_ 미들웨어에서 프리코그니션 요청에 대해서는 건너뛰어야 하는 부수효과(사이드 이펙트)가 있는지도 꼭 고려해야 합니다.

<!-- For example, you may have a middleware that increments the total number of "interactions" each user has with your application, but you may not want precognitive requests to be counted as an interaction. To accomplish this, we may check the request's `isPrecognitive` method before incrementing the interaction count: -->
예를 들어, 미들웨어에서 각 사용자의 "상호작용 횟수"를 집계하는 로직이 있고, 프리코그니션 요청은 상호작용으로 간주하고 싶지 않을 수 있습니다. 이럴 때는, 요청의 `isPrecognitive` 메서드를 사용해 프리코그니션 요청에서는 상호작용 수를 증가시키지 않도록 제어할 수 있습니다.

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- If you would like to make precognitive requests in your tests, Laravel's `TestCase` includes a `withPrecognition` helper which will add the `Precognition` request header. -->
테스트에서 프리코그니션 요청을 보내고 싶다면, Laravel의 `TestCase`에서 제공하는 `withPrecognition` 헬퍼를 사용하면 됩니다. 이 헬퍼는 `Precognition` 헤더를 요청에 자동으로 추가해줍니다.

<!-- Additionally, if you would like to assert that a precognitive request was successful, e.g., did not return any validation errors, you may use the `assertSuccessfulPrecognition` method on the response: -->
또한, 프리코그니션 요청이 성공적으로 처리되었는지(즉, 유효성 검증 오류가 없었는지) 검사하려면, 응답 객체의 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다.

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```