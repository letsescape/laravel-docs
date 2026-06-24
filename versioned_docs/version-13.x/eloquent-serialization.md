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
Laravel을 사용해 API를 만들 때 모델과 연관관계를 배열이나 JSON으로 변환해야 하는 경우가 자주 있습니다. Eloquent는 이러한 변환을 편리하게 수행하는 메서드를 제공하며, 모델의 직렬화된 표현에 어떤 속성을 포함할지도 제어할 수 있습니다.

> [!NOTE]
> Eloquent 모델과 컬렉션의 JSON 직렬화를 더욱 견고하게 처리하려면 [Eloquent API resources](/docs/13.x/eloquent-resources) 문서를 확인하세요.

<a name="serializing-models-and-collections"></a>
<!-- ## Serializing Models and Collections -->
## Serializing Models and Collections

<a name="serializing-to-arrays"></a>
<!-- ### Serializing to Arrays -->
### Serializing to Arrays

<!-- To convert a model and its loaded [relationships](/docs/13.x/eloquent-relationships) to an array, you should use the `toArray` method. This method is recursive, so all attributes and all relations (including the relations of relations) will be converted to arrays: -->
모델과 로드된 [relationships](/docs/13.x/eloquent-relationships)를 배열로 변환하려면 `toArray` 메서드를 사용해야 합니다. 이 메서드는 재귀적으로 동작하므로 모든 속성과 모든 연관관계(연관관계의 연관관계 포함)가 배열로 변환됩니다.

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();
```

<!-- The `attributesToArray` method may be used to convert a model's attributes to an array but not its relationships: -->
`attributesToArray` 메서드는 모델의 속성만 배열로 변환하고, 연관관계는 변환하지 않을 때 사용할 수 있습니다.

```php
$user = User::first();

return $user->attributesToArray();
```

<!-- You may also convert entire [collections](/docs/13.x/eloquent-collections) of models to arrays by calling the `toArray` method on the collection instance: -->
컬렉션 인스턴스에서 `toArray` 메서드를 호출하여 모델의 전체 [collections](/docs/13.x/eloquent-collections)을 배열로 변환할 수도 있습니다.

```php
$users = User::all();

return $users->toArray();
```

<a name="serializing-to-json"></a>
<!-- ### Serializing to JSON -->
### Serializing to JSON

<!-- To convert a model to JSON, you should use the `toJson` method. Like `toArray`, the `toJson` method is recursive, so all attributes and relations will be converted to JSON. You may also specify any JSON encoding options that are [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php): -->
모델을 JSON으로 변환하려면 `toJson` 메서드를 사용해야 합니다. `toArray`와 마찬가지로 `toJson` 메서드도 재귀적으로 동작하므로 모든 속성과 연관관계가 JSON으로 변환됩니다. 또한 [supported by PHP](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션을 지정할 수도 있습니다.

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);
```

<!-- Alternatively, you may cast a model or collection to a string, which will automatically call the `toJson` method on the model or collection: -->
또는 모델이나 컬렉션을 문자열로 casting할 수 있으며, 이 경우 모델이나 컬렉션의 `toJson` 메서드가 자동으로 호출됩니다.

```php
return (string) User::find(1);
```

<!-- Since models and collections are converted to JSON when cast to a string, you can return Eloquent objects directly from your application's routes or controllers. Laravel will automatically serialize your Eloquent models and collections to JSON when they are returned from routes or controllers: -->
모델과 컬렉션은 문자열로 casting될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. Laravel은 라우트나 컨트롤러에서 반환된 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<a name="relationships"></a>
<!-- #### Relationships -->
#### Relationships

<!-- When an Eloquent model is converted to JSON, its loaded relationships will automatically be included as attributes on the JSON object. Also, though Eloquent relationship methods are defined using "camel case" method names, a relationship's JSON attribute will be "snake case". -->
Eloquent 모델이 JSON으로 변환되면, 로드된 연관관계는 JSON 객체의 속성으로 자동 포함됩니다. 또한 Eloquent 연관관계 메서드는 "camel case" 메서드 이름으로 정의되지만, 연관관계의 JSON 속성은 "snake case"가 됩니다.

<a name="hiding-attributes-from-json"></a>
<!-- ## Hiding Attributes From JSON -->
## Hiding Attributes From JSON

<!-- Sometimes you may wish to limit the attributes, such as passwords, that are included in your model's array or JSON representation. To do so, you may use the `Hidden` attribute on your model. Attributes that are listed in the `Hidden` attribute will not be included in the serialized representation of your model: -->
때로는 비밀번호와 같은 속성이 모델의 배열 또는 JSON 표현에 포함되지 않도록 제한하고 싶을 수 있습니다. 이를 위해 모델에서 `Hidden` 속성을 사용할 수 있습니다. `Hidden` 속성에 나열된 속성은 모델의 직렬화된 표현에 포함되지 않습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}
```


> [!NOTE]
> 연관관계를 숨기려면 해당 연관관계의 메서드 이름을 Eloquent 모델의 `Hidden` 속성에 추가하세요.

<!-- Alternatively, you may use the `Visible` attribute to define an "allow list" of attributes that should be included in your model's array and JSON representation. All attributes that are not present in the `Visible` attribute will be hidden when the model is converted to an array or JSON: -->
또는 `Visible` 속성을 사용하여 모델의 배열 및 JSON 표현에 포함되어야 하는 속성의 "허용 목록"을 정의할 수 있습니다. `Visible` 속성에 없는 모든 속성은 모델이 배열이나 JSON으로 변환될 때 숨겨집니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}
```

<a name="temporarily-modifying-attribute-visibility"></a>
<!-- #### Temporarily Modifying Attribute Visibility -->
#### Temporarily Modifying Attribute Visibility

<!-- If you would like to make some typically hidden attributes visible on a given model instance, you may use the `makeVisible` or `mergeVisible` methods. The `makeVisible` method returns the model instance: -->
일반적으로 숨겨지는 일부 속성을 특정 모델 인스턴스에서 보이게 하려면 `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다.

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();
```

<!-- Likewise, if you would like to hide some attributes that are typically visible, you may use the `makeHidden` or `mergeHidden` methods: -->
마찬가지로, 일반적으로 보이는 일부 속성을 숨기고 싶다면 `makeHidden` 또는 `mergeHidden` 메서드를 사용할 수 있습니다.

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();
```

<!-- If you wish to temporarily override all of the visible or hidden attributes, you may use the `setVisible` and `setHidden` methods respectively: -->
표시되거나 숨겨지는 모든 속성을 일시적으로 재정의하려면 각각 `setVisible` 및 `setHidden` 메서드를 사용할 수 있습니다.

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();
```

<a name="appending-values-to-json"></a>
<!-- ## Appending Values to JSON -->
## Appending Values to JSON

<!-- Occasionally, when converting models to arrays or JSON, you may wish to add attributes that do not have a corresponding column in your database. To do so, first define an [accessor](/docs/13.x/eloquent-mutators) for the value: -->
모델을 배열이나 JSON으로 변환할 때, 데이터베이스에 대응되는 컬럼이 없는 속성을 추가하고 싶을 때가 있습니다. 이를 위해 먼저 해당 값에 대한 [accessor](/docs/13.x/eloquent-mutators)를 정의합니다.

```php
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

<!-- If you would like the accessor to always be appended to your model's array and JSON representations, you may use the `Appends` attribute on your model. Note that attribute names are typically referenced using their "snake case" serialized representation, even though the accessor's PHP method is defined using "camel case": -->
accessor가 항상 모델의 배열 및 JSON 표현에 추가되도록 하려면 모델에서 `Appends` 속성을 사용할 수 있습니다. accessor의 PHP 메서드는 "camel case"로 정의되지만, 속성 이름은 일반적으로 직렬화된 표현인 "snake case"를 사용해 참조한다는 점에 유의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}
```

<!-- Once the attribute has been added to the `appends` list, it will be included in both the model's array and JSON representations. Attributes in the `appends` array will also respect the `visible` and `hidden` settings configured on the model. -->
속성이 `appends` 목록에 추가되면 모델의 배열 및 JSON 표현에 모두 포함됩니다. `appends` 배열의 속성도 모델에 설정된 `visible` 및 `hidden` 설정을 따릅니다.

<a name="appending-at-run-time"></a>
<!-- #### Appending at Run Time -->
#### Appending at Run Time

<!-- At runtime, you may instruct a model instance to append additional attributes using the `append` or `mergeAppends` methods. Or, you may use the `setAppends` method to override the entire array of appended properties for a given model instance: -->
런타임에는 `append` 또는 `mergeAppends` 메서드를 사용하여 모델 인스턴스에 추가 속성을 덧붙이도록 지시할 수 있습니다. 또는 `setAppends` 메서드를 사용하여 특정 모델 인스턴스에 대해 추가되는 속성 전체 배열을 재정의할 수 있습니다.

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();
```

<!-- Likewise, if you would like to remove all appended properties from a model, you may use the `withoutAppends` method: -->
마찬가지로, 모델에서 추가된 모든 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용할 수 있습니다.

```php
return $user->withoutAppends()->toArray();
```

<a name="date-serialization"></a>
<!-- ## Date Serialization -->
## Date Serialization

<a name="customizing-the-default-date-format"></a>
<!-- #### Customizing the Default Date Format -->
#### Customizing the Default Date Format

<!-- You may customize the default serialization format by overriding the `serializeDate` method. This method does not affect how your dates are formatted for storage in the database: -->
`serializeDate` 메서드를 재정의하여 기본 직렬화 형식을 사용자 지정할 수 있습니다. 이 메서드는 날짜가 데이터베이스에 저장될 때의 형식에는 영향을 주지 않습니다.

```php
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

<!-- You may customize the serialization format of individual Eloquent date attributes by specifying the date format in the model's [cast declarations](/docs/13.x/eloquent-mutators#attribute-casting): -->
모델의 [cast declarations](/docs/13.x/eloquent-mutators#attribute-casting)에 날짜 형식을 지정하여 개별 Eloquent 날짜 속성의 직렬화 형식을 사용자 지정할 수 있습니다.

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}
```
