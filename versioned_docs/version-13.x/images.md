<!-- # Image Manipulation -->
# Image Manipulation

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Reading Images](#reading-images)
    - [Uploaded Files](#uploaded-files)
    - [Storage Files](#storage-files)
    - [Other Sources](#other-sources)
- [Manipulating Images](#manipulating-images)
    - [Resizing Images](#resizing-images)
    - [Other Transformations](#other-transformations)
- [Encoding Images](#encoding-images)
- [Storing Images](#storing-images)
- [Inspecting Images](#inspecting-images)
- [Image Drivers](#image-drivers)
    - [Custom Image Drivers](#custom-image-drivers)
    - [Custom Transformations](#custom-transformations)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a fluent image manipulation API that allows you to resize, crop, encode, and store images using the same expressive conventions found throughout the framework. Laravel's image features are powered by [Intervention Image](https://image.intervention.io/) and support the GD and Imagick PHP extensions. -->
Laravel은 프레임워크 전반에서 사용하는 표현력 있는 규칙과 동일한 방식으로 이미지를 리사이즈하고, 자르고, 인코딩하고, 저장할 수 있는 유연한 이미지 조작 API를 제공합니다. Laravel의 이미지 기능은 [Intervention Image](https://image.intervention.io/)를 기반으로 하며 GD 및 Imagick PHP 확장을 지원합니다.

<!-- The image API is useful when working with uploaded files, files stored on Laravel [filesystem disks](/docs/13.x/filesystem), local files, remote URLs, or raw image bytes: -->
이미지 API는 업로드된 파일, Laravel의 [filesystem disks](/docs/13.x/filesystem)에 저장된 파일, 로컬 파일, 원격 URL 또는 원시 이미지 바이트를 다룰 때 유용합니다:

```php
use Illuminate\Support\Facades\Image;

$path = Image::fromStorage('avatars/photo.jpg', 'public')
    ->cover(400, 400)
    ->toWebp()
    ->quality(80)
    ->storePublicly('avatars', 'public');
```

> [!WARNING]
> 이미지 조작은 CPU와 메모리를 많이 사용할 수 있습니다. 업로드를 수신하는 HTTP 요청 중에 처리하는 대신 대규모 이미지 처리 작업을 [queued job](/docs/13.x/queues)에서 수행하는 것을 고려하세요.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Before using Laravel's image manipulation features, install the Intervention Image package via Composer: -->
Laravel의 이미지 조작 기능을 사용하기 전에 Composer를 통해 Intervention Image 패키지를 설치합니다:

```shell
composer require intervention/image:^4.0
```

<!-- You should also ensure your PHP installation has either the GD or Imagick extension installed, depending on which driver your application will use. -->
또한 애플리케이션에서 사용할 드라이버에 따라 PHP 설치 환경에 GD 또는 Imagick 확장 기능이 설치되어 있는지 확인해야 합니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Laravel's image configuration file is located at `config/images.php`. If your application does not have an `images` configuration file, you may publish it using the `config:publish` Artisan command: -->
Laravel의 이미지 설정 파일은 `config/images.php`에 있습니다. 애플리케이션에 `images` 설정 파일이 없다면 `config:publish` Artisan 명령어를 사용해 게시할 수 있습니다.

```shell
php artisan config:publish images
```

<!-- The image configuration file allows you to specify your application's default image driver. You may also specify the default driver using the `IMAGE_DRIVER` environment variable. The supported drivers are `gd` and `imagick`: -->
이미지 설정 파일에서 애플리케이션의 기본 이미지 드라이버를 지정할 수 있습니다. `IMAGE_DRIVER` 환경 변수를 사용해 기본 드라이버를 지정할 수도 있습니다. 지원되는 드라이버는 `gd`와 `imagick`입니다:

```ini
IMAGE_DRIVER=imagick
```

<a name="reading-images"></a>
<!-- ## Reading Images -->
## Reading Images

<!-- The `Image` facade provides several methods for reading images from common sources. Image contents are loaded lazily, so the source is typically not read until the image is processed or its bytes are requested. -->
`Image` 파사드는 일반적인 소스에서 이미지를 읽는 여러 메서드를 제공합니다. 이미지 콘텐츠는 지연 로드되므로, 일반적으로 이미지를 처리하거나 해당 바이트를 요청할 때까지 소스를 읽지 않습니다.

<a name="uploaded-files"></a>
<!-- ### Uploaded Files -->
### Uploaded Files

<!-- You may retrieve an uploaded image from an incoming request using the `image` method. This method returns an `Illuminate\Image\Image` instance for the uploaded file, or `null` if the file is not present: -->
들어오는 요청에서 업로드된 이미지를 가져오려면 `image` 메서드를 사용할 수 있습니다. 이 메서드는 업로드된 파일을 나타내는 `Illuminate\Image\Image` 인스턴스를 반환하며, 파일이 없으면 `null`을 반환합니다:

```php
use Illuminate\Http\Request;

Route::post('/avatar', function (Request $request) {
    $request->validate(['avatar' => ['required', 'image']]);

    $path = $request->image('avatar')
        ->cover(400, 400)
        ->toWebp()
        ->storePublicly('avatars', 'public');

    // ...
});
```

<!-- Alternatively, you may create an image instance from an `Illuminate\Http\UploadedFile` instance using the `fromUpload` method: -->
또는 `fromUpload` 메서드를 사용해 `Illuminate\Http\UploadedFile` 인스턴스에서 이미지 인스턴스를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromUpload($request->file('avatar'));
```

<!-- When an image is created from an uploaded file, you may retrieve the underlying uploaded file using the `file` method: -->
업로드된 파일에서 이미지를 생성한 경우 `file` 메서드를 사용해 기반이 된 업로드 파일을 가져올 수 있습니다.

```php
$file = $image->file();
```

<a name="storage-files"></a>
<!-- ### Storage Files -->
### Storage Files

<!-- You may create an image instance from a file stored on one of your application's [filesystem disks](/docs/13.x/filesystem) using the `fromStorage` method. The first argument is the path to the file, while the second argument is the disk name: -->
애플리케이션의 [filesystem disks](/docs/13.x/filesystem)에 저장된 파일에서 `fromStorage` 메서드를 사용해 이미지 인스턴스를 생성할 수 있습니다. 첫 번째 인수는 파일 경로이고 두 번째 인수는 디스크 이름입니다.

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');
```

<!-- You may also create image instances directly from a filesystem disk instance using the `image` method: -->
파일 시스템 디스크 인스턴스에서 `image` 메서드를 사용해 이미지 인스턴스를 직접 생성할 수도 있습니다.

```php
use Illuminate\Support\Facades\Storage;

$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a name="other-sources"></a>
<!-- ### Other Sources -->
### Other Sources

<!-- The `Image` facade also includes methods for creating image instances from raw bytes, local file paths, remote URLs, and Base64 encoded strings: -->
`Image` 파사드에는 원시 바이트, 로컬 파일 경로, 원격 URL, Base64로 인코딩된 문자열에서 이미지 인스턴스를 생성하는 메서드도 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromBytes($contents);
$image = Image::fromBase64($base64);
$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));
$image = Image::fromUrl('https://example.com/photo.jpg');
```

<a name="manipulating-images"></a>
<!-- ## Manipulating Images -->
## Manipulating Images

<!-- Image instances are immutable. Each manipulation method returns a new image instance with the transformation appended to its processing pipeline, allowing methods to be chained fluently: -->
이미지 인스턴스는 변경할 수 없습니다. 각 조작 메서드는 변환이 처리 파이프라인에 추가된 새 이미지 인스턴스를 반환하므로 메서드를 유연하게 연결해 사용할 수 있습니다:

```php
$image = $request->image('avatar')
    ->orient()
    ->cover(400, 400)
    ->sharpen(10);
```

<!-- Transformations are processed in the order they are added to the image pipeline and the image is only encoded once at the end. -->
변환은 이미지 파이프라인에 추가된 순서대로 처리되며, 이미지는 마지막에 한 번만 인코딩됩니다.

<a name="resizing-images"></a>
<!-- ### Resizing Images -->
### Resizing Images

<!-- The `resize` method resizes an image to the given dimensions. You may provide both a width and height, or provide only one dimension using named arguments: -->
`resize` 메서드는 이미지를 지정한 크기로 조정합니다. 너비와 높이를 모두 지정하거나, 이름이 지정된 인수를 사용해 한 가지 크기만 지정할 수 있습니다:

```php
$image = $image->resize(800, 600);
$image = $image->resize(width: 800);
$image = $image->resize(height: 600);
```

<!-- The `scale` method proportionally scales an image down so that it fits within the given dimensions. This method will never increase the size of an image: -->
`scale` 메서드는 이미지가 지정된 크기 안에 맞도록 비율을 유지하면서 축소합니다. 이 메서드는 이미지 크기를 절대 확대하지 않습니다:

```php
$image = $image->scale(800, 600);
$image = $image->scale(width: 800);
$image = $image->scale(height: 600);
```

<!-- The `cover` method resizes and crops an image to completely cover the given dimensions: -->
`cover` 메서드는 지정된 크기를 완전히 채우도록 이미지 크기를 조정하고 자릅니다:

```php
$image = $image->cover(400, 400);
```

<!-- The `contain` method resizes an image to fit within the given dimensions while preserving the entire image. If necessary, empty space will be filled using the optional background color: -->
`contain` 메서드는 전체 이미지를 유지하면서 지정된 크기 안에 맞도록 이미지 크기를 조정합니다. 필요한 경우 빈 공간을 선택적 배경색으로 채웁니다:

```php
$image = $image->contain(400, 400);
$image = $image->contain(400, 400, '#ffffff');
$image = $image->contain(400, 400, 'dominant');
```

<!-- You may specify `dominant` as the background color to fill empty space using the image's dominant color. -->
이미지의 주요 색상을 사용해 빈 공간을 채우려면 배경색으로 `dominant`를 지정할 수 있습니다.

<!-- You may crop an image using the `crop` method. The first two arguments are the desired width and height, and the optional third and fourth arguments specify the crop's `x` and `y` coordinates: -->
`crop` 메서드를 사용해 이미지를 자를 수 있습니다. 처음 두 인수는 원하는 너비와 높이이며, 선택적 세 번째와 네 번째 인수는 자르기 영역의 `x` 및 `y` 좌표를 지정합니다.

```php
$image = $image->crop(300, 200);
$image = $image->crop(300, 200, x: 50, y: 25);
```

<a name="other-transformations"></a>
<!-- ### Other Transformations -->
### Other Transformations

<!-- Laravel also provides a variety of additional image transformation methods: -->
Laravel은 다양한 추가 이미지 변환 메서드도 제공합니다:

```php
$image = $image->orient();
$image = $image->rotate(90);
$image = $image->rotate(90, '#ffffff');
$image = $image->rotate(90, 'dominant');
$image = $image->blur(5);
$image = $image->grayscale();
$image = $image->sharpen(10);
$image = $image->flipVertically();
$image = $image->flipHorizontally();
```

<!-- The `orient` method rotates the image according to its EXIF orientation data. The `rotate` method rotates the image clockwise by the given angle and accepts an optional background color. The `blur` and `sharpen` methods accept values between `0` and `100`. -->
`orient` 메서드는 이미지의 EXIF 방향 데이터에 따라 이미지를 회전합니다. `rotate` 메서드는 지정된 각도만큼 이미지를 시계 방향으로 회전하며 선택적 배경 색상을 허용합니다. `blur` 및 `sharpen` 메서드는 `0`에서 `100` 사이의 값을 허용합니다.

<a name="conditional-transformations"></a>
<!-- #### Conditional Transformations -->
#### Conditional Transformations

<!-- Image instances support Laravel's `Conditionable` trait, allowing you to conditionally apply transformations using the `when` and `unless` methods: -->
이미지 인스턴스는 Laravel의 `Conditionable` 트레이트를 지원하므로, `when` 및 `unless` 메서드를 사용해 조건부로 변환을 적용할 수 있습니다:

```php
$image = $request->image('avatar')
    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))
    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());
```

<a name="encoding-images"></a>
<!-- ## Encoding Images -->
## Encoding Images

<!-- By default, processed images are encoded using their original format. However, you may convert the image to another supported format before retrieving or storing it: -->
기본적으로 처리된 이미지는 원래 형식으로 인코딩됩니다. 하지만 이미지를 가져오거나 저장하기 전에 지원되는 다른 형식으로 변환할 수 있습니다.

```php
$image = $image->toWebp();
$image = $image->toJpg();
$image = $image->toJpeg();
$image = $image->toPng();
$image = $image->toGif();
$image = $image->toAvif();
$image = $image->toBmp();
```

<!-- You may use the `quality` method to set the output quality. The quality will be clamped between `1` and `100`: -->
출력 품질을 설정하려면 `quality` 메서드를 사용할 수 있습니다. 품질 값은 `1`에서 `100` 사이로 제한됩니다.

```php
$image = $image->toWebp()->quality(80);
```

<!-- The `optimize` method is a convenient shortcut for converting the image to a given format and setting its quality. By default, images are optimized as WebP images with a quality of `70`: -->
`optimize` 메서드는 이미지를 지정한 형식으로 변환하고 품질을 설정하는 편리한 단축 기능입니다. 기본적으로 이미지는 품질 `70`의 WebP 이미지로 최적화됩니다:

```php
$image = $image->optimize();

$image = $image->optimize(format: 'jpg', quality: 85);
```

<!-- You may retrieve the processed image contents as a string of bytes, base64 encoded string, or data URI: -->
처리된 이미지 콘텐츠를 바이트 문자열, base64로 인코딩된 문자열 또는 데이터 URI로 가져올 수 있습니다:

```php
$bytes = $image->toBytes();
$base64 = $image->toBase64();
$dataUri = $image->toDataUri();
```

<!-- An image instance may also be cast to a string to retrieve a data URI: -->
이미지 인스턴스는 데이터 URI를 가져오기 위해 문자열로 캐스팅할 수도 있습니다:

```php
$dataUri = (string) $image;
```

<a name="storing-images"></a>
<!-- ## Storing Images -->
## Storing Images

<!-- The `store` method stores the processed image on one of your application's filesystem disks. Like uploaded files, Laravel will generate a unique filename and return the stored path. The second argument may be used to specify the disk: -->
`store` 메서드는 처리된 이미지를 애플리케이션의 파일 시스템 디스크 중 하나에 저장합니다. 업로드된 파일과 마찬가지로 Laravel은 고유한 파일 이름을 생성하고 저장된 경로를 반환합니다. 두 번째 인수로 디스크를 지정할 수 있습니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars', disk: 's3');
```

<!-- You may use the `storeAs` method to specify the stored filename: -->
`storeAs` 메서드를 사용해 저장할 파일 이름을 지정할 수 있습니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');
```

<!-- The `storePublicly` and `storePubliclyAs` methods store the image with `public` visibility: -->
`storePublicly` 및 `storePubliclyAs` 메서드는 이미지의 공개 가시성을 `public`으로 설정해 저장합니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePublicly(path: 'avatars', disk: 'public');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');
```

<!-- If the image could not be stored, the storage methods return `false`. -->
이미지를 저장할 수 없으면 스토리지 메서드는 `false`를 반환합니다.

<a name="inspecting-images"></a>
<!-- ## Inspecting Images -->
## Inspecting Images

<!-- You may retrieve the image's MIME type, extension, dimensions, width, height, and dominant color using the following methods: -->
다음 메서드를 사용하면 이미지의 MIME 타입, 확장자, 크기, 너비, 높이 및 주요 색상을 가져올 수 있습니다:

```php
$mimeType = $image->mimeType();
$extension = $image->extension();

[$width, $height] = $image->dimensions();
$width = $image->width();
$height = $image->height();

$dominantColor = $image->dominantColor();
```

<!-- These methods operate on the processed image. For example, calling `width` after `cover(400, 400)` will return `400`. -->
이 메서드는 처리된 이미지에 작동합니다. 예를 들어, `cover(400, 400)`을 호출한 후 `width`를 호출하면 `400`을 반환합니다.

<a name="image-drivers"></a>
<!-- ## Image Drivers -->
## Image Drivers

<a name="custom-image-drivers"></a>
<!-- ### Custom Image Drivers -->
### Custom Image Drivers

<!-- Laravel's image manager extends Laravel's base `Illuminate\Support\Manager` class. This means you may register custom image drivers using the `extend` method available on the image manager and `Image` facade. -->
Laravel의 이미지 매니저는 Laravel의 기본 `Illuminate\Support\Manager` 클래스를 확장합니다. 따라서 이미지 매니저와 `Image` 파사드에서 사용할 수 있는 `extend` 메서드를 사용해 사용자 지정 이미지 드라이버를 등록할 수 있습니다.

<!-- Custom image drivers should implement the `Illuminate\Contracts\Image\Driver` interface. The `process` method receives the original image contents and the ordered `Illuminate\Image\ImagePipeline` that should be applied to the image, and should return the processed image bytes: -->
사용자 지정 이미지 드라이버는 `Illuminate\Contracts\Image\Driver` 인터페이스를 구현해야 합니다. `process` 메서드는 원본 이미지 콘텐츠와 이미지에 적용할 순서가 지정된 `Illuminate\Image\ImagePipeline`을 인수로 받아 처리된 이미지 바이트를 반환해야 합니다.

```php
<?php

namespace App\Images;

use Illuminate\Contracts\Image\Driver;
use Illuminate\Image\ImagePipeline;

class VipsDriver implements Driver
{
    /**
     * Process the given image contents with the specified pipeline.
     */
    public function process(string $contents, ImagePipeline $pipeline): string
    {
        // Apply the pipeline's transformations and output options...

        return $contents;
    }

    /**
     * Register a transformation handler.
     */
    public function transformUsing(string $transformation, callable $callback): static
    {
        // Store the handler so it may be applied while processing the pipeline...

        return $this;
    }
}
```

> [!NOTE]
> 사용자 지정 이미지 드라이버를 구현하는 방법을 더 잘 이해하려면 프레임워크에 내장된 `Illuminate\Image\Drivers\InterventionDriver` 클래스를 참고할 수 있습니다.

<!-- Once you have implemented your custom driver, you may register it using the `Image` facade's `extend` method. Typically, this should be done in the `boot` method of a service provider: -->
사용자 정의 드라이버를 구현한 후에는 `Image` 파사드의 `extend` 메서드를 사용해 등록할 수 있습니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 등록합니다:

```php
use App\Images\VipsDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Image;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Image::extend('vips', function (Application $app) {
        return new VipsDriver;
    });
}
```

<!-- After registering the driver, you may use it for a specific image using the `using` method: -->
드라이버를 등록한 후에는 `using` 메서드를 사용해 특정 이미지에 적용할 수 있습니다.

```php
$image = $request->image('avatar')
    ->using('vips')
    ->cover(400, 400);
```

<!-- You may also configure a custom driver as your application's default image driver using the `default` option in your application's `config/images.php` configuration file or the `IMAGE_DRIVER` environment variable: -->
사용자 애플리케이션의 `config/images.php` 설정 파일에서 `default` 옵션을 사용하거나 `IMAGE_DRIVER` 환경 변수를 설정해 커스텀 드라이버를 애플리케이션의 기본 이미지 드라이버로 구성할 수도 있습니다:

```ini
IMAGE_DRIVER=vips
```

<a name="custom-transformations"></a>
<!-- ### Custom Transformations -->
### Custom Transformations

<!-- Applications and packages may define custom transformations by creating a class that implements the `Illuminate\Contracts\Image\Transformation` contract. Custom transformations can then be added to an image pipeline using the `transform` method: -->
애플리케이션과 패키지는 `Illuminate\Contracts\Image\Transformation` 컨트랙트를 구현하는 클래스를 생성해 사용자 지정 변환을 정의할 수 있습니다. 그런 다음 `transform` 메서드를 사용해 이미지 파이프라인에 사용자 지정 변환을 추가할 수 있습니다.

```php
<?php

namespace App\Images\Transformations;

use Illuminate\Contracts\Image\Transformation;

class Pixelate implements Transformation
{
    public function __construct(
        public readonly int $size,
    ) {
        //
    }
}
```

<!-- Next, register a handler for the transformation and driver using the `Image` facade's `transformUsing` method. Typically, this should be done in the `boot` method of a service provider: -->
다음으로 `Image` 파사드의 `transformUsing` 메서드를 사용해 변환 및 드라이버의 핸들러를 등록합니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 이 작업을 수행해야 합니다:

```php
use App\Images\Transformations\Pixelate;
use Illuminate\Support\Facades\Image;
use Intervention\Image\Interfaces\ImageInterface;

Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {
    return $image->pixelate($transformation->size);
});
```

<!-- Once the transformation handler has been registered, you may apply the transformation to an image: -->
변환 핸들러를 등록한 후 이미지에 변환을 적용할 수 있습니다.

```php
use App\Images\Transformations\Pixelate;

$image = $request->image('avatar')
    ->transform(new Pixelate(12))
    ->store('avatars');
```
