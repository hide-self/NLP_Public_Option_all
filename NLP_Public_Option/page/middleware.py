# middleware.py
from django.http import HttpResponseNotFound
from django.template import TemplateDoesNotExist, loader
from django.conf import settings
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)


class Custom404Middleware:
    """
    自定义404中间件

    这个中间件可以在DEBUG模式下也能显示自定义404页面，
    而不是Django默认的详细错误页面。

    工作原理:
    1. 捕获所有响应
    2. 检查响应状态码是否为404
    3. 如果是404且不是管理后台请求，则渲染自定义404模板
    4. 返回自定义404响应

    注意: 这个中间件应该放在中间件栈的最后，以确保它能捕获到所有404响应
    """

    def __init__(self, get_response):
        """
        初始化中间件

        Django使用这个模式初始化中间件，get_response是下一个中间件或视图的调用
        """
        self.get_response = get_response
        # 可以在这里进行一次性配置和初始化

    def __call__(self, request):
        """
        处理每个请求的主要方法

        Args:
            request: HttpRequest对象，包含请求的所有信息

        Returns:
            HttpResponse对象
        """
        # 调用下一个中间件或视图，获取响应
        response = self.get_response(request)

        # 检查响应状态码是否为404
        if response.status_code == 404:
            # 排除管理后台的请求，让Django处理管理后台的404
            if not request.path.startswith('/admin/'):
                # 记录404错误，便于调试
                logger.warning(f"404错误: 用户访问了不存在的页面: {request.path}")

                # 尝试渲染自定义404模板
                try:
                    # 加载404模板
                    template = loader.get_template('404.html')

                    # 创建上下文，可以传递额外信息到模板
                    context = {
                        'request_path': request.path,
                        'debug_mode': settings.DEBUG,
                    }

                    # 渲染模板并返回404响应
                    return HttpResponseNotFound(
                        template.render(context, request),
                        content_type='text/html'
                    )

                except TemplateDoesNotExist:
                    # 如果自定义404模板不存在，回退到默认行为
                    logger.error("自定义404模板未找到，使用默认404页面")
                    return response

        # 如果不是404响应，直接返回
        return response

    def process_exception(self, request, exception):
        """
        处理视图中的异常

        这个方法可以捕获视图函数中抛出的异常，但不会影响404处理，
        因为404通常是在路由解析阶段产生的，不会触发这个异常处理。

        保留这个方法是为了中间件的完整性，但在这个场景下可能不会用到。
        """
        # 可以在这里处理其他类型的异常
        return None