<!-- # Eloquent: Serialization -->
# Eloquent: Serialization

- [Introduction](#introduction)
- [Serializing Models and Collections](#serializing-models-and-collections)
    - [Serializing to Arrays](#serializing-to-arrays)
    - [Serializing to JSON](#serializing-to-json)
- [Hiding Attributes From JSON](#hiding-attributes-from-json)
- [Appending Values to JSON](#appending-values-to-json)
- [Date Serialization](#date-serialization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When building APIs using Laravel, you will often need to convert your models and relationships to arrays or JSON. Eloquent includes convenient methods for making these conversions, as well as controlling which attributes are included in the serialized representation of your models. -->
Laravel로 API를 개발할 때에는 모델과 연관관계 데이터를 배열이나 JSON 형태로 변환해야 할 때가 많습니다. Eloquent는 이러한 변환 작업을 매우 간편하게 해주는 여러 메서드들을 제공할 뿐만 아니라, 직렬화된 모델에 어떤 속성을 포함할지 제어할 수 있는 기능도 함께 제공합니다.

> [!NOTE]
> Eloquent 모델과 컬렉션을 JSON으로 더욱 정교하게 변환·제어하고 싶다면 [Eloquent API resources](/docs/11.x/eloquent-resources) 문서를 참고하시기 바랍니다.

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models and Collections -->
## Serializing Models and Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing to Arrays -->
### Serializing to Arrays

<!-- To convert a model and its loaded [relationships](/docs/11.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
모델과, 미리 로드된 [relationships](/docs/11.x/eloquent-relationships)까지 배열로 변환하고 싶다면 `toArray` 메서드를 사용하면 됩니다. 이 메서드는 재귀적으로 동작하므로, 모델의 모든 속성뿐만 아니라 모든 연관관계(그리고 그 연관관계의 하위 관계까지)도 모두 배열로 변환됩니다.

```
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` 메서드를 사용하면 모델의 속성만 배열로 변환하고, 연관관계는 포함하지 않습니다.

```
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/11.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
또한 전체 [collections](/docs/11.x/eloquent-collections) 자체를 배열로 변환하려면, 컬렉션 인스턴스에서 `toArray` 메서드를 호출하면 됩니다.

```
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing to JSON -->
### Serializing to JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
모델을 JSON으로 변환하려면 `toJson` 메서드를 사용합니다. `toArray`처럼 `toJson`도 재귀적으로 작동하여 모든 속성과 연관관계가 JSON으로 변환됩니다. 필요하다면 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php)을 지정할 수도 있습니다.

```
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
또는, 모델이나 컬렉션을 문자열로 casting하면 자동으로 `toJson` 메서드가 호출되어 JSON 문자열로 변환됩니다.

```
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
모델과 컬렉션은 문자열로 casting될 때 자동으로 JSON으로 변환되기 때문에, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수도 있습니다. Laravel은 라우트 또는 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

```
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
Eloquent 모델이 JSON으로 변환될 때, 미리 로드된 연관관계도 자동으로 JSON 객체의 속성(attribute)으로 포함됩니다. 참고로, Eloquent의 연관관계 메서드는 일반적으로 "카멜 케이스(camel case)"로 정의하지만, JSON에서는 "스네이크 케이스(snake case)" 형태로 속성 이름이 변환됩니다.

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, add a `$hidden` property to your model. Attributes that are listed in the `$hidden` property's array will not be included in the serialized representation of your model: -->
비밀번호와 같이, 모델의 배열 혹은 JSON 표현에서 특정 속성(예: 보안 민감 정보 등)을 제외하고 싶은 경우가 있습니다. 이럴 때는 모델에 `$hidden` 속성을 추가하면 됩니다. `$hidden` 배열에 기재된 속성들은 직렬화된 결과에서 제외됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be hidden for serialization.
     *
     * @var array<string>
     */
    protected $hidden = ['password'];
}
```

> [!NOTE]
> 만약 연관관계를 숨기고 싶다면, 해당 연관관계 메서드명을 Eloquent 모델의 `$hidden` 배열에 추가하면 됩니다.

<!-- Alternatively, you may use the `visible` property to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `$visible` array will be hidden when the model is converted to an array or JSON: -->
반대로, `visible` 속성을 이용해 모델의 배열, JSON 표현에 포함되어야 하는 속성만 "허용 목록(allow list)" 방식으로 지정할 수도 있습니다. `$visible` 배열에 없는 모든 속성은 모델이 배열이나 JSON으로 변환될 때 숨겨집니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The attributes that should be visible in arrays.
     *
     * @var array
     */
    protected $visible = ['first_name', 'last_name'];
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
<!-- #### Temporarily Modifying Attribute Visibility -->
#### Temporarily Modifying Attribute Visibility

<!-- If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` method. The `makeVisible` method returns the model instance: -->
특정 모델 인스턴스에서 기본적으로 숨겨진 속성을 일시적으로 보이게 하고 싶다면 `makeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```
return $user->makeVisible('attribute')->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` method. -->
반대로, 평소에 노출되는 속성을 임시로 숨기고 싶다면 `makeHidden` 메서드를 사용합니다.

```
return $user->makeHidden('attribute')->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
그리고 공개 또는 비공개 속성 목록 전체를 임시로 재정의하고 싶을 때는 각각 `setVisible`, `setHidden` 메서드를 사용할 수 있습니다.

```
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values to JSON -->
## Appending Values to JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/11.x/eloquent-mutators) for the value: -->
모델을 배열이나 JSON으로 변환할 때, 데이터베이스 컬럼에는 없는 추가 정보를 포함시키고 싶을 때가 있습니다. 이럴 때는 [accessor](/docs/11.x/eloquent-mutators)를 먼저 정의합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}
```

<!-- If you would like the accessor to always be appended to your model's array and JSON representations, you may add the attribute name to the `appends` property of your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
이 accessor가 모델의 배열/JSON 표현에 항상 추가로 포함되길 원한다면, 해당 속성명을 모델의 `appends` 속성에 추가하면 됩니다. 참고로 속성명은 accessor의 PHP 메서드를 "카멜 케이스"로 정의하더라도, 보통 "스네이크 케이스" 직렬화 표현으로 참조합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The accessors to append to the model's array form.
     *
     * @var array
     */
    protected $appends = ['is_admin'];
}
```

<!-- Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON representations. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model. -->
이렇게 `appends`에 추가된 속성은 모델의 배열과 JSON 표현 모두에 포함됩니다. 그리고 `appends` 배열에 있는 속성도 모델에서 설정한 `visible`과 `hidden` 속성의 영향을 받습니다.

<a name="appending-at-run-time"></a>
<!-- #### Appending at Run Time -->
#### Appending at Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` method. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
실행 중에 모델 인스턴스에 추가 속성을 포함시키고 싶다면 `append` 메서드를 사용할 수 있습니다. 그리고 `setAppends` 메서드를 이용하면 해당 인스턴스의 전체 추가 속성 목록을 한 번에 지정할 수 있습니다.

```
return $user->append('is_admin')->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<a name="date-serialization"></a>
<!-- ## Date Serialization -->
## Date Serialization

<a name="customizing-the-default-date-format"></a>
<!-- #### Customizing the Default Date Format -->
#### Customizing the Default Date Format

<!-- You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database: -->
날짜의 직렬화 기본 포맷을 바꾸고 싶을 때는, `serializeDate` 메서드를 오버라이드(재정의)하면 됩니다. 이 메서드는 데이터베이스에 저장되는 날짜 포맷에는 영향을 주지 않습니다.

```
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```

<a name="customizing-the-date-format-per-attribute"></a>
<!-- #### Customizing the Date Format per Attribute -->
#### Customizing the Date Format per Attribute

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/11.x/eloquent-mutators#attribute-casting): -->
특정한 Eloquent 날짜 속성마다 별도의 직렬화 형식을 지정하고 싶을 때는, 모델의 [cast declarations](/docs/11.x/eloquent-mutators#attribute-casting)에서 직접 날짜 형식을 지정할 수 있습니다.

```
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
