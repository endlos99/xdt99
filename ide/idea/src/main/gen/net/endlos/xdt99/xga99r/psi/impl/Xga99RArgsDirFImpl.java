// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99r.psi.Xga99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99r.psi.*;

public class Xga99RArgsDirFImpl extends ASTWrapperPsiElement implements Xga99RArgsDirF {

  public Xga99RArgsDirFImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99RVisitor visitor) {
    visitor.visitArgsDirF(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99RVisitor) accept((Xga99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public Xga99ROpFloat getOpFloat() {
    return findNotNullChildByClass(Xga99ROpFloat.class);
  }

}