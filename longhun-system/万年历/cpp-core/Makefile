# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂万年历 · C++17内核 Makefile                         ║
# ║  DNA: #龍芯⚡️2026-04-12-MAKEFILE-v1.0                   ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ╚══════════════════════════════════════════════════════════╝

CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -I include

SRCS = calendar/lunar_engine.cpp \
       bagua/bagua_engine.cpp \
       digital_root/sancai_engine.cpp \
       dna/dna_activator.cpp

OBJS = $(SRCS:.cpp=.o)

TEST_TARGET = test_calendar
LIB_TARGET = liblonghun_calendar.a

.PHONY: all clean test

all: $(LIB_TARGET) $(TEST_TARGET)

# 静态库（给Swift桥接用）
$(LIB_TARGET): $(OBJS)
	ar rcs $@ $^
	@echo "✅ 龍魂万年历内核库已构建: $@"

# 测试程序
$(TEST_TARGET): tests/test_main.cpp $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^
	@echo "✅ 测试程序已构建: $@"

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

test: $(TEST_TARGET)
	@echo "═══════════════════════════════════════"
	@echo "🐉 龍魂万年历 C++17 内核测试"
	@echo "═══════════════════════════════════════"
	./$(TEST_TARGET)

clean:
	rm -f $(OBJS) $(LIB_TARGET) $(TEST_TARGET)
	@echo "🧹 已清理"
