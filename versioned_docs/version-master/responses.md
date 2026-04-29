# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 첨부하기](#attaching-headers-to-responses)
    - [응답에 쿠키 첨부하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트하기](#redirecting-external-domains)
    - [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트리밍 응답](#streamed-responses)
    - [스트리밍 응답 소비하기](#consuming-streamed-responses)
    - [스트리밍 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림 (SSE)](#event-streams)
    - [스트리밍 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 돌려보낼 응답을 반환해야 합니다. Laravel은 응답을 반환하는 여러 가지 방법을 제공합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트와 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/master/eloquent-collections)도 반환할 수 있다는 사실을 알고 계셨나요? 이 컬렉션은 자동으로 JSON으로 변환됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서 단순한 문자열이나 배열만 반환하지는 않습니다. 대신 완전한 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/master/views)를 반환하게 됩니다.

완전한 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 사용자 정의할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이 클래스는 HTTP 응답을 구성하기 위한 다양한 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

라우트와 컨트롤러에서 [Eloquent ORM](/docs/master/eloquent) 모델과 컬렉션을 직접 반환할 수도 있습니다. 이렇게 하면 Laravel은 모델의 [숨겨진 속성](/docs/master/eloquent-serialization#hiding-attributes-from-json)을 존중하면서 모델과 컬렉션을 자동으로 JSON 응답으로 변환합니다.

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 첨부하기

대부분의 응답 메서드는 체이닝할 수 있으므로 응답 인스턴스를 유창하게 구성할 수 있다는 점을 기억하세요. 예를 들어 응답을 사용자에게 돌려보내기 전에 `header` 메서드를 사용하여 여러 헤더를 응답에 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용하여 응답에 추가할 헤더 배열을 지정할 수 있습니다.

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

`withoutHeader` 메서드를 사용하여 나가는 응답에서 특정 헤더를 제거할 수 있습니다.

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
#### Cache Control 미들웨어

Laravel에는 라우트 그룹의 `Cache-Control` 헤더를 빠르게 설정하는 데 사용할 수 있는 `cache.headers` 미들웨어가 포함되어 있습니다. 지시문은 해당 cache-control 지시문에 대응하는 "snake case" 형식으로 제공해야 하며, 세미콜론으로 구분해야 합니다. 지시문 목록에 `etag`가 지정되어 있으면 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다.

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a name="attaching-cookies-to-responses"></a>
### 응답에 쿠키 첨부하기

`cookie` 메서드를 사용하여 나가는 `Illuminate\Http\Response` 인스턴스에 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 그리고 쿠키가 유효하다고 간주될 시간(분)을 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 덜 자주 사용되는 몇 가지 추가 인수도 받습니다. 일반적으로 이러한 인수는 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 메서드에 전달하는 인수와 같은 목적과 의미를 가집니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

나가는 응답과 함께 쿠키가 전송되도록 보장하고 싶지만 아직 해당 응답 인스턴스가 없다면, `Cookie` 파사드를 사용하여 응답이 전송될 때 쿠키가 첨부되도록 "큐에 넣을" 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인수를 받습니다. 이러한 쿠키는 브라우저로 전송되기 전에 나가는 응답에 첨부됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고 싶다면, 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부되지 않는 한 클라이언트로 다시 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키를 조기에 만료시키기

나가는 응답의 `withoutCookie` 메서드를 통해 쿠키를 만료시켜 제거할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

아직 나가는 응답 인스턴스가 없다면 `Cookie` 파사드의 `expire` 메서드를 사용하여 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 Laravel이 생성한 모든 쿠키는 암호화되고 서명됩니다. 따라서 클라이언트가 쿠키를 수정하거나 읽을 수 없습니다. 애플리케이션에서 생성한 일부 쿠키에 대해 암호화를 비활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화하지 않아야 합니다. 비활성화하면 쿠키가 클라이언트 측 데이터 노출과 변조 위험에 노출됩니다.

<a name="redirects"></a>
## 리다이렉트 (Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```
제출된 폼이 유효하지 않은 경우처럼, 사용자를 이전 위치로 리다이렉트하고 싶을 때가 있습니다. 이때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/master/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하고 있는지 확인해야 합니다.

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 이름이 지정된 라우트로 리다이렉트

매개변수 없이 `redirect` 헬퍼를 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되며, 이를 통해 `Redirector` 인스턴스의 모든 메서드를 호출할 수 있습니다. 예를 들어 이름이 지정된 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다.

```php
return redirect()->route('login');
```

라우트에 매개변수가 있다면, `route` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통해 매개변수 채우기

Eloquent 모델에서 채워지는 "ID" 매개변수를 가진 라우트로 리다이렉트하는 경우, 모델 자체를 전달할 수 있습니다. ID는 자동으로 추출됩니다.

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 매개변수에 들어갈 값을 사용자 지정하고 싶다면, 라우트 매개변수 정의에서 컬럼을 지정하거나(`/profile/{id:slug}`), Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다.

```php
/**
 * Get the value of the model's route key.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리다이렉트

[컨트롤러 액션](/docs/master/controllers)으로 리다이렉트를 생성할 수도 있습니다. 이렇게 하려면 컨트롤러와 액션 이름을 `action` 메서드에 전달합니다.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 매개변수가 필요하다면, `action` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

때로는 애플리케이션 외부의 도메인으로 리다이렉트해야 할 수 있습니다. 이때 `away` 메서드를 호출하면 추가적인 URL 인코딩, 유효성 검증, 확인 절차 없이 `RedirectResponse`를 생성할 수 있습니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 플래시된 세션 데이터와 함께 리다이렉트

새 URL로 리다이렉트하는 작업과 [데이터를 세션에 플래시하는 작업](/docs/master/session#flash-data)은 보통 동시에 수행됩니다. 일반적으로 어떤 작업을 성공적으로 수행한 뒤, 성공 메시지를 세션에 플래시할 때 사용합니다. 편의를 위해 하나의 유창한 메서드 체인으로 `RedirectResponse` 인스턴스를 생성하고 데이터를 세션에 플래시할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 뒤에는 [세션](/docs/master/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade 문법](/docs/master/blade)을 사용하면 다음과 같습니다.

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트

사용자를 새 위치로 리다이렉트하기 전에 현재 요청의 입력 데이터를 세션에 플래시하려면 `RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 사용할 수 있습니다. 일반적으로 사용자가 유효성 검증 오류를 만났을 때 사용합니다. 입력값이 세션에 플래시되고 나면, 다음 요청에서 이를 쉽게 [조회하여](/docs/master/requests#retrieving-old-input) 폼을 다시 채울 수 있습니다.

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입 (Other Response Types)

`response` 헬퍼는 다른 타입의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. 인수 없이 `response` 헬퍼를 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/master/contracts)의 구현체가 반환됩니다. 이 컨트랙트는 응답을 생성하는 데 유용한 여러 메서드를 제공합니다.

<a name="view-responses"></a>
### View 응답

응답의 상태와 헤더를 제어해야 하지만, 응답의 콘텐츠로 [뷰](/docs/master/views)도 반환해야 한다면 `view` 메서드를 사용해야 합니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

물론 사용자 지정 HTTP 상태 코드나 사용자 지정 헤더를 전달할 필요가 없다면, 전역 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 전달된 배열을 PHP의 `json_encode` 함수를 사용해 JSON으로 변환합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하고 싶다면, `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정된 경로의 파일을 사용자의 브라우저가 다운로드하도록 강제하는 응답을 생성하는 데 사용할 수 있습니다. `download` 메서드는 두 번째 인수로 파일명을 받으며, 이 파일명은 파일을 다운로드하는 사용자에게 표시될 파일명을 결정합니다. 마지막으로 세 번째 인수로 HTTP 헤더 배열을 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드되는 파일의 파일명이 ASCII여야 합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 이미지나 PDF 같은 파일을 다운로드로 시작하지 않고 사용자의 브라우저에 직접 표시하는 데 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 파일의 절대 경로를 받고, 두 번째 인수로 헤더 배열을 받습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트리밍 응답 (Streamed Responses)

데이터가 생성되는 즉시 클라이언트로 스트리밍하면, 특히 매우 큰 응답에서 메모리 사용량을 크게 줄이고 성능을 향상시킬 수 있습니다. 스트리밍 응답을 사용하면 서버가 데이터를 모두 보내기 전에 클라이언트가 데이터 처리를 시작할 수 있습니다.

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // Simulate delay between chunks...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의를 위해 `stream` 메서드에 전달한 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel은 제너레이터가 반환하는 문자열 사이마다 출력 버퍼를 자동으로 플러시하고 Nginx 출력 버퍼링도 비활성화합니다.

```php
Route::post('/chat', function () {
    return response()->stream(function (): Generator {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```
<a name="consuming-streamed-responses"></a>
### 스트리밍 응답 사용하기

스트리밍 응답은 Laravel의 `stream` npm 패키지를 사용하여 사용할 수 있습니다. 이 패키지는 Laravel 응답 스트림과 이벤트 스트림을 다루기 위한 편리한 API를 제공합니다. 시작하려면 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그런 다음 `useStream`을 사용하여 이벤트 스트림을 사용할 수 있습니다. 스트림 URL을 제공하면, Laravel 애플리케이션에서 콘텐츠가 반환될 때마다 hook이 연결된 응답으로 `data`를 자동으로 업데이트합니다:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, isFetching, isStreaming, send } = useStream("chat");

    const sendMessage = () => {
        send({
            message: `Current timestamp: ${Date.now()}`,
        });
    };

    return (
        <div>
            <div>{data}</div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
            <button onClick={sendMessage}>Send Message</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, isFetching, isStreaming, send } = useStream("chat");

const sendMessage = () => {
    send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
        <button @click="sendMessage">Send Message</button>
    </div>
</template>
```

`send`를 통해 스트림으로 데이터를 다시 전송할 때는 새 데이터를 보내기 전에 스트림에 대한 활성 연결이 취소됩니다. 모든 요청은 JSON `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` hook은 애플리케이션에 `POST` 요청을 보내므로 유효한 CSRF 토큰이 필요합니다. CSRF 토큰을 제공하는 가장 쉬운 방법은 [애플리케이션 레이아웃의 head에 meta 태그로 포함하는 것](/docs/master/csrf#csrf-x-csrf-token)입니다.

`useStream`에 전달되는 두 번째 인수는 스트림 사용 동작을 사용자 정의할 수 있는 옵션 객체입니다. 이 객체의 기본값은 아래와 같습니다:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        id: undefined,
        initialInput: undefined,
        headers: undefined,
        csrfToken: undefined,
        onResponse: (response: Response) => void,
        onData: (data: string) => void,
        onCancel: () => void,
        onFinish: () => void,
        onError: (error: Error) => void,
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response: Response) => void,
    onData: (data: string) => void,
    onCancel: () => void,
    onFinish: () => void,
    onError: (error: Error) => void,
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

`onResponse`는 스트림에서 최초 응답을 성공적으로 받은 후 실행되며, 원본 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response)가 콜백에 전달됩니다. `onData`는 각 청크를 받을 때마다 호출되며, 현재 청크가 콜백에 전달됩니다. `onFinish`는 스트림이 완료되었을 때와 fetch / read 사이클 중 오류가 발생했을 때 호출됩니다.

기본적으로 초기화 시점에는 스트림으로 요청을 보내지 않습니다. `initialInput` 옵션을 사용하여 스트림에 초기 페이로드를 전달할 수 있습니다:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        initialInput: {
            message: "Introduce yourself.",
        },
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

스트림을 수동으로 취소하려면 hook에서 반환되는 `cancel` 메서드를 사용할 수 있습니다:

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, cancel } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, cancel } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <button @click="cancel">Cancel</button>
    </div>
</template>
```

`useStream` hook을 사용할 때마다 스트림을 식별하기 위한 무작위 `id`가 생성됩니다. 이 값은 각 요청마다 `X-STREAM-ID` 헤더에 담겨 서버로 다시 전송됩니다. 여러 컴포넌트에서 같은 스트림을 사용할 때는 직접 `id`를 제공하여 해당 스트림을 읽고 쓸 수 있습니다:

```tsx tab=React
// App.tsx
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, id } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <StreamStatus id={id} />
        </div>
    );
}

// StreamStatus.tsx
import { useStream } from "@laravel/stream-react";

function StreamStatus({ id }) {
    const { isFetching, isStreaming } = useStream("chat", { id });

    return (
        <div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
        </div>
    );
}
```
```vue tab=Vue
<!-- App.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";
import StreamStatus from "./StreamStatus.vue";

const { data, id } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <StreamStatus :id="id" />
    </div>
</template>

<!-- StreamStatus.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const props = defineProps<{
    id: string;
}>();

const { isFetching, isStreaming } = useStream("chat", { id: props.id });
</script>

<template>
    <div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
    </div>
</template>
```

<a name="streamed-json-responses"></a>
### 스트리밍 JSON 응답

JSON 데이터를 점진적으로 스트리밍해야 한다면 `streamJson` 메서드를 사용할 수 있습니다. 이 메서드는 JavaScript에서 쉽게 파싱할 수 있는 형식으로 큰 데이터셋을 브라우저에 단계적으로 보내야 할 때 특히 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 스트리밍이 끝난 뒤 데이터를 JSON으로 파싱하려 시도한다는 점을 제외하면 [useStream 훅](#consuming-streamed-responses)과 동일합니다.

```tsx tab=React
import { useJsonStream } from "@laravel/stream-react";

type User = {
    id: number;
    name: string;
    email: string;
};

function App() {
    const { data, send } = useJsonStream<{ users: User[] }>("users");

    const loadUsers = () => {
        send({
            query: "taylor",
        });
    };

    return (
        <div>
            <ul>
                {data?.users.map((user) => (
                    <li>
                        {user.id}: {user.name}
                    </li>
                ))}
            </ul>
            <button onClick={loadUsers}>Load Users</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useJsonStream } from "@laravel/stream-vue";

type User = {
    id: number;
    name: string;
    email: string;
};

const { data, send } = useJsonStream<{ users: User[] }>("users");

const loadUsers = () => {
    send({
        query: "taylor",
    });
};
</script>

<template>
    <div>
        <ul>
            <li v-for="user in data?.users" :key="user.id">
                {{ user.id }}: {{ user.name }}
            </li>
        </ul>
        <button @click="loadUsers">Load Users</button>
    </div>
</template>
```

<a name="event-streams"></a>
### 이벤트 스트림(SSE)

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 서버 전송 이벤트(server-sent events, SSE) 스트리밍 응답을 반환하는 데 사용할 수 있습니다. `eventStream` 메서드는 클로저를 받으며, 이 클로저는 응답을 사용할 수 있게 되는 즉시 스트림에 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php)해야 합니다.

```php
Route::get('/chat', function () {
    return response()->eventStream(function () {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

이벤트 이름을 사용자 지정하려면 `StreamedEvent` 클래스의 인스턴스를 yield할 수 있습니다.

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 사용하기

이벤트 스트림은 Laravel의 `stream` npm 패키지를 사용하여 소비할 수 있습니다. 이 패키지는 Laravel 이벤트 스트림과 상호작용하기 위한 편리한 API를 제공합니다. 시작하려면 `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그런 다음 `useEventStream`을 사용하여 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, Laravel 애플리케이션에서 메시지가 반환될 때 훅이 이어 붙인 응답으로 `message`를 자동으로 업데이트합니다.

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/chat");

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat");
</script>

<template>
  <div>{{ message }}</div>
</template>
```

`useEventStream`에 전달하는 두 번째 인수는 스트림 소비 동작을 사용자 지정하는 데 사용할 수 있는 옵션 객체입니다. 이 객체의 기본값은 아래와 같습니다.

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    eventName: "update",
    onMessage: (message) => {
      //
    },
    onError: (error) => {
      //
    },
    onComplete: () => {
      //
    },
    endSignal: "</stream>",
    glue: " ",
  });

  return <div>{message}</div>;
}
```
```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat", {
  eventName: "update",
  onMessage: (message) => {
    // ...
  },
  onError: (error) => {
    // ...
  },
  onComplete: () => {
    // ...
  },
  endSignal: "</stream>",
  glue: " ",
});
</script>
```

이벤트 스트림은 애플리케이션 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해 수동으로 사용할 수도 있습니다. `eventStream` 메서드는 스트림이 완료되면 이벤트 스트림에 `</stream>` 업데이트를 자동으로 전송합니다:

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
});
```

이벤트 스트림에 전송되는 마지막 이벤트를 커스터마이징하려면 `StreamedEvent` 인스턴스를 `eventStream` 메서드의 `endStreamWith` 인수에 전달할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

때로는 특정 작업의 문자열 응답을, 해당 작업의 내용을 디스크에 쓰지 않고 다운로드 가능한 응답으로 변환하고 싶을 수 있습니다. 이런 경우 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 선택 사항인 헤더 배열을 인수로 받습니다:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## 응답 매크로 (Response Macros)

여러 라우트와 컨트롤러에서 재사용할 수 있는 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/master/providers) 중 하나의 `boot` 메서드에서 호출해야 합니다. 예를 들어 `App\Providers\AppServiceProvider` 서비스 프로바이더에서 호출할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인수로 이름을 받고, 두 번째 인수로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현체 또는 `response` 헬퍼에서 매크로 이름을 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```
