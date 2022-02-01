package net.endlos.xdt99.xga99r;

import com.intellij.lang.Commenter;
import org.jetbrains.annotations.Nullable;

public class Xga99RCommenter implements Commenter {

    @Override
    @Nullable
    public String getLineCommentPrefix() {
        return ";";
    }

    @Override
    @Nullable
    public String getBlockCommentPrefix() {
        return null;
    }

    @Override
    @Nullable
    public String getBlockCommentSuffix() {
        return null;
    }

    @Override
    @Nullable
    public String getCommentedBlockCommentPrefix() {
        return null;
    }

    @Override
    @Nullable
    public String getCommentedBlockCommentSuffix() {
        return null;
    }

}
