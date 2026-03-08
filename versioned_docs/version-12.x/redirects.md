# HTTP 리다이렉트 (HTTP Redirects)

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [플래시된 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기 (Creating Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하기 위해 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있으며, 가장 간단한 방법은 전역 `redirect` 헬퍼 함수를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

때때로, 제출된 폼이 유효하지 않을 경우처럼 사용자를 이전 위치로 리다이렉트해야 할 때가 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/12.x/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하거나 세션 미들웨어가 모두 적용되어 있어야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청 유효성 검사...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트하기 (Redirecting To Named Routes)

`redirect` 헬퍼를 인수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, `Redirector`의 메서드들을 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트하는 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

만약 라우트에 매개변수가 있다면, `route` 메서드의 두 번째 인수로 전달하면 됩니다:

```php
// 다음 URI를 가진 라우트의 예: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

편의를 위해, Laravel은 전역 `to_route` 함수도 제공합니다:

```php
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 매개변수 채우기

"ID" 매개변수가 있는 라우트로 리다이렉트할 때, 매개변수를 Eloquent 모델에서 자동으로 추출하려면 모델 자체를 전달할 수 있습니다. 그러면 ID가 자동으로 추출됩니다:

```php
// 다음 URI를 가진 라우트의 예: profile/{id}

return redirect()->route('profile', [$user]);
```

라우트 매개변수에 넣을 값을 커스터마이즈하고 싶다면, Eloquent 모델의 `getRouteKey` 메서드를 오버라이드하면 됩니다:

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
## 컨트롤러 액션으로 리다이렉트하기 (Redirecting To Controller Actions)

[컨트롤러 액션](/docs/12.x/controllers)으로 리다이렉트를 생성할 수도 있습니다. 이때 `action` 메서드에 컨트롤러 및 액션 이름을 전달합니다:

```php
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트에 매개변수가 필요하다면, 두 번째 인수로 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 플래시된 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하면서 동시에 [세션에 데이터를 플래시(한시 저장)](/docs/12.x/session#flash-data)하는 경우가 많습니다. 보통 어떤 작업을 성공적으로 처리한 뒤, 세션에 성공 메시지를 플래시할 때 사용합니다. 편리하게도, `RedirectResponse` 인스턴스를 생성하면서 세션에 데이터를 플래시할 수 있는 체이닝 메서드를 제공합니다:

```php
Route::post('/user/profile', function () {
    // 사용자 프로필 업데이트...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 플래시한 뒤 사용자를 새로운 위치로 리다이렉트할 수 있습니다. 플래시된 입력 데이터는 다음 요청 시 간편하게 [조회할 수 있습니다](/docs/12.x/requests#retrieving-old-input):

```php
return back()->withInput();
```

사용자가 리다이렉트된 후에는, [세션](/docs/12.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/12.x/blade)을 사용하면 다음과 같습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```