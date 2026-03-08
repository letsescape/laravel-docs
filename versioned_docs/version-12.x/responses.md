# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가](#attaching-headers-to-responses)
    - [응답에 쿠키 추가](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [명명된 라우트로 리다이렉트](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트](#redirecting-external-domains)
    - [세션 데이터와 함께 리다이렉트](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트림 응답](#streamed-responses)
    - [스트림 응답 소비](#consuming-streamed-responses)
    - [스트림 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림(SSE)](#event-streams)
    - [스트림 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성 (Creating Responses)

<a name="strings-arrays"></a>
#### 문자열과 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 반환될 응답을 반환해야 합니다. Laravel은 응답을 반환하는 여러 가지 방법을 제공합니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

```php
Route::get('/', function () {
    return 'Hello World';
});
```

라우트나 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections)도 라우트나 컨트롤러에서 반환할 수 있다는 사실을 알고 계셨나요? 자동으로 JSON으로 변환됩니다. 한 번 시도해 보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로 라우트 액션에서는 단순한 문자열이나 배열만 반환하지 않고, 보통은 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/12.x/views)를 반환합니다.

완전한 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드나 헤더를 원하는 대로 커스터마이즈할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속받아 HTTP 응답 생성을 위한 다양한 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델과 컬렉션

[Eloquent ORM](/docs/12.x/eloquent) 모델이나 컬렉션도 라우트/컨트롤러에서 직접 반환할 수 있습니다. 이렇게 하면, Laravel이 모델 및 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨김 속성](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)을 준수합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가

대부분의 응답 메서드는 체이닝(메서드 연결)을 지원하므로, 유연하게 응답을 구성할 수 있습니다. 예를 들어, `header` 메서드를 이용해 여러 개의 헤더를 응답에 추가할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는 `withHeaders` 메서드를 사용해 배열로 여러 헤더를 한 번에 지정할 수도 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

`withoutHeader` 메서드를 활용하면, 전송되는 응답에서 특정 헤더를 제거할 수 있습니다:

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
#### 캐시 컨트롤 미들웨어

Laravel에는 `cache.headers` 미들웨어가 포함되어 있어 라우트 그룹에 대해 간편하게 `Cache-Control` 헤더를 설정할 수 있습니다. 캐시 디렉티브는 대응되는 cache-control 디렉티브를 "snake case"로 변환해 세미콜론(`;`)으로 구분하여 전달합니다. 만약 디렉티브 목록에 `etag`가 포함되어 있다면, 응답 본문의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

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
### 응답에 쿠키 추가

`Illuminate\Http\Response` 인스턴스에서 `cookie` 메서드를 사용해 송신 응답에 쿠키를 추가할 수 있습니다. 이 메서드는 쿠키의 이름, 값, 유효 시간(분 단위)을 받습니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 추가적으로 자주 사용되지 않는 몇 가지 인자를 더 받을 수 있습니다. 대체로 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 동일한 의미를 가집니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

만약 아직 응답 인스턴스가 없지만, 송신 응답에 쿠키를 동봉하고 싶다면 `Cookie` 파사드를 사용하여 쿠키를 "큐잉"할 수 있습니다. `queue` 메서드는 쿠키 생성에 필요한 인자를 받아, 있는 응답이 브라우저로 전송되기 전에 해당 쿠키가 자동으로 첨부되도록 합니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하려면, 글로벌 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부되지 않는 한 클라이언트에 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 조기 만료

응답의 `withoutCookie` 메서드를 사용하여 쿠키를 만료시켜 제거할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

송신 응답 인스턴스가 아직 없다면, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수도 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로, `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에 Laravel이 생성하는 모든 쿠키는 암호화되고 서명되어 클라이언트가 임의로 수정하거나 읽을 수 없습니다. 애플리케이션에서 생성하는 일부 쿠키만 암호화하지 않으려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화하지 않아야 합니다. 암호화를 끄면 쿠키가 클라이언트 측에 노출되어 데이터 변조 및 침해 위험이 있습니다.

<a name="redirects"></a>
## 리다이렉트 (Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 올바른 헤더를 포함합니다. 여러 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 글로벌 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

사용자가 기존 위치로 이동하도록 리다이렉트하고 싶을 때가 있습니다. 예를 들어, 제출한 폼이 유효하지 않은 경우입니다. 이때 글로벌 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 활용하므로, `web` 미들웨어 그룹이 해당 라우트에 적용되어 있어야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 명명된 라우트로 리다이렉트

`redirect` 헬퍼를 인자 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어, 다양한 메서드를 자유롭게 사용할 수 있습니다. 예를 들어, 명명된 라우트로 리다이렉트하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 매개변수가 필요한 경우, 두 번째 인자로 전달하면 됩니다:

```php
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델을 통한 파라미터 자동 전달

"Eloquent 모델의 ID" 파라미터가 필요한 라우트에 리다이렉트할 때는, 직접 ID가 아닌 모델 객체를 전달할 수 있습니다. 그러면 ID가 자동으로 추출되어 사용됩니다:

```php
// URI가 /profile/{id}인 라우트의 경우

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어갈 값을 커스터마이즈하고 싶다면, 라우트 정의에서 컬럼명을 지정(`/profile/{id:slug}`)하거나, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

```php
/**
 * 모델의 라우트 키 값을 반환합니다.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리다이렉트

[컨트롤러 액션](/docs/12.x/controllers)으로 리다이렉트를 생성할 수도 있습니다. `action` 메서드에는 컨트롤러와 액션 이름을 전달하면 됩니다:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우, 두 번째 인자로 파라미터를 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

애플리케이션 외부의 도메인으로 리다이렉트가 필요한 경우가 있습니다. 이럴 때는 추가적인 URL 인코딩이나 검증 없이 `away` 메서드를 사용하면 됩니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 데이터와 함께 리다이렉트

새로운 URL로 리다이렉트하면서 [데이터를 세션에 플래시(flash)](/docs/12.x/session#flash-data)하는 경우가 많습니다. 보통은 어떤 작업에 성공했을 때 성공 메시지를 세션에 플래시합니다. `RedirectResponse` 인스턴스를 생성하고 메서드 체이닝을 활용해 세션에 데이터를 플래시할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후에는 [세션](/docs/12.x/session)에 저장된 플래시 메시지를 확인해 표시할 수 있습니다. 예시로 [Blade 문법](/docs/12.x/blade) 사용:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트

`RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 사용해, 현재 요청의 입력값을 세션에 플래시한 후 새 위치로 리다이렉트할 수 있습니다. 주로 유효성 검증 오류가 발생했을 때 사용하며, 다음 요청에서 [입력값을 조회](/docs/12.x/requests#retrieving-old-input)하여 폼을 다시 채울 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입 (Other Response Types)

`response` 헬퍼를 사용해 다양한 타입의 응답 인스턴스를 생성할 수 있습니다. 아무 인자 없이 호출할 경우, `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/12.x/contracts)가 반환됩니다. 이 컨트랙트에는 다양한 편리한 응답 생성 메서드가 포함되어 있습니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드나 헤더 값을 직접 제어하면서, 동시에 [뷰](/docs/12.x/views)를 반환해야 한다면 `view` 메서드를 사용하면 됩니다:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

커스텀 HTTP 상태 코드나 헤더가 필요하지 않다면, 간단히 글로벌 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 자동으로 `Content-Type` 헤더를 `application/json`으로 설정하고, 전달한 배열을 PHP의 `json_encode` 함수로 JSON 문자열로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 만들고 싶다면, `json`과 `withCallback` 메서드를 조합해 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드를 사용해, 브라우저가 지정한 경로의 파일을 강제로 다운로드하도록 응답을 생성할 수 있습니다. 이때 두 번째 인자에 파일명이 들어가며, 브라우저에서 보이게 될 파일명이 됩니다. 마지막 세 번째 인자에는 HTTP 헤더 배열도 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드 대상 파일이 반드시 ASCII 파일명을 가져야 한다는 점에 주의하세요.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드를 사용하면 이미지를 비롯한 파일(PDF 등)을 다운로드하지 않고, 브라우저 내에서 바로 표시할 수 있습니다. 첫 번째 인자에는 파일의 절대 경로, 두 번째 인자에는 헤더 배열이 들어갑니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트림 응답 (Streamed Responses)

데이터가 생성되는 즉시 클라이언트로 스트리밍하면, 메모리 사용량을 크게 줄이고 성능을 개선할 수 있습니다. 특히 데이터의 양이 많은 응답에 효과적입니다. 스트림 응답은 서버에서 모든 데이터를 전송하기 전에 클라이언트가 먼저 데이터를 받아 처리할 수 있게 해줍니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 청크 간 지연 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의를 위해, `stream` 메서드에 전달하는 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel이 각 문자열 청크마다 자동으로 출력 버퍼를 비우고, Nginx의 출력 버퍼링도 비활성화합니다:

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
### 스트림 응답 소비

스트림 응답은 Laravel의 `stream` npm 패키지를 사용해 소비할 수 있습니다. 이 패키지는 Laravel 응답 및 이벤트 스트림과 상호작용하는 편리한 API를 제공합니다. 먼저, `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그 다음, `useStream` 훅을 사용해 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, 훅이 자동으로 Laravel 애플리케이션에서 반환된 콘텐츠를 이어붙여서 `data`에 업데이트합니다:

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

`send`를 사용해 데이터를 스트림에 보낼 때, 활성화된 스트림 접속이 중단되고 새 데이터가 전송됩니다. 모든 요청은 JSON `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내기 때문에, 유효한 CSRF 토큰이 필요합니다. 가장 쉬운 방법은 [메타 태그로 레이아웃의 head에 포함](/docs/12.x/csrf#csrf-x-csrf-token)하는 것입니다.

`useStream`의 두 번째 인자는 옵션 객체로, 스트림 소비 동작을 세밀하게 제어할 수 있습니다. 기본 값은 아래와 같습니다:

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

`onResponse`는 스트림에서 최초 응답을 성공적으로 받으면 트리거되며, 콜백에 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) 객체를 전달합니다. `onData`는 각 데이터 청크를 받을 때마다 호출되어 해당 청크를 콜백에 전달합니다. `onFinish`는 스트림이 종료되거나 fetch/읽기 과정에서 에러가 발생하면 호출됩니다.

기본적으로, 스트림을 초기화할 때 요청이 자동으로 발생하지 않습니다. `initialInput` 옵션을 사용해 초기 페이로드를 전달하면, 스트림 생성 시 자동으로 데이터를 전송할 수 있습니다:

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

스트림을 수동으로 취소하려면, 훅에서 반환된 `cancel` 메서드를 사용할 수 있습니다:

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

`useStream` 훅을 사용할 때마다 스트림을 식별하기 위한 랜덤 `id`가 생성됩니다. 이 id는 각 요청의 `X-STREAM-ID` 헤더로 서버에 전달됩니다. 여러 컴포넌트에서 같은 스트림을 사용하려면, 직접 `id`를 제공하여 같은 스트림을 읽고 쓸 수 있습니다:

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
### 스트림 JSON 응답

점진적으로 JSON 데이터를 스트리밍하려면 `streamJson` 메서드를 사용할 수 있습니다. 이 방법은 거대한 데이터셋을 자바스크립트에서 쉽게 파싱하도록 점진적으로 브라우저에 전송할 때 특히 유용합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 유사하지만, 스트림 종료 시 자동으로 데이터를 JSON으로 파싱하려 시도합니다:

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
### 이벤트 스트림 (SSE)

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용해 서버 전송 이벤트(Server-Sent Events, SSE) 스트림 응답을 반환할 수 있습니다. 이 메서드는 클로저를 인자로 받아, 해당 클로저에서 스트림에 반환할 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php)하면 됩니다:

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

이벤트의 이름을 커스터마이즈하려면, `StreamedEvent` 클래스의 인스턴스를 `yield`할 수 있습니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비

이벤트 스트림은 Laravel의 `stream` npm 패키지를 사용해서도 소비할 수 있습니다. 이 패키지는 Laravel 이벤트 스트림과 상호작용하는 API를 제공합니다. `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 먼저 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그 다음, `useEventStream` 훅을 사용하면 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, 반환되는 메시지들이 `message` 변수에 이어집니다:

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

`useEventStream`의 두 번째 인자는 옵션 객체로, 스트림 소비 방식을 직접 조절할 수 있습니다. 기본 값은 아래와 같습니다:

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

이벤트 스트림도 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해 프론트엔드에서 직접 다룰 수 있습니다. `eventStream` 메서드는 스트림이 완료되면 자동으로 `</stream>` 메시지를 전송합니다:

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

최종 이벤트를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인자로 `StreamedEvent` 인스턴스를 전달할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트림 다운로드

어떤 작업의 문자열 결과를 파일로 저장하지 않고 곧바로 다운로드 응답으로 반환하고 싶을 때, `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일 이름, 선택적으로 헤더 배열을 인자로 받습니다:

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

여러 라우트 및 컨트롤러에서 재사용 가능한 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 프로바이더](/docs/12.x/providers), 예를 들어 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 좋습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

`macro` 함수는 첫 번째 인자로 이름, 두 번째 인자로 클로저를 받습니다. 매크로 이름을 `ResponseFactory` 구현이나 `response` 헬퍼에서 호출하면, 해당 클로저가 실행됩니다:

```php
return response()->caps('foo');
```
