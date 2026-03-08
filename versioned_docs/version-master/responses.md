# HTTP 응답 (HTTP Responses)

- [응답 생성](#creating-responses)
    - [응답에 헤더 추가하기](#attaching-headers-to-responses)
    - [응답에 쿠키 추가하기](#attaching-cookies-to-responses)
    - [쿠키와 암호화](#cookies-and-encryption)
- [리다이렉트](#redirects)
    - [네임드 라우트로 리다이렉트](#redirecting-named-routes)
    - [컨트롤러 액션으로 리다이렉트](#redirecting-controller-actions)
    - [외부 도메인으로 리다이렉트](#redirecting-external-domains)
    - [세션 플래시 데이터와 함께 리다이렉트](#redirecting-with-flashed-session-data)
- [기타 응답 타입](#other-response-types)
    - [뷰 응답](#view-responses)
    - [JSON 응답](#json-responses)
    - [파일 다운로드](#file-downloads)
    - [파일 응답](#file-responses)
- [스트리밍 응답](#streamed-responses)
    - [스트리밍 응답 소비하기](#consuming-streamed-responses)
    - [스트리밍 JSON 응답](#streamed-json-responses)
    - [이벤트 스트림(SSE)](#event-streams)
    - [스트리밍 다운로드](#streamed-downloads)
- [응답 매크로](#response-macros)

<a name="creating-responses"></a>
## 응답 생성

<a name="strings-arrays"></a>
#### 문자열 및 배열

모든 라우트와 컨트롤러는 사용자의 브라우저로 반환할 응답을 반환해야 합니다. Laravel은 다양한 방식으로 응답을 반환할 수 있도록 지원합니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 해당 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다:

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
> [Eloquent 컬렉션](/docs/master/eloquent-collections)도 라우트나 컨트롤러에서 직접 반환할 수 있다는 사실을 알고 계셨나요? Eloquent 컬렉션도 자동으로 JSON으로 변환됩니다. 한번 사용해보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로는 라우트 액션에서 단순한 문자열이나 배열만 반환하는 경우가 많지 않습니다. 대신, 전체 `Illuminate\Http\Response` 인스턴스 또는 [뷰](/docs/master/views)를 반환하게 됩니다.

`Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드나 헤더를 자유롭게 지정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하므로, 다양한 HTTP 응답을 구축할 수 있는 여러 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent 모델 및 컬렉션

[ Eloquent ORM ](/docs/master/eloquent) 모델과 컬렉션도 라우트와 컨트롤러에서 직접 반환할 수 있습니다. 이 경우 Laravel은 모델 및 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [숨겨진 속성](/docs/master/eloquent-serialization#hiding-attributes-from-json)을 자동으로 적용합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 추가하기

대부분의 응답 메서드는 체이닝(매서드 연결)이 가능하여, 응답 인스턴스를 유연하게 조립할 수 있습니다. 예를 들어, `header` 메서드를 사용해 여러 헤더를 응답에 추가한 뒤 사용자에게 전송할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

또는, `withHeaders` 메서드를 사용하여 헤더 배열을 한 번에 지정할 수도 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

`withoutHeader` 메서드를 사용하면 응답에서 특정 헤더를 제거할 수 있습니다:

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
#### 캐시 컨트롤 미들웨어

Laravel에는 `cache.headers` 미들웨어가 내장되어 있어, 라우트 그룹별로 손쉽게 `Cache-Control` 헤더를 설정할 수 있습니다. 각 디렉티브는 해당 cache-control 디렉티브의 "스네이크 케이스" 형태로 작성하며, 세미콜론(;)으로 구분합니다. 디렉티브 목록에 `etag`가 포함되어 있을 경우 응답 내용의 MD5 해시가 ETag 식별자로 자동 설정됩니다:

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
### 응답에 쿠키 추가하기

`cookie` 메서드를 통해 반환할 `Illuminate\Http\Response` 인스턴스에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키 이름, 값, 유효 기간(분)을 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` 메서드는 추가적으로 몇 가지 인수를 더 받을 수 있습니다. 일반적으로 이 인수들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 동일한 의미를 갖습니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

아직 응답 인스턴스가 없지만 쿠키를 응답에 반드시 포함시키고 싶다면, `Cookie` 파사드를 사용해 쿠키를 "큐잉(queue)"할 수 있습니다. `queue` 메서드는 쿠키 생성에 필요한 인수들을 받으며, 큐에 담긴 쿠키는 브라우저로 전송되기 전 응답에 자동 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성하기

나중에 응답 인스턴스에 첨부할 수 있도록 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 직접 생성하려면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이렇게 생성된 쿠키는 응답 인스턴스에 포함되지 않는 한 클라이언트로 전송되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### 쿠키 미리 만료시키기

`withoutCookie` 메서드를 사용해 반환하는 응답에서 쿠키를 만료시켜 제거할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');
```

아직 반환 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, Laravel에서 생성되는 모든 쿠키는 암호화 및 서명되어, 클라이언트가 내용을 읽거나 조작할 수 없습니다. 애플리케이션에서 생성되는 일부 쿠키의 암호화를 끄고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에 있는 `encryptCookies` 메서드를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화하지 않아야 합니다. 암호화를 해제하면 클라이언트 측에서 쿠키 데이터가 노출되거나 변조될 위험이 있습니다.

<a name="redirects"></a>
## 리다이렉트

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. 여러 가지 방법으로 `RedirectResponse` 인스턴스를 생성할 수 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때로는 제출된 폼이 유효하지 않을 때처럼, 사용자를 이전 위치로 리다이렉트하고 싶을 수 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [세션](/docs/master/session)을 활용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하고 있어야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 네임드 라우트로 리다이렉트

`redirect` 헬퍼를 인수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스를 반환합니다. 이를 통해 `Redirector` 인스턴스의 다양한 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요한 경우, `route` 메서드의 두 번째 인수로 전달합니다:

```php
// 예: /profile/{id} 라우트에 대해

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 라우트 파라미터 채우기

"ID" 파라미터가 Eloquent 모델로 채워지는 라우트로 리다이렉트할 때는 모델 인스턴스를 직접 전달할 수 있습니다. 이 경우 ID가 자동으로 추출됩니다:

```php
// 예: /profile/{id} 라우트에 대해

return redirect()->route('profile', [$user]);
```

라우트 파라미터에 들어가는 값을 직접 지정하고 싶다면, 라우트 파라미터 정의에서 컬럼을 명시(`/profile/{id:slug}`)하거나, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다:

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

[컨트롤러 액션](/docs/master/controllers)으로 리다이렉트도 가능합니다. 컨트롤러 명과 액션 이름을 `action` 메서드에 전달하면 됩니다:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

컨트롤러 라우트에 파라미터가 필요한 경우, 두 번째 인수로 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리다이렉트

때때로 애플리케이션 외의 도메인으로 리다이렉트해야 할 필요가 있습니다. 이럴 때는 `away` 메서드를 사용합니다. 이 메서드는 추가적인 URL 인코딩, 검증 또는 확인 없이 바로 `RedirectResponse`를 생성합니다:

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### 세션 플래시 데이터와 함께 리다이렉트

새 URL로 리다이렉트하면서 [데이터를 세션에 플래시](/docs/master/session#flash-data)하는 경우가 대부분입니다. 예를 들어 어떤 작업이 성공적으로 수행된 후, 성공 메시지를 세션에 플래시하는 경우가 이에 해당합니다. 보다 편리하게, `RedirectResponse` 인스턴스와 세션 플래시 데이터 생성을 메서드 체이닝으로 한번에 할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

사용자가 리다이렉트된 후에는 [세션](/docs/master/session)에 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/master/blade)에서 다음과 같이 표시할 수 있습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 입력값과 함께 리다이렉트

`RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 사용해, 현재 요청의 입력 데이터를 세션에 플래시한 후 새로운 위치로 리다이렉트할 수 있습니다. 일반적으로 유효성 검사에 실패한 경우 이렇게 활용합니다. 입력 데이터가 세션에 플래시된 이후 다음 요청에서 [입력값을 손쉽게 복원](/docs/master/requests#retrieving-old-input)할 수 있습니다:

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 기타 응답 타입

`response` 헬퍼를 사용해 다양한 타입의 응답 인스턴스를 생성할 수 있습니다. 이 헬퍼를 인수 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [컨트랙트](/docs/master/contracts) 구현체가 반환됩니다. 이 컨트랙트는 여러 유용한 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태 코드와 헤더를 직접 제어해야 하면서, 동시에 [뷰](/docs/master/views)도 응답 내용으로 반환하고 싶다면 `view` 메서드를 사용하세요:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

만약 커스텀 HTTP 상태 코드나 헤더를 지정할 필요가 없다면 전역 `view` 헬퍼 함수를 바로 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 지정한 배열을 `json_encode`로 자동 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 응답을 생성하고 싶다면 `json` 메서드와 함께 `withCallback` 메서드를 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 지정한 경로의 파일을 사용자의 브라우저에서 바로 다운로드하게 만듭니다. 두 번째 인수로 파일명을 지정하면, 실제 다운로드 받을 때 표시될 파일명이 됩니다. 마지막으로, 세 번째 인수에는 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드될 파일명이 반드시 ASCII 문자여야 합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 예를 들어 이미지나 PDF 등 파일을 다운로드하지 않고 사용자 브라우저에서 직접 표시할 수 있게 해줍니다. 첫 번째 인수로 파일의 절대 경로, 두 번째 인수로는 헤더 배열을 전달할 수 있습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## 스트리밍 응답

데이터를 생성 즉시 클라이언트로 스트리밍하면 메모리 사용량을 크게 줄이고, 특히 매우 큰 응답에서 성능을 개선할 수 있습니다. 스트리밍 응답은 서버가 데이터를 모두 전송하기 전에 클라이언트가 먼저 처리를 시작할 수 있게 해줍니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // 조각 사이의 지연을 시뮬레이션...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

편의상, `stream` 메서드에 전달한 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel은 생성기가 반환하는 문자열 사이마다 자동으로 출력 버퍼를 플러시하고 Nginx 버퍼링도 비활성화합니다:

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
### 스트리밍 응답 소비하기

스트리밍 응답은 Laravel의 `stream` npm 패키지를 사용해 소비할 수 있습니다. 이 패키지는 Laravel 응답 및 이벤트 스트림과 상호작용할 수 있는 편리한 API를 제공합니다. 먼저, `@laravel/stream-react` 또는 `@laravel/stream-vue` 패키지를 설치하세요:

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

그런 다음, 스트림 URL을 전달하면 `useStream`을 통해 이벤트 스트림을 소비할 수 있습니다. 해당 훅에서는 서버에서 응답 콘텐츠가 반환될 때마다 `data`에 내용을 누적하여 자동 업데이트합니다:

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

`send`를 통해 데이터를 스트림에 전송하면, 새로운 데이터를 전송하기 전에 기존의 활성 스트림 연결을 취소합니다. 모든 요청은 JSON `POST` 요청으로 전달됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. 가장 편리한 방법은 [레이아웃 head에 메타 태그로 CSRF 토큰을 포함](/docs/master/csrf#csrf-x-csrf-token)하는 것입니다.

`useStream`에 전달되는 두 번째 인수는 스트림 취득 동작을 커스터마이즈할 수 있는 옵션 객체입니다. 이 객체의 기본값은 다음과 같습니다:

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

`onResponse`는 스트림에서 최초로 성공적 응답을 받은 후 호출되며, 원시 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response)가 콜백에 전달됩니다. `onData`는 각 데이터 조각을 받을 때마다 호출되고, `onFinish`는 스트림이 완료되거나 fetch/read 과정에 에러가 발생할 때 호출됩니다.

기본적으로 스트림은 초기화 시 즉시 요청을 보내지 않습니다. `initialInput` 옵션을 사용해 스트림으로 처음 보낼 페이로드를 정의할 수 있습니다:

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

각각의 `useStream` 훅이 호출되면, 스트림 식별을 위한 랜덤한 `id`가 생성되어 매 요청마다 `X-STREAM-ID` 헤더에 전송됩니다. 여러 컴포넌트에서 동일한 스트림을 읽고 쓸 때는 직접 `id`를 지정할 수 있습니다:

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

JSON 데이터를 점진적으로 전송(스트리밍)하려면 `streamJson` 메서드를 사용할 수 있습니다. 이 방법은 대용량 데이터를 점차적으로 브라우저에 전송해야 하면서, JavaScript로 쉽게 파싱이 가능한 형태가 필요할 때 유용합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 동일하게 동작하면서, 스트리밍 완료 시 데이터를 JSON으로 파싱해 처리해줍니다:

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

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 서버-센트 이벤트(SSE) 스트리밍 응답을 반환할 수 있게 해줍니다. 이때, 스트림에 반환할 응답이 준비될 때마다 클로저에서 [yield](https://www.php.net/manual/en/language.generators.overview.php)하면 됩니다:

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

이벤트 이름을 커스터마이즈하고 싶으면 `StreamedEvent` 클래스 인스턴스를 yield 하면 됩니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비하기

이벤트 스트림도 Laravel의 `stream` npm 패키지를 사용해 편리하게 소비할 수 있습니다. 패키지 설치 후, `useEventStream` 훅으로 이벤트 스트림을 사용할 수 있습니다. Laravel 애플리케이션에서 메시지가 반환되면, hook에서는 `message`에 응답이 누적되어 자동 갱신됩니다:

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

`useEventStream`에 전달할 수 있는 옵션 객체의 기본값은 아래와 같습니다:

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

이벤트 스트림은 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 이용해 프론트엔드에서 직접 수동으로 소비할 수도 있습니다. `eventStream` 메서드는 스트림이 끝나면 자동으로 `</stream>` 이벤트를 전송합니다:

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

마지막에 이벤트 스트림에 전송할 이벤트를 커스터마이즈하려면, `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 전달하면 됩니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### 스트리밍 다운로드

어떤 연산 결과 문자열을 파일로 저장하지 않고 바로 다운로드 응답으로 제공하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고(선택적으로) 헤더 배열을 인수로 받습니다:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
## 응답 매크로

공통으로 재사용할 커스텀 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 이용할 수 있습니다. 보통 이 메서드는 `App\Providers\AppServiceProvider` 같은 애플리케이션의 [서비스 프로바이더](/docs/master/providers) 내 `boot` 메서드에서 호출합니다:

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

`macro` 함수는 첫 번째 인수로 매크로 이름, 두 번째 인수로 클로저를 받습니다. 매크로로 등록된 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```
