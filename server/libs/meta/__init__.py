class Singleton(type):
	_instances = {}
	# 当创建类对象时候，就会调用type函数。
	# 当调用type函数时候，就等于调用以下函数。
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super().__call__(*args, **kwargs)
		return cls._instances[cls]
