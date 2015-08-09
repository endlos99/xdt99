package net.endlos.xdt99.xbas99;

import com.intellij.openapi.fileTypes.FileTypeConsumer;
import com.intellij.openapi.fileTypes.FileTypeFactory;
import net.endlos.xdt99.xbas99.Xbas99FileType;
import org.jetbrains.annotations.NotNull;

public class Xbas99FileTypeFactory extends FileTypeFactory{
    @Override
    public void createFileTypes(@NotNull FileTypeConsumer fileTypeConsumer) {
        fileTypeConsumer.consume(Xbas99FileType.INSTANCE, "b99");
    }
}
